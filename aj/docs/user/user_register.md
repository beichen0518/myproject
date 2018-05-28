### 注册接口
#### request请求
    post /user/register/
##### params参数：
    mobile str 电话
    password str 密码
    password2 str 确认密码


#### response响应

##### 失败响应1：
    {
        "code": 900,
        "msg": "参数错误"
    }

##### 失败响应2：
    {
        "code": 1002,
        "msg": "手机号码已注册"
    }

##### 失败响应3：
    {
        "code": 1003,
        "msg": "两次密码不一致"
    }

##### 失败响应4：
    {
        "code": 1001,
        "msg": "手机号码不符合规则"
    }

##### 成功响应：
    {
        "code": 200,
        "msg": "请求成功"
    }