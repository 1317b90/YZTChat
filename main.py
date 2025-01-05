from fastapi import FastAPI,Body,HTTPException
from fastapi.middleware.cors import CORSMiddleware

import models
from invoice import main as make_invoice_main




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
    return {"code": 500, "msg": str(exc)}



@app.post("/receive")
def receive_message(M: models.Message = Body(...)):
    if M.type == "make_invoice":
        M.reply_message = make_invoice_main(M)
    else:
        raise HTTPException(status_code=400, detail="任务类型错误")
    return {"message":M.reply_message}
 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
