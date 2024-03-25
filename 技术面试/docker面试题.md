[toc]
##### 镜像

- 把应用程序和配置依赖打包成一个可交付的运行环境，包含运行某个软件所需的所有内容
- 通过镜像文件才能生成docker容器实例
- docker镜像层是只读的，docker容器层是可写的
- 新镜像是在base镜像一层一层叠加生成的
- 虚悬镜像：仓库名和标签都是<none>，清理镜像：docker image prune
- docker images [-qa]
- docker search image_name
- docker pull image_name
- docker push 
- docker rmi ID
- docker rmi -r $(docker images -qa)
- docker system df
- docker tag old_imange new_image
- 查看镜像详细信息：docker inspect image
- 查看镜像历史：docker history image

###### 1. 创建镜像

1. 基于已有容器：docker commit -m "xxx" 容器ID 仓库名：标签
2. 基于本地模板导入：docker import     /     docker load -i/< xxx.tar
3. 基于dockerfile 创建：docker build

###### 2. Unions（联合文件系统）

- 是一种分层、轻量级并且高性能的文件系统
- 支持对文件系统的修改作为一次提交来一层层叠加
- 联合文件系统是docker镜像的基础

##### 容器

- docker run
- docker ps [-qa]
- docker start
- docker stop
- docker rm $(docker ps -qa)
- docker logs
- docker top
- docker stats
- 查看容器内部详细信息：docker inspect container
- 进入容器操作：docker exec -it container_ID /bin/bash
- 文件复制：docker cp
- 导入导出tar文件：docker export
- 查看端口映射：docker port 

 ##### 容器数据卷

- -v：启动容器时挂载数据卷

  ```
  docker run -it --privileged=true -v /宿主机绝对路径目录:/容器内目录:[rw/ro] 镜像名
  ```

###### docker volume

- docker volume create
- docker [volume] inspect 
- docker volume ls
- docker volume prune
- docker volume rm
- 数据卷容器：--volumes-from

##### dockerfile

> 用来创建docker镜像的文本文件；
>
> 是由一条条构建镜像所需的指令和参数构成的脚本。

###### 1. 基本结构

1. 基础镜像信息
2. 维护者信息
3. 镜像操作指令
4. 容器启动时执行指令

###### 2. 镜像操作指令关键字

- FROM：指定创建镜像的基础镜像
- RUN：在当前镜像基础上执行命令，并提交为新的镜像层
- USER：指定镜像的执行用户，默认root
- WIRKDIR：配置工作目录
- ENV：指定环境变量
- COPY：复制文件到镜像
- CMD：启动容器时默认执行的命令

##### docker网络

- docker network ls
- 创建docker网络：docker network name
- docker network inspect name
- docker network prune
- docker network rm

###### 1. 常见网络模式

1. bridge桥接模式：将容器与docker0连接，默认
2. host模式：使用宿主机的ip和port
3. container容器模式：和指定容器共享ip/port
4. none

##### docker-compose

> 可以同时管理多个容器，实现对docker容器集群的快速编排；
>
> YAML格式的配置文件

###### 1. docker-compose.yml配置文件主要命令

- image： 指定镜像
- build：指定dockerfile所在文件夹的路径
- port：暴露端口信息
- environment：设置环境变量
- depends_on：配置依赖关系
- volumes：配置数据卷挂载
- command：覆盖容器启动后默认执行的命令

###### 2. docker-compose主要命令

- docker-compose build：构建项目中的服务容器
- docker-compose config：查看配置文件的配置信息
- docker-compose down：停止服务栈
- docker-compose images：列出服务所创建的镜像
- docker-compose kill：强制停止服务器
- docker-compose port：打印某个容器端口所映射的公共端口
- docker-compose ps：列出项目中目前的所有容器
- docker-compose pull：拉取服务依赖的进行
- docker-compose push：推送镜像到仓库
- docker-compose rm：删除所有（停止状态的）服务容器
- docker-compose run：在指定服务上执行一个命令
- docker-compose start 启动已经存在的服务容器
- docker-compose stop：停止已经处于运行状态的容器
- docker-compose top：显示服务栈中正在运行的进程信息
- docker-compose version：打印版本信息
- docker-compose up：完成一系列操作：构建镜像、创建服务、启动服务，关联服务等