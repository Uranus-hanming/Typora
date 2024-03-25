[toc]

> **如何解决http无状态？	采用token**

# token - 令牌

## 学前须知：

### 1，base64 '防君子不防小人' 

| 方法              | 作用                                                  | 参数                                           | 返回值                                                    |
| ----------------- | ----------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------- |
| b64encode         | 将输入的参数转化为base64规则的串                      | 预加密的明文，类型为bytes；例：b‘guoxiaonao’   | base64对应编码的密文，类型为bytes；例:b'Z3VveGlhb25hbw==' |
| b64decode         | 将base64串 解密回 明文                                | base64密文,类型为bytes;例：b'Z3VveGlhb25hbw==' | 参数对应的明文，类型为bytes；例：b'guoxiaonao'            |
| urlsafe_b64encode | 作用同b64encode,但是会将 '+'替换成 '-',将'/'替换成'_' | 同b64encode                                    | 同b64encode                                               |
| urlsafe_b64decode | 作用同b64decode                                       | 同b64decode                                    | 同b64decode                                               |

代码演示:

```python
import base64
#base64加密
s = b'guoxiaonao'
b_s = base64.b64encode(s)
#b_s打印结果为 b'Z3VveGlhb25hbw=='

bas64.b64encode(b'guoxiaonao')

#base64解密
ss = base64.b64decode(b_s)
#ss打印结果为 b'guoxiaonao'

```

### 2，SHA-256  安全散列算法的一种（hash）

	hash三大特点：
	
	1）定长输出    2）不可逆    3） 雪崩

```python
import hashlib
s = hashlib.sha256() #创建sha256对象
s.update(b'xxxx')  #添加欲hash的内容，类型为 bytes
s.digest()  #获取最终结果,二进制
s.hexdigest() #16进制

```

### 3，HMAC-SHA256
是一种通过特别计算方式之后产生的消息认证码，使用**散列算法**同时结合一个**加密密钥**。它可以用来保证数据的完整性，同时可以用来作某个消息的身份验证

```python
import hmac
#生成hmac对象
#第一个参数为加密的key，bytes类型，
#第二个参数为欲加密的串，bytes类型
#第三个参数为hmac的算法，指定为SHA256
h = hmac.new(key, str, digestmod='SHA256 ') 
h.digest() #获取最终结果
```

### 4，RSA256 非对称加密

		1，加密： 公钥加密，私钥解密
	
		2，签名： 私钥签名， 公钥验签

## 2.1 JWT -  json-web-token  

### 1，三大组成

	1，header
	
		格式为字典-元数据格式如下

```python
{'alg':'HS256', 'typ':'JWT'}
#alg代表要使用的 算法
#typ表明该token的类别 - 此处必须为 大写的 JWT
```

		 该部分数据需要转成json串并用base64 加密



	2，payload
	
		格式为字典-此部分分为公有声明和私有声明
	
	  公共声明：JWT提供了内置关键字用于描述常见的问题

此部分均为**可选项**，用户根据自己需求 按需添加key，常见公共声明如下：

```python
{'exp':xxx, # Expiration Time 此token的过期时间的时间戳
 'iss':xxx，# (Issuer) Claim 指明此token的签发者
 'aud':xxx, #(Audience) Claim 指明此token的
 'iat':xxx, # (Issued At) Claim 指明此创建时间的时间戳
 'aud':xxx, # (Audience) Claim	指明此token签发面向群体
}
```

		私有声明：用户可根据自己业务需求，添加自定义的key，例如如下：

```python
{'username': 'guoxiaonao'}
```

		公共声明和私有声明均在同一个字典中；转成json串并用base64加密
	
	3，signature 签名
	
		签名规则如下：
	
		根据header中的alg确定 具体算法，以下用 HS256为例
	
		HS256(自定义的key ,   base64后的header + '.' + base64后的payload)
	
	    解释：用自定义的key, 对base64后的header + '.' + base64后的payload进行hmac计算

### 2，jwt结果格式

		base64(header) + '.' + base64(payload) + '.' +  base64(sign)
	
		最终结果如下： b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1b3hpYW9uYW8iLCJpc3MiOiJnZ2cifQ.Zzg1u55DCBqPRGf9z3-NAn4kbA-MJN83SxyLFfc5mmM'

### 3，校验jwt规则

		1，解析header, 确认alg
	
		2，签名校验 - 根据传过来的header和payload按 alg指明的算法进行签名，将签名结果和传过来的sign进行对比，若对比一致，则校验通过
	
		3，获取payload自定义内容
### 4，pyjwt 

	1，安装 pip3 install pyjwt

| 方法                            | 参数说明                                                     | 返回值                                        |
| ------------------------------- | ------------------------------------------------------------ | --------------------------------------------- |
| encode(payload, key, algorithm) | payload:  jwt三大组成中的payload,需要组成字典，按需添加公有声明和私有声明<br />例如: {'username': 'guoxiaonao', 'exp': 1562475112}<br />参数类型： dict | token串<br />返回类型：bytes                  |
|                                 | key : 自定义的加密key<br />参数类型：str                     |                                               |
|                                 | algorithm:  需要使用的加密算法[HS256, RSA256等] <br />参数类型：str |                                               |
| decode(token,key,algorithm,)    | token:   token串<br />参数类型： bytes/str                   | payload明文<br />返回类型：dict               |
|                                 | key : 自定义的加密key ,需要跟encode中的key保持一致<br />参数类型：str |                                               |
|                                 | algorithm:  同encode                                         |                                               |
|                                 | issuer:  发布者，若encode payload中添加 'iss' 字段，则可针对该字段校验<br />参数类型：str | 若iss校验失败，则抛出jwt.InvalidIssuerError   |
|                                 | audience：签发的受众群体，若encode payload中添加'aud'字段，则可针对该字段校验<br />参数类型：str | 若aud校验失败，则抛出jwt.InvalidAudienceError |

**PS**:  若encode得时候 payload中添加了exp字段; 则exp字段得值需为 当前时间戳+此token得有效期时间， 例如希望token 300秒后过期  {'exp': time.time() + 300};  在执行decode时，若检查到exp字段，且token过期，则抛出jwt.ExpiredSignatureError
```
In [1]: import jwt                                                              

In [2]: jwt.encode({'username':'uranus'},'123456',algorithm='HS256')            
Out[2]: b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVyYW51cyJ9.ic1HwcFawjLIa9QUyaJm348kl58WocTUfaf5IrtkiCc'

In [3]: s=jwt.encode({'username':'uranus'},'123456',algorithm='HS256')          

In [5]: jwt.decode(s,'123456',algorithms='HS256')                               
Out[5]: {'username': 'uranus'}

In [6]: import time                                                             

In [7]: s=jwt.encode({'username':'uranus','exp':time.time()+60},'123456',algorit
   ...: hm='HS256')                                                             

In [8]: jwt.decode(s,'123456',algorithms='HS256')                               
Out[8]: {'username': 'uranus', 'exp': 1586569539.474536}
```