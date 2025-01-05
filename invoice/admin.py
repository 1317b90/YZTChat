import tell

def puppet(sender:str,message:str):
    puppet_id=''.join(filter(str.isdigit, message))
    user_data=tell.get_user(puppet_id)
    if user_data:
        if tell.put_user({"Phone":sender,"PuppetID":puppet_id}):
            return f"""指代成功
🚹 {user_data["CompanyName"]}
🆔 {puppet_id}"""
        else:
            return "指代请求失败"
    else:
        return "指代用户不存在"