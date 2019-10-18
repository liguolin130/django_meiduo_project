import random

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.constants import SMS_CODE_EXPIRES, SEND_SMS_CODE_INTERVAL
from meiduo_mall.libs.captcha.captcha import captcha
from meiduo_mall.utils import constants

# from meiduo_mall.celery_tasks.sms.constants import SMS_CODE_EXPIRES, SEND_SMS_CODE_INTERVAL
from celery_tasks.sms.tasks import send_sms_code
from meiduo_mall.apps.verifications import serializers


class ImageCodeView(APIView):
    """
    图片验证码
    """

    def get(self, request, image_code_id):
        """
        获取图片验证码
        """
        # 生成验证码图片
        name, text, image = captcha.generate_captcha()

        # 连接redis数据库
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        print(text)
        # 指定返回的数据类型
        return HttpResponse(image, content_type="images/jpg")


class SMSCodeView(GenericAPIView):
    """
    短信验证码
    """
    serializer_class = serializers.CheckImageCodeSerialzier

    def get(self, request, mobile):
        # print(1223)
        """
        创建短信验证码
        """
        # 判断图片验证码, 判断是否在60s内
        serializer = self.get_serializer(data=request.query_params)
        # 校验
        serializer.is_valid(raise_exception=True)

        # 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        print("短信验证码内容是：%s" % sms_code)

        # 保存短信验证码与发送记录
        redis_conn = get_redis_connection('verify_codes')
        # 短讯验证码有效期
        redis_conn.setex("sms_%s" % mobile, SMS_CODE_EXPIRES, sms_code)
        # 短讯验证码发送间隔
        redis_conn.setex("send_flag_%s" % mobile, SEND_SMS_CODE_INTERVAL, 1)

        # 发送短信验证码
        return Response({"message": "OK"}, status.HTTP_200_OK)
