from typing import Optional
from pydantic import BaseModel


# 接收到的消息格式
class Message(BaseModel):
    userid:str
    serviceid: str
    messages: list
    answer: Optional[str] = None

# 润色所需的消息格式
class PolishMessage(BaseModel):
    userid:str
    serviceid: str
    message: str

# 群聊的消息格式
class GroupMessage(BaseModel):
    userid:str
    serviceid: str
    adminid: str
    message: str


# 发票格式验证
class Invoice(BaseModel):
    buy_name: str  # 购买方名称（发票抬头）
    buy_id: str = ""  # 购买方社会统一代码或身份证号码
    buy_email: str = ""  # 购买方邮箱号
    buy_address: str = ""  # 购买方地址
    buy_phone: str = ""  # 购买方电话
    buy_bank_name: str = ""  # 购买方开户银行名称
    buy_bank_id: str = ""  # 购买方开户银行卡号
    invoice_type: str  # 发票类型
    invoice_name: str  # 开票项目(商品名称)
    invoice_amount: str  # 金额
    invoice_model:str = ""  # 规格
    invoice_unit: str = ""  # 单位
    invoice_num: str = ""  # 数量
    invoice_price: str = ""  # 单价
    invoice_code: str = ""  # 项目编码(商品编码)
    is_preview: bool = True  # 是否预览发票

    userid: str = ""
    serviceid: str = ""
    adminid: str = ""
    is_group: bool = False
