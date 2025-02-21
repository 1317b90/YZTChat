from openai import OpenAI

from . import system,tools

client = OpenAI(
    # 替换为您需要调用的模型服务Base Url
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 环境变量中配置您的API Key
    api_key="06999cd5-28da-4ad4-9933-228594785837",
)

model="ep-20250218142425-5t6h5"


# 接收并返回消息
def receive(
        messages:list,
        temperature:float=1.0,
        memory:dict={}
        ):

    system_prompt=system.receive
    # 是否追加记忆
    if memory:
        system_prompt+="\n# 记忆\n"
        for key,value in memory.items():
            system_prompt+=f"## {key}:\n{value}\n"

    sys_messages=[
        {"role": "system", "content": system_prompt}, 
    ]

    messages=sys_messages+messages

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools.main,
        stream=False,
        temperature=temperature,
    )
    try:
        return completion.choices[0].message
    # 如果出错，递归重试
    except:
        return receive(messages,temperature,memory)


# 润色
def polish(
    messages:list,
    temperature:float=1.0,
):

    sys_messages=[
        {"role": "system", "content": system.polish}, 
    ]

    messages=sys_messages+messages

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        temperature=temperature,
    )
    
    try:
        return completion.choices[0].message.content
    # 如果出错，递归重试
    except:
        return polish(messages,temperature)
