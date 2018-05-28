#### 修改信息接口
#### request请求
    put /user/user/
##### params参数：
    avatar file 头像
    name str 用户名


#### response响应

##### 失败响应1：
    {
        "code": 900,
        "msg": "参数错误"
    }

##### 失败响应2：
    {
        "code": 1006,
        "msg": "上传图片格式错误"
    }

##### 失败响应3：
    {
        "code": 1007,
        "msg": "用户名已存在"
    }

##### 成功响应1：
    {
        "code": 200,

    }

##### 成功响应2：
    {
        "code": 200,
        "url": /static/unload/1.png
    }