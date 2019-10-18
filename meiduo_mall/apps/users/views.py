import re

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers
from users.models import User
from users.utils import get_user_by_account
from verifications.serializers import CheckImageCodeSerialzier


class UsernameCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)


class UserView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer


class SMSCodeTokenView(GenericAPIView):
    """
    根据账号和图片验证码，获取发送短信的token
    """
    serializer_class = CheckImageCodeSerialzier

    def get(self, request, account):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = get_user_by_account(account)
        print(user,111111111111111111111111111111111111111)
        if user is None:
            return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 生成发送短信的access_token
        access_token = user.generate_send_sms_token()

        # 处理手机号
        mobile = re.sub(r'(\d{3})\d{4}(\d{3})', r'\1****\2', user.mobile)
        return Response({'mobile': mobile, 'access_token': access_token})