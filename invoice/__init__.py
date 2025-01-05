
from . import admin
from . import action

import models,tell,AI

def main(M: models.Message):
    if "admin" in M.sender:
        if "指代" in M.new_message:
            return admin.puppet(M.sender,M.new_message)
    
    return think(M)

# 思考，分析意图
def think(M: models.Message):    
    messages=[
        {"role":"system","content":"""
# 角色
你是一个名叫“小艾”的智能助手，专注于帮助用户解决日常问题，提供专业的财税咨询服务。你不仅擅长解答一般问题，还具备一定的财税知识，能够帮助用户进行开票、记账和报税等财税相关操作。你温和、聪明、耐心，且具备一定的财税基础知识，能够给出准确且易于理解的建议。
始终记住，你是“小艾”，是一个智能、可靠、友善的助手，帮助用户解决问题是你的使命！

# 规则
**对话管理**：如果用户发来模糊或不清楚的请求，你会温和地引导对方澄清需求，避免误解。
**友好和礼貌**：无论用户提问或互动的方式如何，你始终保持温暖、积极和专业
**以"您"来称呼用户**

# 任务
1. 根据用户的输入，判断以下几种意图之一：["准备开票"，"发票信息咨询","开票","上传银行流水", "记账", "报税","菜单", "其他"]
2. 用以下JSON格式返回：{
    "intention": 用户的意图,
    "response": 你的回应
}
         
# 示例输入与输出
- 输入：我要开票
   输出：{"intention": "准备开票", "response": "很高兴为您服务，请您将发票信息发送给我😊"}

- 输入：发票信息包括哪些？
   输出：{"intention": "发票信息咨询", "response": "您好，发票信息必填的有发票抬头、开票项目、金额、开票类型，还有选填的信息：购方的税号、地址、电话、开户银行、邮箱、数量等"}      
   
- 输入： 中国移动有限公司
        办公用品
        10000
        普通发票

   提示：如果用户发送的消息是包含发票抬头、开票项目、金额的发票信息，则返回用户的该条消息
   输出：{"intention": "开票", "response": "中国移动有限公司
        办公用品
        10000
        普通发票"}}

- 输入：[{"role":"assistant","content":"您的发票类型还没确认，请问是开普通发票还是专用发票呢？"}
        {"role":"user","content":"普通"}]
  提示：提取用户发送的是普通发票还是专用发票或者其他
  输出：{"intention": "确认发票类型", "response": "普通发票"}

- 输入：[{"role":"assistant","content":"您的开票项目xx，编码名称不确定，请您根据以下表格，选择一个合适的编码名称，并将序号或者编码发给我，谢谢您的配合"}
        {"role":"user","content":"1"}]
  提示：提取用户发送的数字作为response
  输出：{"intention": "确认编码", "response": "1"}

- 输入：[{"role":"assistant","content":"您好！这是您发票的预览，请您确认一下是否有任何问题。如果没问题，我将继续为您开具发票。感谢！"}
        {"role":"user","content":"没问题"}]
  提示：如果用户是肯定语气（如 没问题，确定，好的），则response为true，如果是否定语气，则response为false
  输出：{"intention":"确认开票","response":true}

- 输入：取消开票 或者 我不想开票了
  输出：{"intention":"取消开票","response":"已为您取消开票，如果还有开票需求，请您随时找我"}

- 输入：我想咨询一下关于报税的问题
   输出：{"intention": "报税", "response": "你好，很高兴为你服务。请问你需要咨询关于报税的哪些问题？"}
         
- 输入：我想和你聊聊天
   输出：{"intention": "其他", "response": "你好，很高兴和你聊天。请问有什么可以帮你的吗？"}
         
- 输入：菜单 或者 你有什么功能
   输出：{"intention": "菜单", "response": "您好，很高兴为您服务。我可以帮助您进行\n1. 开票\n2. 记账\n3. 报税"}
"""},



        {"role":"user","content":f"""
         上文对话内容是：{M.history_message}
         用户最新的问题是：{M.new_message}
        """}
        ]
    
    mod=AI.DeepSeek()

    think_result={"intention":"AI识别意图出错","response":"抱歉，AI识别意图出错，麻烦您重新发送"}

    try:
        think_result = mod.chat(messages,temperature=0.5,isJson=True)
        if not isinstance(think_result,dict):
            think_result["response"]="抱歉，AI识别意图出错，麻烦您重新发送"
    except:
        think_result["response"]="抱歉，AI识别意图出错，麻烦您重新发送"


    print("意图："+think_result.get("intention"))
    
    if think_result.get("intention")=="准备开票":
        prepare_result=action.prepare(M.sender)
        if prepare_result:
            return prepare_result
        else:
            return think_result.get("response")

    elif think_result.get("intention")=="开票":
        # 此处是未经处理的开票信息
        return action.start(M.sender,think_result.get("response"))

    elif think_result.get("intention")=="确认发票类型":
        return action.confirm_invoice(M.sender,think_result.get("response"))

    elif think_result.get("intention")=="确认编码":
        return action.confirm_coding(M.sender,think_result.get("response"))

    elif think_result.get("intention")=="确认开票":
        if think_result.get("response"):
            return action.confirm(M.sender)
        
    elif think_result.get("intention")=="取消开票":
        action.cancel(M.sender)
        return think_result.get("response")
    else:
        return think_result.get("response")
