from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
# Create your models here.
from meiduo_mall.utils import constants


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_send_sms_token(self):
        """
        生成发送短信验证码的token
        """
        # itsdangerous模型实例,第一个参数为配置密钥,第二个为过期时间
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.SEND_SMS_TOKEN_EXPIRES)
        data = {
            'mobile': self.mobile
        }
        token = serializer.dumps(data)
        return token.decode()

