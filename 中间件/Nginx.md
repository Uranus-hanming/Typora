[toc]

###### 启动nginx

- 直接双击nginx.exe，双击后一个黑色的弹窗一闪而过
- 打开cmd命令窗口，切换到nginx解压目录下，输入命令 nginx.exe 或者 start nginx ，回车即可

###### 修改配置文件nginx.conf

- 执行命令 **nginx -s reload** 即可让改动生效

###### 关闭nginx

- 在cmd中输入nginx命令**nginx -s stop**(快速停止nginx)  或 **nginx -s quit**(完整有序的停止nginx)
- 进入nginx安装目录，使用**taskkill  taskkill /f /t /im nginx.exe**

###### nginx部署访问静态资源

```
自定义server配置：
    server {
		listen			9000;
		server_name		resouce;
		# 这里需要写相对路径  绝对路径会报错404
		root 			../resouce/ebook;# 相对于你nginx安装目录的路径
		autoindex 		on;
		location / {
			# 支持跨域
			add_header Access-Control-Allow-Origin *;
		}
		# 不存缓存 每次重新验证
		add_header Cache-Control "no-cache,must-revalidate";
    }
```

###### 使用nginx代理服务器做负载均衡

> 修改nginx的配置文件nginx.conf 达到访问nginx代理服务器时跳转到指定服务器的目的，即通过proxy_pass 配置请求转发地址，即当我们依然输入http://localhost:80 时，请求会跳转到我们配置的服务器

```
server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            proxy_pass http://tomacat_server;
        }
upstream tomcat_servert{
	server localhost:8080;
}

# 可以配置多个目标服务器，当一台服务器出现故障时，nginx能将请求自动转向另一台服务器:当服务器 localhost:8080 挂掉时，nginxnginx能将请求自动转向服务器 192.168.101.9:8080 。上面还加了一个weight属性，此属性表示各服务器被访问到的权重，weight越高被访问到的几率越高。
upstream tomcat_servert{
	server localhost:8080 weight=2;
	server 192.168.101.9:8080 weight=1;
}
```

###### nginx基础命令

- nginx -t 检查我们的配置文件是否有问题
- start nginx//启动nginx服务。 
- nginx -s stop // 停止nginx
- nginx -s reload // 重新加载配置文件
- nginx -s quit // 退出nginx