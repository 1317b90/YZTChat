from openai import OpenAI
import json
from pathlib import Path


# 去除markdown语法
def removeMark(text):
    remove_chars = ["#", "**", "- ","\n\n","```json","```","\n","\t"," "]
    for char in remove_chars:
        text = text.replace(char, "")

    return text


# ------- 深度求索 ------- 深度求索------- 深度求索------- 深度求索------- 深度求索------- 深度求索------- 深度求索
class DeepSeek():
    def __init__(self):
        self.client = OpenAI(
            api_key="sk-42755e5134584426b7405843e4746a0d",
            base_url="https://api.deepseek.com",
        )

    # 一般对话
    def chat(self,messages:list,max_tokens=1024,temperature=1.0,stream=False,isJson=False,isRemoveMark=True):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.0 if isJson else temperature,
            stream=stream,
            response_format= {
                'type': 'json_object' if isJson else 'text'
            }
        )

        result=response.choices[0].message.content
        if isRemoveMark:
            result=removeMark(result)
        if isJson:
            try:
                result=json.loads(result)
            except:
                result={}
                
        return result
# --------- 智谱 --------- 智谱 --------- 智谱 --------- 智谱 --------- 智谱 --------- 智谱 --------- 智谱 --------- 智谱 --------- 智谱
class Zhipu():
    def __init__(self):
        self.client = OpenAI(
            api_key="b584a661b8ad396befa3796f23040a62.6eRLSQxYOITVLDaC",
            base_url="https://open.bigmodel.cn/api/paas/v4/",
        )

    # 一般对话
    def chat(self,messages:list,temperature=0.0,top_p=0.7,isJson=False,isRemoveMark=True):
        response =self. client.chat.completions.create(
            model="glm-4-flash",  
            messages=messages,
            top_p=top_p,
            temperature=temperature
        ) 

        result=response.choices[0].message.content
        if isRemoveMark:
            result=removeMark(result)
        if isJson:
            try:
                result=json.loads(result)
            except:
                result={}
                
        return result

    # 上传文件并返回id
    def up_file(self,filePath:str):
        fileData = self.client.files.create(file=Path(filePath), purpose="file-extract")
        return fileData.id

    # 解析文件
    def parse_file(self,fileId:str):
        return json.loads(self.client.files.content(fileId).content)["content"]

    # 删除文件
    def del_file(self,fileId:str):
        return  self.client.files.delete(
        file_id=fileId
        )

    # 上传文件，解析，删除文件，一条龙服务
    def pack_file(self,filePath:str):
        fileId=self.up_file(filePath)
        content=self.parse_file(fileId)
        self.del_file(fileId)
        return content

def main(args):
    pass
