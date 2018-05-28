#### 实名认证接口
#### request请求
    get /user/auths/

#### response
##### 成功响应
    {
        "code": 200,
        "id_name": xxx,
        'id_card': 1234562345342554323
    }


#### request请求
    put /user/auths/
##### params参数：
    real_name str 真实姓名
    id_card str 身份证号

#### response响应

##### 失败响应1：
    {
        "code": 900,
        "msg": "参数错误"
    }

##### 失败响应2：
    {
        "code": 1008,
        "msg": "身份证格式错误"
    }

##### 成功响应：
    {
        "code": 200,
        "msg": 请求成功
    }

