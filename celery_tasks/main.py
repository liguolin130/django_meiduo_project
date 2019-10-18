
# 创建celery应用
from celery import Celery

celery_app = Celery('meiduo_project')

# 引入celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])