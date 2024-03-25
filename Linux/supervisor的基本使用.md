[toc]

##### supervisor

- Supervisor 是基于 Python 的进程管理工具
- 当执行一些需要以守护进程方式执行的程序，比如一个后台任务，常用它来进程管理。
- Supervisor 还能友好的管理程序在命令行上输出的日志，可以将日志重定向到自定义的日志文件中

###### supervisord，服务守护进程

> supervisor 的服务器端称为 supervisord，主要负责在启动自身时 启动所管理的子进程，响应客户端的命令，并在所管理的子进程出现崩溃时自动重启。

###### supervisorctl，命令行客户端

> 用户可以连接到 supervisord 服务器进程，获得子进程的状态，可以执行 stop、start、restart 等命令，来对这些子进程进行管理。

###### 安装supervisor

-  apt install supervisor 或 pip install supervisor

- 创建配置文件

  > sudo echo_supervisord_conf > /etc/supervisor/supervisord.conf

- 修改配置文件

  > vim supervisord.conf 
  >
  > [include] 
  >
  > files = /etc/supervisor/conf.d/*.conf  
  >
  > 
  >
  > [inet_http_server] 
  >
  > port=0.0.0.0:9001 
  >
  > username=user 
  >
  > password=123
  >
  > 
  >
  > *支持通过浏览器来管理进程，端口 9001*
  >
  > *使用 include，跟 Nginx 一样的，可以 include 某个文件夹下的所有配置文件，可以为每个进程单独写一个配置文件。*

- 启动 supervisord

  - 指定配置文件

    > supervisord -c /etc/supervisor/supervisord.conf

  - 启动 supervisord

    > sudo service supervisor start 
    >
    > sudo service supervisor status

###### 创建进程

- ubuntu 在 /etc/supervisor/conf.d/ 下 **.conf** 文件

- 进程的样例：

  ```shell
  [program:online-shop]
  # 程序的启动目录
  directory = /home/python/Desktop/online-store/myshop
  environment = PYTHONPATH=/home/python/.virtualenvs/online-store/bin
  user = root
  command = /home/python/.virtualenvs/online-store/bin/python /home/python/Desktop/online-store/myshop/manage.py runserver --insecure 0.0.0.0:8000
  
  # 在supervisord启动的时候也自动启动
  autostart = true
  # 启动5秒后没有异常退出,就当作已经正常启动了
  startsecs = 5 
  # 程序异常退出后自动重启
  autorestart = true
  # 启动失败自动重试次数，默认是 3
  startretries = 3 
  # 把stderr重定向到stdout，默认false,是否将程序错误信息重定向的到文件
  redirect_stderr = true
  # 程序错误信息输出到该文件
  stderr_logfile = /var/log/online-shop.log
  ```

###### supervisor相关命令

- 查看supervisor服务是否正常运行
	```
	sudo supervisorctl
	```
- 关闭supervisor则执行命令
	```
	sudo supervisorctl shutdown
	```
- 重载supervisor

  > sudo supervisorctl reload

- 更新supervisor

  > sudo supervisorctl update

- 查看状态

  > sudo supervisorctl status

- 启动所有/指定的程序进程

  > sudo supervisorctl start all / aa
- 启动某个supervisor进程
	```
	sudo supervisorctl start xxxx
	```
- 重启某个supervisor进程
	```
	sudo supervisorctl restart xxxx
	```
- 停止某个supervisor进程
	```
	sudo supervisorctl stop xxxx
	```
- 停止所有supervisor进程
	```
	sudo supervisorctl stop all
	```