import json
import requests

API_URL="https://test.g4b.cn/rpa/api"

# 获取用户信息
def get_user(phone:str):
    response=requests.get(f"{API_URL}/user/{phone}")
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

# 使用手机号搜索对应的任务输入数据
def get_task_data(phone:str):
    params={"key":"make_invoice_"+phone}
    response=requests.get(f"{API_URL}/redis/value",params=params)

    if response.status_code==200:
        response=response.json()
        response=json.loads(response.get("data",{}))
        return response
    else:
        print(response.text)
        return {}
    
# 设置任务输入数据
def set_task_data(phone:str,data:dict):
    data={"key":"make_invoice_"+phone,"value":json.dumps(data)}
    response=requests.post(f"{API_URL}/redis/value",json=data)
    if response.status_code==200:
        return True
    else:
        return False



# 创建开票任务
def create_task(data:dict):
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
    
    # print(set_task_data("13076785712",{"name":"张三"}))
    print(get_task_data("admin_flx"))
    # print(put_user({"Phone":"13800138000","CompanyName":"广州逐辉贸易有限公司"}))
    # print(get_user("13800138000"))