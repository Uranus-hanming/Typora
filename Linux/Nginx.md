[toc]

##### 生成免费 SSL 证书

1. 安装 OpenSSL

2. 生成私钥

   ```
   openssl genrsa -out mydomain.key 2048
   ```

3. 创建证书签名请求(CSR)

   ```
   openssl req -new -key mydomain.key -out mydomain.csr
   ```

4. 生成自签名证书

   ```
   openssl x509 -req -days 365 -in mydomain.csr -signkey mydomain.key -out mydomain.crt
   ```

5. 验证证书

   ```
   openssl x509 -noout -text -in mydomain.crt
   openssl rsa -noout -check -in mydomain.key
   ```



##### Ngin配置

```nginx
worker_processes 1;

events { worker_connections 1024; }

http {
    sendfile on;
    client_max_body_size 100M;
    upstream app_servers {
        server web:xxx;  # 后端容器中服务启动的端口
    }
	
    # 这个服务不起作用，目前不知道啥原因？
    server {
	listen 80;
	server_name _;  # _ 允许所有主机名，适合测试

        return 301 https://$host$request_uri;
    }

    server {
	charset utf-8;
	listen 443 ssl;  # 监听 443 端口，并使用 SSL
	server_name _;  # 你的域名

	ssl_certificate "/etc/nginx/mydomain.crt";  # SSL 证书路径
	ssl_certificate_key "/etc/nginx/mydomain.key";  # SSL 私钥路径
	
    # 配置代理
	location / {
            proxy_pass http://app_servers;  # 代理到 Django 应用的地址和端口
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}

# 使用自签名证书：如果你控制服务器，并且确实在使用自签名证书，你需要告诉 requests 库接受这个证书。可以通过传递 verify=False 到 requests.post 来实现
# response = requests.post('https://xxx', data=data, verify=False)
```

