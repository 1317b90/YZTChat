make_invoice=[
        {
            "type": "function",
            "function": {
                "name": "make_invoice",
                "description": "当你想开票时非常有用，注意：禁止暴露内部参数，空值请用空字符串''代替",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "buy_name": {
                            "type": "string",
                            "description": "购买方名称（发票抬头）"
                        },
                        "buy_id": {
                            "type": "string",
                            "description": "购买方社会统一代码或身份证号码",
                            #"default": ""
                        },
                        "buy_email": {
                            "type": "string",
                            "description": "购买方邮箱号",
                           # "default": ""
                        },
                        "buy_address": {
                            "type": "string",
                            "description": "购买方地址",
                            #"default": ""
                        },
                        "buy_phone": {
                            "type": "string",
                            "description": "购买方电话",
                            #"default": ""
                        },
                        "buy_bank_name": {
                            "type": "string",
                            "description": "购买方开户银行名称",
                            #"default": ""
                        },
                        "buy_bank_id": {
                            "type": "string",
                            "description": "购买方开户银行卡号",
                            #"default": ""
                        },
                        "invoice_type": {
                            "type": "string",
                            "description": "发票类型",
                            "enum": ["普通发票", "增值税专用发票"]
                        },
                        "invoice_name": {
                            "type": "string",
                            "description": "开票项目(商品名称)"
                        },
                        "invoice_amount": {
                            "type": "string",
                            "description": "金额",
                        },
                        "invoice_model": {
                            "type": "string",
                            "description": "规格",
                            #"default": ""
                        },
                        "invoice_unit": {
                            "type": "string",
                            "description": "单位",
                            #"default": ""
                        },
                        "invoice_num": {
                            "type": "string",
                            "description": "数量",
                            #"default": ""
                        },
                        "invoice_price": {
                            "type": "string",
                            "description": "单价",
                           # "default": ""
                        },
                        "invoice_code": {
                            "type": "string",
                            "description": "项目编码(商品编码)",
                           # "default": ""
                        },
                        "is_preview": {
                            "type": "boolean",
                            "description": "是否预览发票",
                            "default": "True"
                        }
                    },
                    "required": [
                        "buy_name",
                        "invoice_type",
                        "invoice_name",
                        "invoice_amount",
                    ]
                }
            }
        },

    ]
main=make_invoice