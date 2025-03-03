import AI
import time
messages=[
        {
            "role": "user",
            "content": "抬头:穆君; 金额:10.00; 邮箱:ngzddbe-19219@kfp.meituan.com 普通发票 餐费"
        }
    ]

# 记录开始时间
start_time = time.time()

# 调用API
response_message = AI.receive(messages)

print(response_message)

