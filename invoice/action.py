import json
from datetime import datetime
import tell,AI



"""
    invoice_data:
    {
        "title": 抬头：，项目：，金额：
        "data":
        "table":
        "create_time"：
    }
"""

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



to_dict={
    '销售方税号': 'uscid', 
    '电子税务局用户名': 'dsj_username', 
    '电子税务局密码': 'dsj_password', 

    '购买方名称': 'buy_name', 
    '购买方税号': 'buy_id', 
    '购买方地址': 'buy_address', 
    '购买方电话': 'buy_phone', 
    '购买方银行名称': 'buy_bank_name',
    '购买方银行账号': 'buy_bank_id',
    '购买方邮箱': 'buy_email', 

    '开票项目': 'invoice_name',
    '金额': 'invoice_amount',
    '发票类型': 'invoice_type', 
    '规格型号': 'invoice_model', 
    '单位': 'invoice_unit', 
    '数量': 'invoice_num',
    '单价': 'invoice_price',

    '销售方银行名称': 'sell_bank_name', 
    '销售方银行账号': 'sell_bank_id',

    '项目编码': 'invoice_code',
    '是否预览发票': 'is_preview', 
    '企业微信ID': 'wecome_id', 
    '任务ID': 'task_id', 
   
    '销售方公司名称': 'company_name'
    }


to_to_dict={v: k for k, v in to_dict.items()}

# 将输入的字符串使用AI解析后转换
def transform(data_str:str):
    exampleJson={
    '购买方名称': 'xxx有限公司', 
    '购买方税号': '91440106MADPE88G37', 
    '购买方地址': '广州市越秀区', 
    '购买方电话': '031183092917', 
    '购买方银行名称': 'xx银行xx支行',
    '购买方银行账号': '1003014180002676',
    '购买方邮箱': 'xxx@qq.com', 

    '开票项目': '冰箱',
    '金额': '1000',
    '发票类型': '普通发票', 
    '规格型号': '大', 
    '单位': 'Kg', 
    '数量': '1',
    '单价': '1000',
    }
    exampleStr=""
    for key in exampleJson.keys():
        exampleStr+=f"{key}：{exampleJson[key]}\n"

    system_prompt = f"""
    # ruler
    - 根据用户输入的文字信息，提取出关键字段
    - 严格按照例子中的输出来转化并输出json格式
    - 用户输入时可能不会按照例子中的格式输入前缀，需要按照顺序灵活识别
    - 用户没有输入的信息，对应Json的值就为空字符串
    - 不可将EXAMPLE中的信息输出
    - 开票类型有：普通发票、增值税专用发票

    # EXAMPLE INPUT: 
    {exampleStr}
    # EXAMPLE JSON OUTPUT:
    {exampleJson}
    """

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": data_str}]

    respone={}

    mod=AI.DeepSeek()
    respone=mod.chat(messages,isJson=True)

    for key in exampleJson.keys():
        # 不管存不存在值，都会将其转换为字符串
        # 如果用户没填的也会自动补充
        respone[key]=str(respone.get(key,""))

        # 转换名称
        respone[to_dict[key]] = respone.pop(key)
    return respone


# 要开票啦要开票啦
def start(phone:str,data_str:str):
    if "admin" in phone:
        sell_phone=tell.get_user(phone).get("PuppetID","")
    else:
        sell_phone=phone
    try:
        data=transform(data_str)
    except Exception as e:
        print(e)
        return "开票信息解析失败，请检查后重试！"
    
    sell_data=tell.get_user(sell_phone)

    data["uscid"]=sell_data.get("Uscid","")
    data["dsj_username"]=sell_data.get("DsjUsername","")
    data["dsj_password"]=sell_data.get("DsjPassword","")
    data["company_name"]=sell_data.get("CompanyName","")
    data["sell_bank_name"]=sell_data.get("BankName","")
    data["sell_bank_id"]=sell_data.get("BankID","")
    
    data["wecome_id"]=phone
    data["is_preview"]=True

    # 必填项目
    need_key=""
    for key in ("uscid","dsj_username","dsj_password","company_name","sell_bank_name","sell_bank_id","invoice_name","invoice_amount","buy_name","invoice_type"):
        if data[key]=="":
            need_key+=f"{to_to_dict[key]}，"

    if need_key!="":
        return f"很抱歉，您的{need_key}信息缺失，请您更新后再重新发起开票哦"

    invoice_data={
        "title":f"抬头：{data['buy_name']}，项目：{data['invoice_name']}，金额：{data['invoice_amount']}",
        "data":data,
        "table":None,
        "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    tell.set_task_data(phone,invoice_data)

    # 如果开票类型没填：
    if data.get("invoice_type","")=="":
        return "您好，您的开票类型尚未确认。请问您需要开具普通发票还是专用发票呢？"

    # 创建任务
    create_result=tell.create_task(data)
    if create_result==True:
        return "已收到您的信息，正在处理中。稍后我会将开票结果发送给您，请稍等片刻。"
    else:
        return "创建任务失败，请稍后再试。"+create_result



# 确认开票类型
def confirm_invoice(phone:str,receive_msg:str):
    invoice_data=tell.get_task_data(phone)
    if "普通" in receive_msg:
        invoice_data["data"]["invoice_type"]="普通发票"
    elif "专用" in receive_msg:
        invoice_data["data"]["invoice_type"]="增值税专用发票"
    else:
        cancel(phone)
        return "抱歉，刚才没有完全理解您的意思。为了避免误开票，已暂时取消了开票。如果您需要开票，请随时重新发起申请。感谢您的理解！"

    # 创建任务
    tell.create_task(invoice_data["data"])
    
    return f"已确认开票类型为{invoice_data['data']['invoice_type']}，正在处理中。稍后我会将开票结果发送给您，请稍等片刻。"


# 确认用户选择的商品编码
def confirm_coding(phone:str,invoice_id):
    try:
        invoice_id=int(invoice_id)
    except:
        return "请您根据表格中的内容，选择并发送正确的序号或编码给我哦。谢谢！"

    # 只选最后一条
    # 包括临时数据和table数据
    invoice_data=tell.get_task_data(phone)

    if invoice_id<6 and invoice_id>0:
        column = [row[1] for row in invoice_data["table"]]
        invoice_id=column[invoice_id]

    elif invoice_id>10000:
        pass

    else:
        return "请您根据表格中的内容，选择并发送正确的序号或编码给我哦。谢谢！"


    invoice_data["data"]["invoice_code"]=invoice_id
    invoice_data["data"]["is_preview"]=True

    # 重新创建一次任务
    tell.create_task(invoice_data["data"])

    return "已确认您的编码，正在处理中。稍后我会将开票结果发送给您，请稍等片刻。"




# 确认开票
def confirm(phone:str):

    # 获取数据库数据
    invoice_data=tell.get_task_data(phone)
    
    # 跳过发票预览
    invoice_data["data"]["is_preview"]=False

    
    # 再次创建任务
    tell.create_task(invoice_data["data"])

    return "您的发票已经确认，稍后我会将发票文件发送给您，请稍等片刻。"



if __name__=="__main__":


    msg="""抬头：广州市中山纪念堂管理中心
税号：12440100455353005K
邮箱：1403474204@qq.com
金额：279.44元"""
    print(transform(msg))
 