from celery_tasks.main import celery_app
from celery_tasks.sms import constants
# from verifications import constants
from celery_tasks.sms.yuntongxun.sms import CCP




# name=自定义任务名字
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    # 利用容联云平台发短信
    # CCP().send_template_sms('接收短信手机号', ['短信验证码', '提示用户短信验证码多久过期单位分钟'],'模板ID')
    CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_EXPIRE_TIMEOUT], '1')





# 启动celery
# celery -A celery_tasks.main worker -l info