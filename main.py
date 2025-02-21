from fastapi import FastAPI,Body,HTTPException,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

import models
import admin
import AI
import invoice
import json
import tell

app=FastAPI()

# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


# 设置报错信息（不设置该函数，程序报错会自动终止）
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return {"code": 500, "message": str(exc)}



@app.post("/receive")
def receive_message(background_tasks: BackgroundTasks,M: models.Message = Body(...)):
    if "admin" in M.userid:
        new_message=M.messages[-1]["content"]
        if "指代" in new_message:
            return {"message":admin.puppet(M.userid,new_message)}

    memory=tell.get_memory(M.userid)
    result=AI.receive(M.messages,memory=memory)
    M.answer=result.content

    # 调用工具
    if result.tool_calls:
        for tool_call in result.tool_calls:
            if tool_call.function.name=="make_invoice":
                try:
                    arguments=json.loads(tool_call.function.arguments)
                    arguments["userid"]=M.userid
                    arguments["serviceid"]=M.serviceid
                    # 创建开票任务
                    create_result=tell.create_make_invoice(arguments)
                except Exception as e:
                    create_result=f"创建开票任务的时候失败：{e}"
     
                # 如果创建失败
                if create_result !=True:
                    M.messages.append(
                        {
                            "role": "tool",
                            "content": create_result,
                            "tool_call_id": tool_call.id
                        }
                    )
                    create_result=AI.receive(M.messages)
                    M.answer=create_result.content
    
    # 将聊天记录存储到数据库中(后台执行)
    background_tasks.add_task(tell.add_message,M.model_dump())
    return {"message":M.answer}


@app.post("/polish")
def polish_message(M: models.MessageWeak = Body(...)):
    # 获取数据库中历史消息
    messages=tell.get_message(M.userid)
    # 将待润色结果传入
    messages.append({"role":"user","content":M.message})

    result=AI.polish(messages)
    return {"message":result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
