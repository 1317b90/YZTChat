from openai import OpenAI

from . import system,tools
import re

client = OpenAI(
    # 替换为您需要调用的模型服务Base Url
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 环境变量中配置您的API Key
    api_key="06999cd5-28da-4ad4-9933-228594785837",
)

model="ep-20250218142425-5t6h5"#

# 接收并返回消息
def receive(
        messages: list,
        temperature: float = 0.77,
        memory: dict = {},
        retry_count: int = 0
    ):

    system_prompt = system.receive
    # 是否追加记忆
    if memory:
        system_prompt += "\n# 记忆\n"
        for key, value in memory.items():
            system_prompt += f"## {key}:\n{value}\n"
    else:
        system_prompt += "\n# 记忆\n无任何任务记忆"

    sys_messages = [
        {"role": "system", "content": system_prompt},
    ]

    messages = sys_messages + messages

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools.main,
            stream=False,
            temperature=temperature,
        )
        completion.choices[0].message.content=remove_repeated(completion.choices[0].message.content)
        return completion.choices[0].message
    # 如果出错，递归重试
    except Exception as e:
        error_message = str(e)
        if "requests.exceptions" in error_message:
            if retry_count < 3:
                return receive(messages, temperature, memory, retry_count + 1)
            else:
                raise Exception("AI获取回复失败")
        else:
            raise Exception(error_message)



# 润色
def polish(
    messages:list,
    temperature:float=1,
    retry_count: int = 0
):

    sys_messages=[
        {"role": "system", "content": system.polish}, 
    ]

    messages=sys_messages+messages

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
            temperature=temperature,
        )

        return remove_repeated(completion.choices[0].message.content)
    # 如果出错，递归重试
    except:
        if retry_count < 3:
            return polish(messages, temperature, retry_count + 1)
        else:
            raise Exception("多次获取回复失败")


# 群聊消息
def group(
        message: list,
        temperature: float = 0.1,
    ):

    messages = [
        {"role": "system", "content":  system.group},
        {"role":"user","content":message}
    ]

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools.make_invoice,
        stream=False,
        temperature=temperature,
    )
    completion.choices[0].message.content=remove_repeated(completion.choices[0].message.content)
    return completion.choices[0].message

# 去除重复回复
def remove_repeated(text):
    text = re.sub(r'\n{2,}', '', text)
    # 匹配包括换行符和空白字符的重复子串
    pattern = r'(.+?)\s*\1+'  # \s* 匹配零个或多个空白字符（包括换行符）
    return re.sub(pattern, r'\1', text, flags=re.DOTALL)