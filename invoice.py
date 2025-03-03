import AI
import models
import tell
import json
# 创建开票任务
def create_task(arguments:models.Invoice,M:models.Message):
    arguments.userid=M.userid
    arguments.serviceid=M.serviceid

    # 如果不预览发票,将发票代码置为空
    if not arguments.is_preview:
        arguments.invoice_code=""

    # 如果是群聊，则不需要预览
    if arguments.is_group:
        arguments.is_preview=False

    # 如果邮箱不为空，去除<a>
    if arguments.buy_email:
        arguments.buy_email=arguments.buy_email.replace("<a>", "").replace("</a>", "")
    
    print(arguments)
    # 创建开票任务
    result=tell.create_make_invoice(arguments.model_dump())
    if result !=True:
        raise result       


# 开票准备
def prepare(phone:str):
    invoice_data=tell.get_task_data(phone)

    if invoice_data!={}:
        return f"""您在{invoice_data["create_time"]}发起的开票任务
{invoice_data["title"]}
还在进行中，请稍等喔"""
    # elif is_fix==True:
    #     return "抱歉，目前电子税务局网站正在维护中，暂时无法开票。请您稍后再试，感谢您的耐心等待！"
    else:
        return None

# 取消开票
def cancel(phone:str):
    tell.set_task_data(phone,{})

