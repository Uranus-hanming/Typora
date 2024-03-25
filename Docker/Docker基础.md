[toc]

### Docker 容器使用

##### Docker 客户端：docker

##### Docker 命令使用方法：**docker command（具體命令） --help**

##### 获取镜像：docker pull ubuntu

###### 重命名容器：docker rename CONTAINER CONTAINER_NEW

######  将容器保存为新的镜像

```
docker commit Nginx zwx/nginx
```

##### 启动容器：docker run -it ubuntu /bin/bash

- **-i**: 交互式操作。
- **-t**: 终端。
- **ubuntu**: ubuntu 镜像。
- **/bin/bash**：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 /bin/bash。
- 要退出终端，直接输入 **exit**:

##### 啟動nginx容器：*docker run -d -p 80:80 nginx*

> -d 放入後台
>
> -p 端口映射

##### 后台运行容器：docker run -itd --name ubuntu-test ubuntu /bin/bash

##### 查看所有的容器：docker ps [OPTIONS]

- OPTIONS说明：

  ```
  -a :显示所有的容器，包括未运行的。
  -f :根据条件过滤显示的内容。
  --format :指定返回值的模板文件。
  -l :显示最近创建的容器。
  -n :列出最近创建的n个容器。
  --no-trunc :不截断输出。
  -q :静默模式，只显示容器编号。
  -s :显示总的文件大小。
  ```

- 输出详情介绍：

  - **CONTAINER ID**: 容器 ID。
  - **IMAGE**: 使用的镜像。
  - **COMMAND**: 启动容器时运行的命令。
  - **CREATED**: 容器的创建时间。
  - **STATUS**: 容器状态。
    - created（已创建）
    - restarting（重启中）
    - running（运行中）
    - removing（迁移中）
    - paused（暂停）
    - exited（停止）
    - dead（死亡）

  - **PORTS:** 容器的端口信息和使用的连接类型（tcp\udp）。
  - **NAMES:** 自动分配的容器名称。

- 列出最近创建的5个容器信息。

  ```
  sudo docker ps -n 5
  ```

- 列出所有创建的容器ID。

  ```
  sudo docker ps -aq
  ```

##### 使用 docker start 启动一个已停止的容器：docker start b750bbbcfd88 

##### 停止一个容器：docker stop <容器 ID>

##### 停止的容器可以通过 docker restart 重启：docker restart <容器 ID>

##### 进入容器：docker attach / **docker exec**：推荐大家使用 docker exec 命令，因为此退出容器（exit）终端，不会导致容器的停止。

```shell
# 在容器 mynginx 中以交互模式执行容器内 /root/runoob.sh 脚本:
docker exec -it mynginx /bin/sh /root/runoob.sh

# 在容器 mynginx 中开启一个交互模式的终端:
docker exec -i -t  mynginx /bin/bash

# 通过 exec 命令对指定的容器执行 bash:
sudo docker exec -it 9df70f9a0714 /bin/bash
sudo docker exec -it 9df70f9a0714 sh
```

##### 删除容器：sudo docker rm -f 1e560fca3906

##### 刪除所有容器 sudo docker rm $(sudo docker ps -a -q)

##### **docker inspect :** 获取容器/镜像的元数据

```
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

OPTIONS说明：

- **-f :**指定返回值的模板文件。
- **-s :**显示总的文件大小。
- **--type :**为指定类型返回JSON。

### Docker 镜像使用

##### 列出镜像列表：**docker images**

- **REPOSITORY：**表示镜像的仓库源
- **TAG：**镜像的标签
- **IMAGE ID：**镜像ID
- **CREATED：**镜像创建时间
- **SIZE：**镜像大小

##### 获取一个新的镜像：docker pull 

```shell
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
OPTIONS说明：
-a :拉取所有 tagged 镜像
--disable-content-trust :忽略镜像的校验,默认开启
```

##### 查找镜像：docker search

##### 拖取镜像：docker pull 

##### 删除镜像： **docker rmi** （刪除鏡像之前要把鏡像對應生成的容器刪除？）

##### 刪除所有鏡像：sudo docker rmi $(sudo docker images -q)

##### **docker save :** 将指定镜像保存成 tar 归档文件

```shell
docker save [OPTIONS] IMAGE [IMAGE...]
```

##### 導出鏡像：*docker image save IMAGE > [IMAGE...]*

```shell
docker image save centos > docker-centos-image.tar.gz
```

##### 導入鏡像：**docker load** 

```
docker load [OPTIONS]
```

OPTIONS 说明：

- **--input , -i :** 指定导入的文件，代替 STDIN。
- **--quiet , -q :** 精简输出信息。

###### 启动镜像服务

```dockerfile
docker run -dit \

--name=Registry \    # 指定容器名称

-p 5000:5000 \      # 仓库默认端口是5000，映射到宿主机，这样可以使用宿主机地址访问

--restart=always \                # 自动重启，这样每次docker重启后仓库容器也会自动启动

--privileged=true \              # 增加安全权限，一般可不加

-v /usr/local/my_registry:/var/lib/registry  \    # 把仓库镜像数据保存到宿主机

registry
```

### Dockerfile创建镜像 – Dockerfile格式

##### FROM //指定基于哪个基础镜像（docker images 所列出的images）

```shell
# Name the node stage "builder"
FROM node:12 AS builder
```

##### RUN //镜像操作指令（用来指定使用的命令）

```shell
格式为 RUN <command>  或者 RUN [“executable”, “param1”, “param2”]，比如
 RUN  yum install  httpd
 RUN ["/bin/bash", "-c", "echo hello"]
```

##### WORKDIR

> 格式 WORKDIR /path/to/workdir
> 为后续的RUN、CMD或者ENTRYPOINT指定工作目录

##### MAINTAINER 指定维护者信息，可以没有

##### ADD 格式 add <src> <dest>将本地的一个文件或目录拷贝到容器的某个目录里。 其中src为Dockerfile所在目录的相对路径，它也可以是一个url。

```shell
ADD <conf/vhosts> </usr/local/nginx/conf>
 ADD http://www.asd.com/1.txt /usr/local/src  //指定网络下载
```

##### COPY 格式同add,使用方法和add一样，不同的是, !! 它不支持url !!

##### CMD CMD用来指定容器!!启动时!!用到的命令，!!只能有一条!! 

```shell
# 三種格式
CMD ["executable", "param1", "param2"]
 CMD command param1 param2
 CMD ["param1", "param2"]
```

##### ENV //环境变量格式 ENV <key> <value>

> #### 主要是为后续的RUN指令提供一个环境变量，我们也可以定义一些自定义的变量: ENV MYSQL_version 5.6

##### USER 

> 格式 USER daemon
> 指定运行容器的用户

##### VOLUME

> 格式 VOLUME ["/data"]
> 创建一个可以从本地主机或其他容器挂载的挂载点。

##### ENTRYPOINT 格式类似CMD,容器启动时要执行的命令，它和CMD很像，也是只有一条生效，如果写多个只有最后一条有效。

> #### 和CMD不同是：CMD 是可以被 docker run 指令覆盖的，而ENTRYPOINT不能覆盖。

##### EXPOSE 格式为 EXPOSE <port> [<port>...]

> #### 这个用来指定要映射出去的端口，比如容器内部我们启动了sshd和nginx，所以我们需要把22和80端口暴漏出去。这个需要配合-P（大写）来工作，也就是说在启动容器时，需要加上-P，让它自动分配。如果想指定具体的端口，也可以使用-p（小写）来指定。

##### docker build 命令用于根据给定的Dockerfile和上下文以构建Docker镜像。

- **docker build [OPTIONS] <PATH | URL | ->**

  > 常用OPTIONS选项说明
  > --build-arg，设置构建时的环境变量
  > --no-cache，默认false。设置该选项，将不使用Build Cache构建镜像
  > --pull，默认false。设置该选项，总是尝试pull镜像的最新版本
  > --compress，默认false。设置该选项，将使用gzip压缩构建的上下文
  > --disable-content-trust，默认true。设置该选项，将对镜像进行验证
  > --file, -f，Dockerfile的完整路径，默认值为‘PATH/Dockerfile’
  > --isolation，默认--isolation="default"，即Linux命名空间；其他还有process或hyperv
  > --label，为生成的镜像设置metadata
  > --squash，默认false。设置该选项，将新构建出的多个层压缩为一个新层，但是将无法在多个镜像之间共享新层；设置该选项，实际上是创建了新image，同时保留原有image。
  > --tag, -t，镜像的名字及tag，通常name:tag或者name格式；可以在一次构建中为一个镜像设置多个tag
  > --network，默认default。设置该选项，Set the networking mode for the RUN instructions during build
  > --quiet, -q ，默认false。设置该选项，Suppress the build output and print image ID on success
  > --force-rm，默认false。设置该选项，总是删除掉中间环节的容器
  > --rm，默认--rm=true，即整个构建过程成功后删除中间环节的容器

  >  PATH | URL | -说明
  >  给出命令执行的上下文。
  >  上下文可以是构建执行所在的本地路径PATH，也可以是远程URL，如Git库、tarball或文本文件等，还可以是-。
  >  构建镜像的进程中，可以通过ADD命令将上下文中的任何文件（注意文件必须在上下文中）加入到镜像中。
  >
  >  可以是PATH，如本地当前PATH为.
  >
  >  如果是Git库，如https://github.com/docker/rootfs.git#container:docker，则隐含先执行git clone --depth 1 --recursive，到本地临时目录；然后再将该临时目录发送给构建进程。
  >
  >  -表示通过STDIN给出Dockerfile或上下文。

##### docker load 從一個存儲文件或一個標準輸入流中加載一個鏡像。

```shell
docker load [OPTIONS]
```

- -i ： --input string ：读取一个tar文件，取代标准输入
  `docker load -i ${filePath}`
- -q ： --quiet ：简化输出信息
  `docker load -q`

##### tar zcvf dir.tar.gz ./dir 压缩后的文件解压出来会是dir这个文件夹

##### **chmod** 是Linux下设置文件权限的命令，后面的数字表示不同用户或用户组的权限。

> 一般是三个数字：
>
> 第一个数字表示文件所有者的权限
>
> 第二个数字表示与文件所有者同属一个用户组的其他用户的权限
>
> 第三个数字表示其它用户组的权限。
>
> 权限分为三种：读（r=4），写（w=2），执行（x=1）。综合起来还有可读可执行（rx=5=4+1）、可读可写（rw=6=4+2）、可读可写可执行(rwx=7=4+2+1)。
>
> 所以，**chmod 755** 设置用户的权限为：
>
> 1.文件所有者可读可写可执行
>
> 2.与文件所有者同属一个用户组的其他用户可读可执行
>
> 3.其它用户组可读可执行

##### chown 将指定文件的拥有者改为指定的用户或组

```
chown [选项]... [所有者][:[组]] 文件...
```

> **必要参数:**
>
> 　　　　-c 显示更改的部分的信息
>
> 　　　　-f 忽略错误信息
>
> 　　　　-h 修复符号链接
>
> 　　　　-R 处理指定目录以及其子目录下的所有文件
>
> 　　　　-v 显示详细的处理信息
>
> 　　　　-deference 作用于符号链接的指向，而不是链接文件本身

###### MAINTAINER 维护者信息

###### EXPOSE 内部服务端口

### Docker Compose 配置文件 Docker-Compose.yml 文件详解

> Docker Compose是一个用来定义和运行复杂应用的Docker工具。一个使用Docker容器的应用，通常由多个容器组成。使用Docker Compose不再需要使用shell脚本来启动容器。 
> Compose 通过一个配置文件来管理多个Docker容器，在配置文件中，所有的容器通过services来定义，然后使用docker-compose脚本来启动，停止和重启应用，和应用中的服务以及所有依赖服务的容器，非常适合组合使用多个容器进行开发的场景。

##### image 指定服务的镜像名称或镜像 ID。如果镜像在本地不存在，Compose 将会尝试拉取这个镜像。

##### services 具體服務，可有多個

##### build

> 服务除了可以基于指定的镜像，还可以基于一份 Dockerfile，在使用 up 启动之时执行构建任务，这个构建标签就是 build，它可以指定 Dockerfile 所在文件夹的路徑。Compose 将会利用它自动构建这个镜像，然后使用这个镜像启动服务容器。

##### environment

> 设置镜像变量，它可以保存变量到镜像里面，也就是说启动的容器也会包含这些变量设置.
>
> environment 和 Dockerfile 中的 ENV 指令一样会把变量一直保存在镜像、容器中，类似 docker run -e 的效果。

##### expose:指定为镜像名称或镜像ID。如果镜像不存在，Compose将尝试从互联网拉取这个镜像

##### ports 映射端口的标签。

> HOST:CONTAINER宿主机器端口：容器端口。

##### command 覆盖容器启动后默认执行的命令

##### links:链接到其他服务容器，使用服务名称(同时作为别名)或服务别名（SERVICE:ALIAS）都可以

##### volumes 挂载一个目录或者一个已存在的数据卷容器

> 可以直接使用 [HOST:CONTAINER] 这样的格式，或者使用 [HOST:CONTAINER:ro] 这样的格式，后者对于容器来说，数据卷是只读的，这样可以有效保护宿主机的文件系统。

##### echo命令的功能是在显示器上显示一段文字，一般起到一个提示的作用。

> 此外，也可以直接在文件中写入要写的内容。也可以用于脚本编程时显示某一个变量的值，或者直接输出指定的字符串。

##### depends_on 解决容器的依赖、启动先后（依賴先啟動）的问题。

##### restart 指定容器退出后的重启策略为始终重启。

> 该命令对保持服务始终运行十分有效，在生产环境中推荐配置为 always 或者 unless-stopped。

##### 使用Compose構建並運行您的應用程序

```shell
docker-compose up
後台運行：docker-compose up -d
使用別名：docker-compose -f server.yml up -d
```

##### dns 配置 DNS 服务器。可以是一个值，也可以是一个列表。

### 使用Dockerfile構建鏡像並運行

1. 編寫Dcokerfile

2. 使用Dockerfile構建鏡像

   ```shell
   # 侯建tomcat鏡像，名稱為mytomcat,版本v1
   sudo docker build -t mytomcat:v1 .
   ```

3. 運行鏡像

   ```shell
   sudo docker run -p 8091:8091 --name hm_tomcat mytomcat:v1
   ```

### docker安装

- 更新程序 
	```
	sudo apt update
	```
- 安装依赖 
	```
	sudo apt install apt-transport-https ca-certificates curl software-properties-common
	```
- 添加Dokcer官方密钥到系统中 
	```
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	
	//添加中国科技大学的 Docker-ce 源，其中$(lsb_release -cs)返回Ubuntu发行版的名称：
	curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu \
	$(lsb_release -cs) stable"
	```
- 添加Docker源 
	```
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
	```
- 更新一下源 
	```
	sudo apt update
	```
- 查看可以安装的docker版本 
	```
	apt-cache policy docker-ce
	```
- 开始安装 
	```
	docker sudo apt install docker-ce
	```
- 测试 
	```
	docker --version     
	sudo docker run hello-world
	```

### 卸載docker

1. 卸载Docker Engine，CLI和Containerd软件包

```shell
sudo apt-get purge docker-ce docker-ce-cli containerd.io
```

2. 刪除數據

   > 主机上的映像，容器，卷或自定义配置文件不会自动删除。要删除所有图像，容器和卷。您必须手动删除所有已编辑的配置文件。

```shell
sudo rm -rf /var/lib/docker
```

### docker基本命令

- 停止docker服务

  ```shell
  sudo systemctl stop docker
  ```

- 重启docker服务

  ```shell
  sudo systemctl start docker
  ```

- 查看docker基本信息

  ```shell
  docker info
  ```

- 复制文件到容器

  ```
  docker cp custom.conf Nginx:/etc/nginx/conf.d/
  ```

- 更新容器启动项

  ```
  docker container update --restart=always nginx
  ```

- 查看docker日志

  ```
  tail -f /var/log/messages
  ```

- 注册https协议（需要通过本地仓库下载镜像，均需要配置）

  ```
  vim /etc/docker/daemon.json        # 默认无此文件，需自行添加，有则追加一下内容。
  
     { "insecure-registries":[" xx.xx.xx.xx:5000"] }  # 指定ip地址或域名
  ```

- 新增tag指明仓库地址

  ```
  docker tag zwx/nginx x.xx.xx.xx:5000/zwx/nginx  # 如果构建时已经指定仓库地址，则可以省略
  ```

- 上传镜像到本地仓库

  ```
  docker push x.xx.xx.xx:5000/zwx/nginx
  ```

- 查看本地仓库

  ```
  curl -XGET http://x.xx.xx.xx:5000/v2/_catalog
  ```



##### docker 数据存放配置

- 默认docker的数据存放位置为：/var/lib/docker

- 命令查看具体位置

  ```shell
  docker info | grep "Docker Root Dir"
  ```

- 停止docker服务

  ```shell
  sudo systemctl stop docker
  ```

- 移动整个/var/lib/docker目录到目的路径：

  ```shell
  # /root/data/docker 是挂载好的磁盘
  sudo mv /var/lib/docker /root/data/docker
  
  # 软连接指向
  sudo ln -s /root/data/docker /var/lib/docker
  ```

- 重新启动docker

  ```shell
  sudo systemctl start docker
  ```

- 查看路径是否已经配置好

  ```shell
  docker info | grep "Docker Root Dir"
  ```

- 查看docker版本号

  ```
  sudo docker version
  ```

- 查看docker-compose版本号

  ```
  sudo docker-compose version
  ```


- docker查看错误日志

  ```
  sudo docker logs id
  
  # -f: 让 docker logs 像使用 tail -f 一样来输出容器内部的标准输出。
  docker logs -f ID
  ```

- sudo docker kill id

- 单独启动容器

  ```
  sudo docker run -it name /bin/bash
  ```