[toc]
# 4，RESTful -Representational State Transfer

## 4.1，什么是RESTful

	1，资源 **（Resources）**
	
		**网络上的一个实体，或者说是网络上的一个具体信息**，并且每个资源都有一个独一无二得URI与之对应；获取资源-直接访问URI即可
	
	2，**表现层（Representation）**
	
		如何去表现资源  - 即资源得表现形式；如HTML , xml  , JPG , json等
	
	3，**状态转化（State Transfer）**
	
		访问一个URI即发生了一次 客户端和服务端得交互；此次交互将会涉及到数据和状态得变化
	
		客户端需要通过某些方式触发具体得变化  -  HTTP method 如 GET， POST，PUT，PATCH，DELETE 等



## 4.2 RESTful的特征

	1，每一个URI代表一种资源
	
	2，客户端和服务器端之前传递着资源的某种表现
	
	3，客户端通过HTTP的几个动作 对 资源进行操作 - 发生‘状态转化’



## 4.3 如何设计符合RESTful 特征的API

	1，协议  - http/https
	
	2，域名：
	
		域名中体现出api字样，如
	
		https://api.example.com
	
		or
	
		https://example.org/api/
	
	3,  版本:
	
		https://api.example.com/v1/
	
	4，路径 -
	
		路径中避免使用动词，资源用名词表示，案例如下

```python
https://api.example.com/v1/users
https://api.example.com/v1/animals
```

	5，HTTP动词语义

- GET（SELECT）：从服务器取出资源（一项或多项）。

- POST（CREATE）：在服务器新建一个资源。

- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。

- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。

- DELETE（DELETE）：从服务器删除资源。

  具体案例如下：

  ```python
  GET /zoos：列出所有动物园
  POST /zoos：新建一个动物园
  GET /zoos/ID：获取某个指定动物园的信息
  PUT /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
  PATCH /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
  DELETE /zoos/ID：删除某个动物园
  GET /zoos/ID/animals：列出某个指定动物园的所有动物
  DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物
  ```

  

  	6，巧用查询字符串

  ```python
  ?limit=10：指定返回记录的数量
  ?offset=10：指定返回记录的开始位置。
  ?page=2&per_page=100：指定第几页，以及每页的记录数。
  ?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
  ?type_id=1：指定筛选条件
  ```

  ​	

  	7，状态码
  	
  		1，用HTTP响应码表达 此次请求结果，例如

  ```python
  200 OK - [GET]：服务器成功返回用户请求的数据
  201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
  202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
  204 NO CONTENT - [DELETE]：用户删除数据成功。
  400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
  401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
  403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
  404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
  406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
  410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
  422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
  500 INTERNAL SERVER ERROR - [*]：服务器发生错误
  ```

  		2, 自定义内部code 进行响应
  	
  	   10100 - 10199 user应用
  	
  		如 返回结构如下  {'code':200,  'data': {}, 'error': ''}

  

  	8，返回结果
  	
  	根据HTTP 动作的不同，返回结果的结构也有所不同
  
  ```python
  GET /users：返回资源对象的列表（数组）
  GET /users/guoxiaonao：返回单个资源对象
  POST /users：返回新生成的资源对象
  PUT /users/guoxiaonao：返回完整的资源对象
  PATCH /users/guoxiaonao：返回完整的资源对象
  DELETE /users/guoxiaonao：返回一个空文档
  ```