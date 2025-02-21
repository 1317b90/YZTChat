import AI
import models
import tell

# 创建开票任务
def create_task(data:dict):
    result=tell.create_make_invoice(data)
    if result:
        return "开票任务创建成功"
    return True
    

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

