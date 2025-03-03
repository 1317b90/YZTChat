from fastapi import FastAPI,Body,HTTPException,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import traceback
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
    print(f"请求信息: {request}")
    print(f"错误信息: {str(exc)}")
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
            tool_content=""
            try:
                # 解析参数
                arguments=json.loads(tool_call.function.arguments)

                none_content=""
                # 如果是开票
                if tool_call.function.name=="make_invoice":
                    arguments = models.Invoice(**arguments)
                    invoice.create_task(arguments,M)
                    # 假如AI没有生成回复，使用下面这句作为回复
                    none_content="正在执行开票中，请您稍等..."

                # 如果是取消开票
                elif tool_call.function.name=="cancel_invoice":
                    tool_content=tell.cancel_invoice(arguments.get("taskid",""))
                    none_content=tool_content

                # 如果AI回复漏了
                if not M.answer:
                    tool_content=none_content

            # 如果出错了
            except Exception as e:
                # 打印详细报错
                traceback.print_exc()
                tool_content=str(e)

            finally:
                # 如果工具有返回值
                if tool_content:
                    print(tool_content)
                    M.messages.append(
                        {
                            "role": "tool",
                            "content": tool_content,
                            "tool_call_id": tool_call.id
                        }
                    )
                    M.answer=AI.receive(M.messages).content

    # 将聊天记录存储到数据库中(后台执行)
    background_tasks.add_task(tell.add_message,M.model_dump())
    return {"message":M.answer}


@app.get("/polish")
def polish_message(message:str):
    # 将待润色结果传入
    messages=[{
                "role": "tool",
                "content": message,
                "tool_call_id": ""
                    }]
    return {"message":AI.polish(messages)}

@app.post("/group")
def group_message(M: models.GroupMessage = Body(...)):
    try:
        # 补充习惯
        try:
            user_data=tell.get_user_data(M.userid)
            if "admin" in M.userid:
                userid=user_data["PuppetID"]
                user_data=tell.get_user_data(userid)

            M.message+=user_data["InvoiceHabit"]
        except Exception as e:
            print(f"习惯出错：{e}")

        result=AI.group(M.message)
        # 调用工具
        if result.tool_calls:
            for tool_call in result.tool_calls:
                none_content=""
                # 解析参数
                arguments=json.loads(tool_call.function.arguments)

                must_dict={
                    "buy_name": "发票抬头",
                    "invoice_type": "发票类型",
                    "invoice_name": "发票名称",
                    "invoice_amount": "发票金额"
                }

                # 检查必填项
                for key in must_dict.keys():
                    if arguments.get(key,"")=="":
                        none_content+=must_dict[key]+"，"

                if none_content:
                    return {"message":f"请将{none_content}补充完整"}

                arguments = models.Invoice(**arguments)
                # 是群聊消息
                arguments.is_group=True
                arguments.adminid=M.adminid
                invoice.create_task(arguments,M)

        return {"message":""}
    except Exception as e:
        # 打印详细报错
        traceback.print_exc()
        raise Exception(f"{str(e)}\n{str(M.model_dump())}")

# 一键提醒
@app.get("/remind")
def remind():
    users=tell.get_users()
    for user in users:
        tell.send_message("yzt_serviceid",user.get("UserID",""),"您好，麻烦导出上个月的银行回单和银行对账单，入账需要，谢谢配合")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
