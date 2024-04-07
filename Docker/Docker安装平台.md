[toc]

##### docker desktop配置国内源

> settings => Docker Engine

```
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com"
  ]
}

国内镜像源：
中国区官方镜像：https://registry.docker-cn.com
清华源：https://docker.mirrors.ustc.edu.cn
腾讯源：https://mirror.ccs.tencentyun.com
网易源：http://hub-mirror.c.163.com
```

##### linux环境中docker配置镜像加速

1. 编辑文件

   ```
   vim /etc/docker/daemon.json 
   ```

2. 添加镜像源

   ```
   {
       "registry-mirrors":[
           "https://kfwkfulq.mirror.aliyuncs.com",
           "https://2lqq34jg.mirror.aliyuncs.com",
           "https://pee6w651.mirror.aliyuncs.com",
           "https://1nj0zren.mirror.aliyuncs.com",
           "https://registry.docker-cn.com",
           "http://f1361db2.m.daocloud.io",
           "https://docker.mirrors.ustc.edu.cn",
           "http://hub-mirror.c.163.com",
           "https://mirror.ccs.tencentyun.com"
       ]
   }
   ```

3. 重启docker服务

   ```
   systemctl  daemon-reload     //重启镜像
   systemctl restart  docker.service
   ```

##### 安装redis

###### 1. 拉取镜像

```shell
docker pull redis:latest
```

###### 2. 创建redis配置文件，为挂载做准备

> 在D盘创建2个文件夹
> conf目录用于挂载配置文件
> data目录用于存放数据持久化文件

- 在conf文件夹新建redis.conf文件

  ```
  #用守护线程的方式启动 后台运行
  daemonize no 
  #给redis设置密码
  requirepass 123456 
  #redis持久化　　默认是no
  appendonly yes
  #防止出现远程主机强迫关闭了一个现有的连接的错误 默认是300
  tcp-keepalive 300 
  ```

###### 3. 构建并启动redis容器

> 映射到宿主16379端口

```shell
docker run --name redis -p 16379:6379 -v /D/docker/redis/conf/redis.conf:/etc/redis/redis_6379.conf -v /D/docker/redis/data:/data/ -d redis:latest redis-server /etc/redis/redis_6379.conf --appendonly yes
```

- name=“容器新名字”：为容器指定一个名称
- p: 指定端口映射，格式为：主机(宿主)端口:容器端口
- d: 后台运行容器，并返回容器ID
- v /D/docker/redis/conf/redis.conf:/etc/redis/redis_6379.conf 把宿主机配置好的redis.conf放到容器内的这个位置中
- v /D/docker/redis/data:/data/ 把redis持久化的数据在宿主机内显示，做数据备份
- net=host

##### 安装ubuntu:22.04

###### 1. 拉取镜像

```
docker pull ubuntu:22.04
```

###### 2. 运行容器

```shell
docker run -itd -p IP地址:外部端口:内部端口 --name 容器名字 镜像:标签 /bin/bash
 
注：
    外部端口是指Windows操作系统中的端口
    内部端口是指容器中的Ubuntu操作系统的端口
    这里是一个例子：
    docker run -itd -p 0.0.0.0:10000:22 --name myubuntu ubuntu:22.04 /bin/bash
    其中：
        0.0.0.0表示本地所有的Ip
        这里把windows系统中的10000端口映射到了ubuntu的22端口（ssh需要使用22端口）
```

###### 3. 进入容器终端配置

1. 切换bash脚本进行编辑

   ```
   bash
   ```

2. 更新

   ```
   apt update
   ```

3. 安装ssh服务

   - 下载ssh工具

     ```
     apt install openssh-server
     ```

   - 编辑ssh配置文件

     ```
     vim /etc/ssh/sshd_config
     
     需要进行以下四项的配置：
     PermitRootLogin yes #允许root使用ssh登录
     PubkeyAuthentication yes #启用公钥私钥配对认证方式
     AuthorizedKeysFile .ssh/authorized_keys # 此处的路径“.ssh/authorized_keys”以本地文件为准
     UsePAM no #不适用PAM
     ```

   - 启动ssh服务

     ```
     service ssh start
     ```

   - 配置开机启动

     ```
     service ssh ssh
     systemctl enable sshd ??
     ```

4. 安装vim

   ```
   apt install -y vim
   ```

##### 安装centos:8

###### 1. 拉取centos8镜像文件

```
docker pull centos
```

###### 2. 启动centos

```
#运行centos镜像 并把centos的22端口映射到本机的8022端口，做shh连接使用
#--privileged 付给容器root权限，不然系统级别的操作都搞不了
docker run -it -d --name=centos8 --privileged -p 8022:22 centos /usr/sbin/init
```

1. 配置appstream 仓库 镜像列表URL

   > centos官方停止了对centos8的维护，使用yum命令时候 会提示 appstream 镜像仓库没有url地址

   ```
   # 修改centos 设置url地址
   sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
   sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
   
   #更新Yum
   yum update -y
   ```

2. 安装vim

   ```
   yum install vim -y
   ```

3. 安装ssh服务

   - 检查有无安装ssh

     ```
     yum list installed | grep openssh-server
     ```

   - 安装密码和ssh服务

     ```
     yum install passwd openssh-server -y
     使用vim 查看 /etc/ssh/sshd_config 文件
     ```

   - 启动sshd

     ```
     systemctl start sshd
     ```

   - 配置开机启动

     ```
     systemctl enable sshd
     ```

   - 配置密码  需要确认两次 且密码不可见

     ```
     passwd
     ```

##### 安装mysql5.7

###### 1. 拉取mysql5.7镜像

```
# 默认下载MySQL5.7最新版本(其他版本可以指定比如 docker pull mysql:5.7.34)
docker pull mysql:5.7
```

###### 2. 启动容器

- 方式一 (快捷方式,仅配置root密码)

```shell
docker run --name mysql5.7 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
```

- 方式二 (配置容器MySQL数据、配置、日志挂载宿主机目录)

```
# 宿主机创建数据存放目录映射到容器
mkdir -p /usr/local/docker_data/mysql/data

# 宿主机创建配置文件目录映射到容器 
mkdir -p /usr/local/docker_data/mysql/conf #(需要在此目录下创建"conf.d"、"mysql.conf.d"两个目录)
mkdir -p /usr/local/docker_data/mysql/conf/conf.d # (建议在此目录创建my.cnf文件并进行相关MySQL配置)
mkdir -p /usr/local/docker_data/mysql/conf/mysql.conf.d

# 宿主机创建日志目录映射到容器
mkdir -p /usr/local/docker_data/mysql/logs

docker run --privileged=true --name mysql5.7 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d  -v /usr/local/docker_data/mysql/data:/var/lib/mysql -v /usr/local/docker_data/mysql/conf:/etc/mysql/ -v /usr/local/docker_data/mysql/logs:/var/log/mysql mysql:5.7
```

- 参数说明

  | 参数                                                | 说明                                      |
  | --------------------------------------------------- | ----------------------------------------- |
  | –name mysql5.7                                      | 容器名称                                  |
  | -p 3306:3306                                        | 端口映射(宿主机端口:容器端口)             |
  | -e MYSQL_ROOT_PASSWORD=123456                       | 容器的环境变量(root账号初始化密码)        |
  | -d                                                  | 后台运行容器                              |
  | -v /usr/local/docker_data/mysql/data:/var/lib/mysql | 容器MySQL数据目录映射(宿主机:容器)        |
  | -v /usr/local/docker_data/mysql/conf:/etc/mysql/    | 容器MySQL配置目录映射(宿主机:容器)        |
  | -v /usr/local/docker_data/mysql/logs:/var/log/mysql | 容器MySQL日志目录映射(宿主机:容器)        |
  | mysql:5.7                                           | 指定docker镜像 (可以是镜像名称或者镜像ID) |

###### 3. 进入MySQL容器及创建账号

```sql
docker exec -it mysql5.7 bash
mysql -u root -p

# 创建用户并开启远程登录
CREATE USER '你的账号'@'%'  IDENTIFIED BY '你的密码';

# 创建数据库并设置字符集
CREATE DATABASE `库名` CHARACTER SET 'utf8mb4';

# 给账号授权数据库
GRANT ALL PRIVILEGES ON `库名`.* TO '你的账号'@'%';

# 给root用户分配权限：
alter user 'root'@'%' identified with mysql_native_password by '123456';

# 刷新权限
FLUSH PRIVILEGES;
```

##### 安装nginx

###### 1. 拉取nginx镜像

```
docker pull nginx
```

###### 2. 运行容器

```
docker run -d -p 80:8081 --name nginx nginx
```

##### 安装gitlab

###### 1. 搜索镜像

```
docker search gitlab
```

###### 2. 下载镜像

```
docker pull twang2218/gitlab-ce-zh
```

###### 3. 启动git镜像

```dockerfile
linux:
docker run -d -p 8443:443 -p 8090:80 -p 8022:22 --restart always --name gitlab -v /usr/local/gitlab/etc:/etc/gitlab -v /usr/local/gitlab/log:/var/log/gitlab -v /usr/local/gitlab/data:/var/opt/gitlab --privileged=true twang2218/gitlab-ce-zh

windows:
docker run -d -p 8443:443 -p 8090:80 -p 8023:22 --restart always --name gitlab -v D:\git\etc:/etc/gitlab -v D:\git\log:/var/log/gitlab -v D:\git\data:/var/opt/gitlab --privileged=true twang2218/gitlab-ce-zh
```

```
docker run 
-d                #后台运行，全称：detach
-p 8443:443      #将容器内部端口向外映射
-p 8090:80       #将容器内80端口映射至宿主机8090端口，这是访问gitlab的端口
-p 8022:22       #将容器内22端口映射至宿主机8022端口，这是访问ssh的端口
--restart always #容器自启动
--name gitlab    #设置容器名称为gitlab
-v /usr/local/gitlab/etc:/etc/gitlab    #将容器/etc/gitlab目录挂载到宿主机/usr/local/gitlab/etc目录下，若宿主机内此目录不存在将会自动创建
-v /usr/local/gitlab/log:/var/log/gitlab    #与上面一样
-v /usr/local/gitlab/data:/var/opt/gitlab   #与上面一样
--privileged=true         #让容器获取宿主机root权限
twang2218/gitlab-ce-zh    #镜像的名称，这里也可以写镜像ID
```

###### 4. 修改gitlab.rb文件

> 先进入到gitlab目录：
> cd /etc/gitlab
> 编辑gitlab.rb文件 ：
> vim gitlab.rb

```
# 修改ip
external_url 'http://xx.xx.xx.xx'

# 配置ssh协议所使用的访问地址和端口
gitlab_rails['gitlab_ssh_host'] = '192.168.XX.XX' //和上一个IP输入的一样
gitlab_rails['gitlab_shell_ssh_port'] = 8022 // 此端口是run时22端口映射的8022端口
```

###### 5. 修改gitlab.yml文件

```
# 文件路径 /opt/gitlab/embedded/service/gitlab-rails/config
# 先进入到config目录下
cd /opt/gitlab/embedded/service/gitlab-rails/config
# 打开编辑gitlab.yml文件
vim gitlab.yml
## GitLab settings
# 修改host 与上面.rb文件修改的一致
# 修改port 为8090
```

###### 6. 重启服务

```
gitlab-ctl restart
```

###### 7. 常用命令

```
//容器外停止
docker stop gitlab   // 这里的gitlab 就是我们上一步docker run 当中使用--name 配置的名字
//容器外重启
docker restart gitlab
//进入容器命令行
docker exec -it gitlab bash
//容器中应用配置，让修改后的配置生效
gitlab-ctl reconfigure
//容器中重启服务
gitlab-ctl restart
```

###### 8. windows生成公钥

```
ssh-keygen
公钥路径可默认，直接回车
进入.ssh目录： cd ~/.ssh
复制id_rsa.pub到gitlab配置SSH密钥
```

###### 9. 修改git ssh端口
```
在C盘用户目录下.gitconfig文件中添加配置信息：
[core]
    sshCommand = ssh -p 8024
```