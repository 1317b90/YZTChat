import json
import requests

API_URL="https://test.g4b.cn/rpa/api"
# API_URL="http://127.0.0.1:8080"


# 获取用户信息
def get_user_data(userid:str):
    url=f"{API_URL}/user/{userid}"
    response=requests.get(url)
    response_data=response.json()
    if "data" not in response_data.keys():
        raise Exception("该用户不存在")
    return response_data["data"]

# 获取所有用户
def get_users():
    params = {
        "IsAdmin": "false",
        "IsZero": "false",
        "IsBill": "false"
    }
    response = requests.get(f"{API_URL}/user", params=params)
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("data", [])
    else:
        print(f"获取用户数据失败: {response.text}")
        return []

# 修改用户
def put_user(data:dict):
    response=requests.put(f"{API_URL}/user",json=data)
    if response.status_code==200:
        return True
    else:
        return False

# 获取记忆
def get_memory(userid:str):
    params={"key":"memory_"+userid}
    response=requests.get(f"{API_URL}/redis/value",params=params)

    if response.status_code==200:
        response=response.json()
        response=json.loads(response.get("data",{}))
        return response
    else:
        print(response.text)
        return {}

# 清空记忆（开票）
def cancel_invoice(userid:str):
    memory_data=get_memory(userid)

    if "开票信息" in memory_data:
        del memory_data["开票信息"]
    if "开票项目编码列表" in memory_data:
        del memory_data["开票项目编码列表"]

    data={"key":"memory_"+userid,"value":json.dumps(memory_data,ensure_ascii=False)}
    response=requests.post(f"{API_URL}/redis/value",json=data)
    if response.status_code==200:
        return "开票任务已经取消"
    else:
        return f"开票任务取消失败：{response.text}"


# 存储聊天记录
def add_message(data:dict):
    response=requests.post(f"{API_URL}/message",json=data)
    if response.status_code==200:
        return True
    else:
        return False

# 获取用户最近的消息记录
def get_message(userid:str):
    try:
        response=requests.get(f"{API_URL}/message/new/{userid}")
        if response.status_code==200:
            response= response.json()
            return response["data"]
        else:
            return []
    except Exception as e:
        print("获取最近的消息记录失败",e)
        return []
    
# 发送消息
def send_message(serviceid,userid,content):
    payload = {
        'serviceid':serviceid,
        'userid': userid,
        'type': 'text',
        'content': content,
    }
    response=requests.post(f"{API_URL}/message/send",json=payload)
    if response.status_code==200:
        return True
    else:
        print(response.text)
        return False

# 润色消息
def polish_message(data:dict):
    response=requests.post(f"{API_URL}/message/polish",json=data)
    if response.status_code==200:
        return True
    else:
        return False


# 创建开票任务
def create_make_invoice(data:dict):
    data={
        "type":"make_invoice",
        "input":data        
    }
    response=requests.post(f"{API_URL}/task",json=data)
    try:
        response_data=response.json()

        if response.status_code==200:
            return True
        else:
            return response_data["message"]
    
    except Exception as e:
        print(e)
        return response.text



if __name__=="__main__":
    users=get_users()
    for user in users:
        a=send_message("yzt_serviceid",user.get('UserID',''),"您好，麻烦导出上个月的银行回单和银行对账单，入账需要，谢谢配合")
        print(a)
