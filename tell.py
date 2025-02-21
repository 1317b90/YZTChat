import json
import requests

API_URL="https://test.g4b.cn/rpa/api"
# API_URL="http://127.0.0.1:8080"


# 获取用户信息
def get_user(userid:str):
    response=requests.get(f"{API_URL}/user/{userid}")
    if response.status_code==200:
        response=response.json()
        return response["data"]
    else:
        print(response.text)
        return {}

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
    print(get_message("admin_flx"))