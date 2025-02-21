import AI
import time
messages=[
        {
            "role": "user",
            "content": "发票抬头:李子柒 金额:123 餐费 普通发票"
        }
    ]

# 记录开始时间
start_time = time.time()

# 调用API
response_message = AI.receive(messages)

print(response_message)

