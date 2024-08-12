[toc]

#### Docker学习

> 一切在云端，万物皆容器。
>
> 天上飞的理念，必然有落地的实现。
>
> 凡技术，必登官网。

##### 如何学习一门新理论

1. 是什么？
2. 能干嘛？
   - 我为什么要学？
   - 解决了哪些问题？
   - 有什么好处？解决了哪些痛点？
3. 去哪下载和安装？
4. 怎么玩？
5. 永远的hello world跑起来一次

###### AB法则

1. before
2. after

###### 三板斧

1. 理论
2. 实操
3. 小总结

##### 帮助启动类命令

- 启动docker：systemctl start docker
- 停止docker：systemctl stop docker
- 重启docker：systemctl restart docker
- 查看docker状态：systemctl status docker
- 开机启动：systemctl enable docker
- 查看docker概要信息：docker info
- 查看docker总体帮助文档：docker --help
- 查看docker命令帮助文档：docker具体命令 --help

##### 镜像命令(docker image help)

> 是一种轻量级、可执行的独立软件包，它包含运行某个软件所需的所有内容，我们把应用程序和配置依赖打包好形成一个可交付的运行环境（包括代码、运行时所需要的库、环境变量和配置文件等），这个打包好的运行环境就是image镜像文件。
>
> 只有通过这个镜像文件才能生成Docker容器实例。
>
> docker镜像层都是只读的，容器层是可写的。
>
> 当容器启动时，一个新的可写层被加载到镜像的顶部。这一层通常被称作“容器层”，“容器层”之下的都叫“镜像层”
>
> 所有对容器的改动 - 无论添加、删除、还是修改文件都只会发生在容器层中。只有容器层是可写的，容器层下面的所有镜像层都是只读的。
>
> docker中的镜像分层，支持通过扩展现有镜像，创建新的镜像。新镜像是从base镜像一层一层叠加生成的。每安装一个软件，就在现有镜像的基础上增加一层。

> 同一个仓库源有多个TAG版本，代表这个仓库源的不同个版本；我们使用REPOSITORY:TAG来定义不同的镜像。
>
> 谈谈docker的虚悬镜像：***仓库名、标签***都是\<none>的镜像，俗称虚悬镜像（dangling image）

| :REPOSITORY    | :TAG             | :IMAGE ID | :CREATED     | :SIZE    |
| -------------- | ---------------- | --------- | ------------ | -------- |
| 表示镜像的仓库 | 镜像的标签版本号 | 镜像ID    | 镜像创建时间 | 镜像大小 |

1. 列出本地主机上的镜像：docker images

   - -a：列出本地所有的镜像（含历史镜像层）

   - -q：只显示镜像ID

   - 显示全部镜像的ID

     ```
     docker iamges -qa
     ```

2. 查看仓库中的镜像：docker search image_name

   - --limit n：只列出N个镜像，默认25个

     ```
     docker search --limit 5 redis
     ```

3. 从仓库拉取镜像：docker pull [OPTIONS] 镜像名字[:TAG]

   > docker pull 镜像名字：没有TAG默认最新版，等价于（docker pull 镜像名字:latest）

   | NAME     | DESCRIPTION | STARS    | OFFICIAL     | AUTOMATED        |
   | -------- | ----------- | -------- | ------------ | ---------------- |
   | 镜像名称 | 镜像说明    | 点赞数量 | 是否是官方的 | 是否是自动构建的 |
   - 从指定的仓库服务器下载
   		```
   		docker pull registry.hub.docker.com/ubuntu:18.04
   		docker pull hub.c.163.com/public/ubuntu:18.04
   		```
	- 使用镜像代理服务来加速docker镜像获取过程
		```
		在docker服务启动配置中增加 --registry-mirror=proxy_URL来指定镜像代理服务地址
		如：https://registry.docker-cn.com
		```

4. 查看镜像/容器/数据卷所占的空间：docker system df

5. 删除镜像：docker rmi 某个XXX镜像名字/ID

   - 删除多个

     ```
     docker rmi -f 镜像名1:TAG 镜像名2:TAG
     ```

   - 删除全部

     ```
     docker rmi -r $(docker images -qa)
     ```


   - -f(force)：强制删除

     ```
     docker rmi -f redis
     ```
6. 使用tag命令添加镜像标签
	```
	docker tag ubunt:latest myubuntu:latest
	```
7. 使用inspect命令查看详细信息
	```
	docker [image] inspect ubuntu:18.04
	```
8. 使用history命令查看镜像历史
	```
	# 列出各层的创建信息
	docker history ubuntu:18.04
	```
9. 搜寻镜像
	```
	docker search [option] keyword
	-f , --fil 七er fil 七er : 过滤输出内容； 、
	--forma 七S 七r ing: 格式化输出内容；
	--limit i n七： 限制输出结果个数，默认为25 个；
	- -no - 七runc: 不截断输出结果。
	```
10. 清理镜像
	```
	使用Docker 一段时间后，系统中可能会遗留一些临时的镜像文件，以及一些没有被使
	用的镜像，可以通过docker image prune 命令来进行清理。
	-a, -all : 删除所有无用镜像，不光是临时镜像；
	-fil 七er fil 七er: 只清理符合给定过滤器的镜像；
	-f, -force: 强制删除镜像，而不进行提示确认。
	```

###### 创建镜像
1. 基于已有容器创建
	```
	docker [container] commi [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
	-a, --au止or="": 作者信息； 、
	-c, - - change=[] : 提交的时候执行Dockerfile 指令，包括CMDIENTRYPOINTIE
	NVIEXPOSEILABELIONBUILDIUSERIVOLUMEIWORKDIR 等；
	-m, - -message= 11 11: 提交消息；
	-p, - -pause= 七rue: 提交时暂停容器运行。
	
	docker run -it ubuntu:18.04 /bin/bash
	记住容器的ID
	docker [container] commit -m "added a new file" -a "myname" a925cb40b3f0 test:latest
	```
2. 基于本地模板导入
	```
	docker [image] import [OPTIONS] file|URL| - [REPOSITORY [:TAG]]
	```
3. 基于dockerfile创建
	```
	docker build [OPTIONS] PATH | URL | -
	docker build -t REPOSITORY[:TAG] /dockerfile_path
	```
###### 存出和载入镜像
1. 存出镜像
	```
	docker save [image] -o name.tar
	```
2. 载入镜像
	```
	将导出的tar文件再导入到本地镜像库
	docker [image] load
	
	docker load -i ubuntu_18.04.tar
	docker load < ubuntu_18.04.tar
	```
###### 上传镜像
	```
	docker [image] push NAME[:TAG] | [REGISTRY_HOST[:REGISTRY_PORT]/] NAME[:TAG]
	```
1. 注册账号
	```
	https://hub.docker.com/
	```
2. 创建存储库
3. 编辑Dockerfile文件
	```
	vim Dockerfile
	# 输入以下内容：
	FROM REPOSITORY:TAG
	```
4. 打包镜像
	```
	docker build -t username/FROM REPOSITORY:TAG .
	或
	docker tag REPOSITORY username/REPOSITORY
	```
5. 登录镜像仓库
	```
	docker login --username=xxx
	```
6. 上传镜像
	```
	docker push username/REPOSITORY:TAG
	```

###### UnionFS(联合文件系统)

> 是一种分层、轻量级并且高性能的文件系统，它支持对文件系统的修改作为一次提交来一层层的叠加，同时可以将不同目录挂载到同一个虚拟文件系统。
>
> Union文件系统是docker镜像的基础。
>
> 镜像可以通过分层来进行继承，基于基础镜像（没有父镜像），可以制作各种具体的应用镜像。

- 特性：一次同时加载多个文件系统，但从外面看起来，只能看到一个文件系统，联合加载会把各层文件系统叠加起来，这样最终的文件系统会包含所有底层的文件和目录。

- docker镜像加载原理

  > bootfs(boot file system)主要包含bootloade和kernel，bootloader主要是引导加载kernel，linux刚启动时会加载bootfs文件系统，在docker镜像的最底层是引导文件系统的bootfs。这一层与我们典型的linux/unix系统是一样的，包含boot加载器和内核。当boot加载完成之后整个内核就都在内存中了，此时内存的使用权已由bootfs转交给内核，此时系统也会卸载bootfs。
  >
  > rootfs(root file system)，在bootfs之上，包含的就是典型的linux系统中的/dev./proc./bin./etc等标准目录和文件。rootfs就是各种不同的操作系统发行版，比如ubuntu,centos等。
  >
  > 对于一个精简的OS，rootfs可以很小，只需要包含最基本的命令、工具和程序库就可以了，因为底层直接用host的kernel，自己只需要提供rootfs就行了。

###### 虚悬镜像

> ***仓库名、标签***都是\<none>的镜像，俗称虚悬镜像（dangling image）

- 查询所有的虚悬镜像

  ```
  docker image ls -f dangling=true
  docker images -f dangling=true
  ```

- 删除虚悬镜像

  ```
  docker image prune
  ```

##### 容器命令(docker container help)

1. 从面向对象角度

   > docker利用容器（container）独立运行一个或一组应用，应用程序或服务运行在容器里面，容器就类似于一个虚拟化的运行环境，***容器是用镜像创建的运行实例***。镜像是静态的定义，容器是镜像运行时的实体。容器为镜像提供了一个标准的和隔离的运行环境，它可以启动、开始、停止、删除。每个容器都是相互隔离的、保证安全的平台。

2. 从镜像容器角度

   > ***可以把容器看做是一个简易版的linux环境***（包括root用户权限、进程空间、用户空间和网络空间等）和运行在其中的应用程序。

3. 容器调试

   ```
   docker run -it --entrypoint /bin/bash bf9a44845a0c
   ```

###### 创建容器(docker create)
> 使用docker create 命令新建的容器处于停止状态，可以使用docker [container] start命令来启动它。
> 选项：与容器运行模式相关、与容器环境配置相关、与容器资源限制和安全保护相关。

###### 启动容器(docker start)
> docker start 用来启动一个已经创建的容器。

###### 新建并启动容器(docker run)
- docker在后台运行的标准操作：
	- 检查本地是否存在指定的镜像，不存在就从公有仓库下载；
	- 利用镜像创建一个容器，并启动该容器；
	- 分配一个文件系统给容器，并在只读的镜像层外面挂载一层可读可写；
	- 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去；
	- 从网桥的地址池配置一个IP地址给容器；
	- 执行用户指定的应用程序；
	- 执行完毕后容器被自动终止；
```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

- 启动交互式容器（前台命令行）

  ```
  docker run -it ubuntu /bin/bash
  ```

- OPTIONS说明：有些是一个减号，有些是两个减号

  - --name="容器新名字"：为容器指定一个名称；

  - -d：后台运行容器并返回容器ID，也即启动守护式容器（后台运行）

  - -i：以交互模式运行容器，通常与-t同时使用，i(interactive 互动的)；

  - -t：为容器重新分配一个伪输入终端，通常与-i同时使用，也即启动交互式容器（前台有伪终端，等待交互）t(tty)；

  - -P：随机端口映射，大写P

  - -p：指定端口映射，小写p(port)

    | :参数                         | :说明                              |
    | ----------------------------- | ---------------------------------- |
    | -p hostport:containerport     | 端口映射：-p 8080:80               |
    | -p ip:hostport:containerport  | 配置监听地址：-p 127.0.0.1:8080:80 |
    | -p ip::containerport          | 随机分配端口 -p 127.0.0.1::80      |
    | -p hostport:containerport:udp | 指定协议 -p 8080:80:tcp            |
    | -p 81:80 -p 443:443           | 指定多个                           |
- 更多的命令选项通过man docker-run命令查看。
- 守护态（Daemonized）形式运行
	```
	docker run -d ubuntu /bin/bash
	```

###### 列出当前所有正在运行的容器(docker ps)

```
docker ps [OPTIONS]
```

- -a：列出当前所有正在运行的容器+历史上运行过的

- -l：显示最近创建的容器

- -n：显示最近n个创建的容器

  ```
  docker ps -n 2
  ```

- -q：静默模式，只显示容器编号

###### 退出容器(exit)

1. exit：run进去容器，exit退出，容器停止
2. ctrl+p+q：run进去容器退出，容器不停止

###### 启动已停止运行的容器(docker start)

```
docker start 容器ID或容器名
```

###### 重启容器(docker restart)

```
docker restart 容器ID或容器名
```

###### 停止容器(docker stop)

```
docker stop 容器ID或容器名
```

###### 强制停止容器(docker kill)

```
docker kill 容器ID或容器名
```

###### 删除已停止的容器(docker rm)

```
docker rm 容器ID
docker rm --help
```

- 一次性删除多个容器实例
  - docker rm -f $(docker ps -qa)
  - docker ps -a -q | xargs docker rm

###### 重要的容器命令

- 有镜像才能创建容器，这是根本前提

- 启动守护式容器（后台服务器 -d）

  > docker 容器后台运行，必须有一个前台进程
  >
  > 容器运行的命令如果不是那些一直挂起的命令（比如运行top,tail），就会自动退出。
  >
  > 解决方案：将你要运行的程序以前台进程的形式运行，常见就是命令行模式
  >
  > 如：docker run -it ubuntu

  ```
  docker run -d 容器名
  -d：指定容器的后台运行模式
  建议使用docker ps查看是否成功运行
  ```

  - redis前后台启动演示
    - 前台交互式启动：docker run -it redis:6.0.8
    - 后台守护式启动：docker run -d redis:6.0.8

- 查看容器日志(docker logs)

  ```
  docker logs [OPTIONS] CONTAINER
  docker logs --help
  ```


- 查看容器内运行的进程(docker top)

  ```
  docker top CONTAINER [ps OPTIONS]
  docker top --help
  ```

- 查看统计信息
	```
	docker stats --help
	docker stats [OPTIONS] [CONTAINER...]
	```

- 查看容器内部细节(docker inspect)

  ```
  docker inspect [OPTIONS] NAME|ID [NAME|ID...]
  ```

- 进入正在运行的容器并以命令行交互(docker exec -it)

  > 推荐使用docker exec命令，因为推出容器终端，不会导致容器的停止。

  - docker exec -it 容器ID bashShell

    ```
	docker [container] exec [-d l - - detach] [--detach-ke y s[=[] ]] [- i l --interactive]
	[--privileged] [ - ti -- 七ty] [ - ul --user[=USER]] CONTAINER COMMAND [ARG . . . ]
	docker exec --help
	
    docker run -it ubuntu /bin/bash
    ```
    - -d, --detach: 在容器中后台执行命令；
    - --de 七ach-keys="": 指定将容器切回后台的按键；
    - -e, - - env= [ l : 指定环境变蜇列表；
    - -i, --interactive= 七rue I false : 打开标准输入接受用户输入命令，默认值为false;
    - --privileged=trueifalse: 是否给执行命令以高权限，默认值为f_alse;
    - -t， --tty=tru eifalse: 分配伪终端，默认值为false ;
    - -u, --user="": 执行命令的用户名或ID 。

  - 重新进入：docker attach 容器ID

  - exec和attach的区别

    1. attach直接进入容器启动命令的终端，不会启动新的进程；用exit退出，会导致容器的停止；
    2. exec是在容器中打开新的终端，并且可以启动新的进程；用exit退出，不会导致容器的停止。

- 从容器内拷贝文件到主机上(cp)

  ```
  docker cp 容器ID：容器内路径 目的主机路径
  docker cp containerID:/usr/local/mycptest/container.txt /tmp/c.txt
  ```

- 将本机的路径data复制到test容器的/tmp路径下：
	```
	docker cp 目的主机路径 容器ID：容器内路径
	```

- 导入和导出容器

  - export: 导出容器的内容流作为一个tar归档文件[对应import命令]

    ```
    docker export --help
    docker export -o filename.tar container_ID
    docker export container_ID > filename.tar
    ```

  - import: 从tar包中的内容创建一个新的文件系统再导入为镜像[对应export]

    ```
    docker import --help
    docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
    cat filename.tar | docker import - 镜像用户/镜像名:镜像版本号
    ```

- 查看变更(docker diff)
	```
	docker diff CONTAINER
	docker diff --help
	```
- 查看端口映射(docker port)
	```
	docker port CONTAINER [PRIVATE_PORT[/PROTO]]
	docker port --help
	```
- 更新配置
	```
	可以更新容器的一些运行时配置，主要是一些资源限制份额。
	docker update [OPTIONS] CONTAINER [CONTAINER...]
	docker update --help
	```


##### 命令图解

![在这里插入图片描述](https://img-blog.csdnimg.cn/e6526b8cc2a047a88b5dc020048b26e8.jpeg#pic_center)




- attach: 当前shell 下attch连接指定运行镜像
- build: 通过Dockerfile定制镜像
- commit: 提交当前容器为新的镜像
- cp: 从容器中拷贝指定文件或者目录到宿主机中
- create: 创建一个新的容器，同run，但不启动容器
- diff: 查看docker容器变化
- events: 从docker服务获取容器实时事件
- exec: 在已存在的容器上运行命令
- export: 导出容器的内容流作为一个tar归档文件[对应import]
- history: 展示一个镜像形成历史
- images: 列出系统当前镜像
- import: 从tar包中的内容创建一个新的文件系统映像[对应export]
- info: 显示系统相关信息
- inspect: 查看容器详细信息
- kill: kill指定docker容器
- load: 从一个tar包中加载一个镜像[对应save]
- login: 注册或者登陆一个docker源服务器
- logout: 从当前Docker registry退出
- logs: 输出当前容器日志信息
- port: 查看映射端口对应的容器内部源端口
- pause: 暂停容器
- ps: 列出容器列表
- pull: 从docker镜像源服务器拉取指定镜像或者库镜像
- push: 推送指定镜像或者库镜像值docker源服务器
- restart: 重启运行的容器
- rm: 移除一个或者多个容器
- rmi: 移除一个或多个镜像（无容器使用该镜像才可删除，否则需删除相关容器才可继续或-f强制删除）
- run: 创建一个新的容器并运行一个命令
- save: 保存一个镜像为一个tar包[对应load]
- search: 在docker hub中搜索镜像
- start: 启动容器
- stop: 停止容器
- tag：给源中镜像打标签
- top: 查看容器中运行的进程信息
- unpause: 取消暂停容器
- version: 查看docker版本号
- wait: 截取容器停止时的退出状态值

##### commit命令

> docker commit 提交容器副本使之成为一个新的镜像

```
docker commit -m="提交的描述信息" -a="作者" 容器ID 要创建的目标镜像名：[标签名]
docker commit -m="add vim cmd" -a="vim_tess" 5fa45c3697b hanming/my_ubuntu:1.1
```

##### 访问docker仓库
###### docker hub 公共镜像市场 
- 登录
	```
	docker login
	本地用户目录下会自动创建.docker/config.json文件，保存用户的认证信息。
	```
- 自动创建（可以自动跟随项目代码的变更而重新构建镜像）
	1. 创建并登录Docker Hub, 以及目标网站如Github;
	2. 在目标网站中允许Docker Hub 访问服务；
	3. 在Docker Hub 中配置一个“自动创建“类型的项目；
	4. 选取一个目标网站中的项目（ 需要含Dockerfile ) 和分支；
	5. 指定Dockerfile 的位置，并提交创建。

###### 本地镜像发布到阿里云

1. 创建镜像空间

   - 选择控制台，进入容器镜像服务

   - 选择个人实例

   - 命名空间

   - 仓库名称

   - 进入管理界面获取脚本

     ```
     从Registry中拉取镜像:
     docker pull registry.cn-shenzhen.aliyuncs.com/charles/mydocker:[镜像版本号]
     
     将镜像推送到Registry:
     $ docker login --username=xxx registry.cn-shenzhen.aliyuncs.com
     $ docker tag [ImageId] registry.cn-shenzhen.aliyuncs.com/charles/mydocker:[镜像版本号]
     $ docker push registry.cn-shenzhen.aliyuncs.com/charles/mydocker:[镜像版本号]
     ```

###### 搭建本地私有仓库
- 使用registry镜像创建私有仓库
	> 通过官方提供的registry镜像搭建本地私有仓库环境；

	```
	# 自动下载并启动一个registry容器，创建本地的私有仓库服务
	# 默认情况下，仓库会被创建在容器的/var/lib/registry目录下：
	docker run -d -p 5000:5000 registry:2
	# 通过-v参数来将镜像文件存放在本地的指定路径：如将镜像放到/opt/data/registry目录
	docker run -d -p 5000:5000 -v /opt/data/registry:/var/lib/registry registry:2
	```

- 下载镜像私有库：docker pull registry

	```
  docker run -d -p 5000:5000 -v /opt/data/registry:/var/lib/registry registry:2
  默认情况，仓库被创建在容器的/var/lib/registry目录下，建议自行用容器卷映射，方便与宿主机联调
  ```
  - 使用docker tag命令标记镜像
  	```
  	docker tag IMAGE [:TAG] [REGISTRYHOST/] [USERNAME/] NAME [:TAG]
  	docker tag ubuntu:18.04 localhost:5000/test
  	```
  - 使用docker push上传镜像
	```
	docker push localhost:5000/test
  ```
  - 重启docker服务，并从私有仓库中下载镜像到本地
	  ```
	  sudo service docker restart
	  docker pull localhost:5000/test
	  ```
  - 下载后，添加一个更通用的标签ubuntu:18.04，方便后续使用
    ```
    docker tag localhost:5000/test ubuntu:18.04
    ```

- 上传私服库

  ```
  docker commit -m="提交的描述信息" -a="作者" 容器ID 要创建的目标镜像名：[标签名]
  ```

- curl验证私服库上有什么镜像

  ```
  curl -XGET http://ip:port/v2/_catalog
  ```

- 将新镜像zzyyubuntu:1.2修改符合私服规范的TAG

  ```
   xxxxxxxxxx 使用命令 docker tag 将zzyyubuntu:1.2 这个镜像修改为IP:PORT/zzyyubuntu:1.2
  ```

- 修改配置文件使之支持http

  ```
  cat /etc/docker/daemon.jon
  添加："insecure-registries":["IP:PORT"]
  注意两个配置中间有个逗号","
  ```

- push推送到私服库

  ```
  docker push IP:PORT/zzyyubuntu:1.2
  ```

- curl验证私服库上有什么镜像

- pull到本地运行

  ```
  docker pull
  ```

##### 容器数据卷(docker volume --help)

> 卷就是目录或文件，存在于一个或多个容器中，有docker挂载到容器，但不属于联合文件系统，因此能够绕过Union File System提供一些用于持续存储或共享数据的特性。
>
> 卷的目的是***数据的持久化*** ，完全独立于容器的生存周期，因此docker不会在容器删除时删除其挂载的数据卷。

- 是什么？

  > 将docker容器内的数据保存进宿主机的磁盘中

  ```
  docker run -it --privileged=true -v /宿主机绝对路径目录:/容器内目录 镜像名
  ```

- 特点

  - 数据卷可在容器之间共享或重用数据
  - 卷中的更改可以直接实时生效
  - 数据卷中的更改不会包含在镜像的更新中
  - 数据卷的声明周期一直持续到没有容器使用它为止

- 容器卷ro和rw读写规则

  ```
  默认就是rw：
  docker run -it --privileged=true -v /宿主机绝对路径目录:/容器内目录:rw 镜像名
  rw:可读可写
  ro:只读read only
  容器实例内部被限制，只能读取不能写：
  docker run -it --privileged=true -v /宿主机绝对路径目录:/容器内目录:ro 镜像名
  ```
###### docker volume相关命令
- 查看详细信息：inspect
	```
	docker volume inspect [OPTIONS] VOLUME [VOLUME...]
	```
- 列出已有数据卷：ls
	```
	docker volume ls [OPTIONS]
	```
- 清理无用数据卷：prune
	```
	docker volume prune [OPTIONS]
	```
- 删除数据卷：rm
	```
	docker volume rm [OPTIONS] VOLUME [VOLUME...]
	```

###### 创建数据卷
```
docker volume --help
# 在/var/lib/docker/volumes路径下创建test容器卷
docker volume create -d local test
```

###### 绑定数据卷(docker run --mount)
> 在创建容器时将主机本地的任意路径挂载到容器内作为数据卷。
- 支持三种类型的数据卷：
	- volume:普通数据卷，映射到主机/var/lib/docker/volume路径下；
	- bind:绑定数据卷，映射到主机指定路径下；
		```
		# 本地目录的路径必须是绝对路径，容器内路径可以为相对路径，如果目录不存在，docker会自动创建。
		# 使用training/webapp镜像创建一个web容器，并创建一个数据卷挂载到容器的/opt/webapp目录
		docker run -d -p --name web --mount type=bind,source=/webapp,destination=/opt/webapp training/webapp python app.py
		# 等同于旧的-v标记：
		docker run -d -p --name web -v /webapp:/opt/webapp training/webapp python app.py
		# docker挂载数据卷的默认权限是读写(rw)，用户也可以通过ro指定为只读：
		docker run -d -p --name web -v /webapp:/opt/webapp:ro training/webapp python app.py
		```
	- tmpfs:临时数据卷，只存在于内存中；

###### 数据卷容器
 > 让用户在多个容器之间共享一些持续更新的数据；
 > 数据卷容器也是一个容器，但目的是专门提供数据卷给其他容器挂载；
1. 创建一个数据卷容器dbdata，并在其中创建一个数据卷挂载到/dbdata:
	```
	docker run -it -v /dbdata --name dbdata ubuntu
	```
2. 在其他容器中使用--volumes-from 来挂载dbdata容器中的数据卷
	```
	docker run -it --volumes-from dbdata --name db1 ubuntu
	docker run -it --volumes-from dbdata --name db2 ubuntu
	# 此时，容器db1和db2都挂载同一个数据卷到相同的/dbdata目录，三个容器任何一方在该目录下的写入，其他容器都可以看到。
	```
###### 利用数据卷容器来迁移数据
> 可以利用数据卷容器对其中的数据卷进行备份、恢复，以实现数据的迁移。
1. 备份
```
docker run --volumes-from dbdata -v $(pwd):/backup --name worker ubuntu tar cvf /backup/backup.tar /dbdata
```
- 首先利用ubuntu 镜像创建了一个容器worker。使用--volumes-from dbdata 参数来让worker 容器挂载dbdata 容器的数据卷（即dbdata 数据卷） ；使用-v $ (pwd) : /backup参数来挂载本地的当前目录到worker 容器的/ backup 目录。
- worker 容器启动后，使用tar cvf /backup/backup.tar /dbdata 命令将/dbdata下内容备份为容器内的/backup/backup.tar, 即宿主主机当前目录下的backup.tar 。
2. 恢复（恢复数据到一个容器）
- 首先创建一个带有数据卷的容器的容器dbdata2:
	```
	docker run -v /dbdata --name dbdata2 ubuntu /bin/bash
	```
- 然后创建另一个新的容器，挂载dbdata2的容器，并使用untar解压备份文件到所挂载的容器卷中
	```
	docker run --volumes-from dbdata2 -v $(pwd):/backup busybox tar xvf /backup/backup.tar
	```

###### 卷的继承和共享

- 容器1完成和宿主机的映射

  ```
  docker run -it --privileged=true -v /mydocker/u:/tmp/u --name u1 ubuntu /bin/bash
  ```

- 容器2继承容器1的卷规则

  ```
  docker run -it --privileged=true --volumes-from 父类 --name u2 ubuntu
  ```

##### dockerfile
> 是什么？dockerfile是用来构建docker镜像的文本文件，是由***一条条构建镜像所需的指令和参数***构成的脚本。
###### 基本结构
- dockerfile主题内容分为四部分：
	1. 基础镜像信息
	2. 维护者信息
	3. 镜像操作指令
	4. 容器启动时执行指令

###### 配置指令
| :指令       | :说明                              | :格式                                                        |
| ----------- | ---------------------------------- | ------------------------------------------------------------ |
| ARG         | 定义创建镜像过程中使用的变量       |                                                              |
| FROM        | 指定所创建镜像的基础镜像           | FROM \<image> [AS \<name>] 或 FROM \<image>:\<tag> [AS \<name>] |
| LABEL       | 为生成的镜像添加元数据标签信息     |                                                              |
| EXPOSE      | 声明镜像内服务监听的端口           |                                                              |
| ENV         | 指定环境变量                       | ENV \<key> \<value> 或 ENV \<key>=\<value> ...               |
| ENTRYPOINT  | 指定镜像的默认入口命令             |                                                              |
| VOLUME      | 创建一个数据卷挂载点               | VOLUME ["/data"]                                             |
| USER        | 指定运行容器时的用户名或UID        |                                                              |
| WORKDIR     | 配置工作目录                       | WORKDIR /path/to/workdir                                     |
| ONBUILD     | 创建子镜像时指定自动执行的操作指令 |                                                              |
| STOPSIGNAL  | 指定退出的信号值                   |                                                              |
| HEALTHCHECK | 配置所启动容器如何进行健康检查     |                                                              |
| SHELL       | 指定默认shell类型                  | SHELL ["executable", "parameters"]                           |

###### 操作指令
| :指令 | :说明                        | :格式                                                    | :补充                                                        |
| ----- | ---------------------------- | -------------------------------------------------------- | ------------------------------------------------------------ |
| RUN   | 运行指定命令                 | RUN \<command> 或 RUN ["executable", "param1", "param2"] | 每条RUN 指令将在当前镜像基础上执行指定命令，并提交为新的镜像层。当命令较长时可以使用＼来换行。 |
| CMD   | 启动容器时指定默认执行的命令 | CMD ["executable", "param1", "param2"]                   | 每个Dockerfile 只能有一条CMD 命令。如果指定了多条命令，只有最后一条会被执行。如果用户启动容器时候手动指定了运行的命令（作为run 命令的参数），则会覆盖掉CMD 指定的命令。 |
| ADD   | 添加内容到镜像               | ADD \<src> \<dest>                                       | 该命令将复制指定的<SrC> 路径下内容到容器中的< dest > 路径下。其中< SrC> 可以是Dockerfile 所在目录的一个相对路径（文件或目录）；也可以是一个URL；还可以是一个tar 文件（自动解压为目录） < des 户可以是镜像内绝对路径，或者相对千工作目录( WORKDIR ) 的相对路径。路径支持正则格式：ADD *.c /code/ |
| COPY  | 复制内容到镜像               | COPY \<src> \<dest>                                      | 复制本地主机的<SrC> (为Dockerfile 所在目录的相对路径，文件或目录）下内容到镜像中的< des 七＞ 。目标路径不存在时，会自动创建。路径同样支持正则格式。COPY 与ADD 指令功能类似，当使用本地目录为源目录时，推荐使用COPY 。 |

###### 创建镜像
```
docker build [OPTIONS] PATH | URL | -
```
> 该命令将读取指定路径下（包括子目录）的Dockerfile, 并将该路径下所有数据作为上下文(Context ) 发送给Docker 服务端。Docker 服务端在校验Dockerfile 格式通过后，逐条执行其中定义的指令，碰到ADD 、COPY 和RUN 指令会生成一层新的镜像。最终如果创建镜像成功，会返回最终镜像的ID 。
> 要指定生成镜像的标签信息，可以通过-t 选项。该选项可以重复使用多次为镜像一次添加多个名称。
> 例如， 上下文路径为/tmp/docker_builder/ , 并且希望生成镜像标签为b叫der/first_image: 1.0.0,可以使用下面的命令：
> $ docker build -t builder/ first_image:1. 0.0 / tmp/ docker_bui l der/

###### 命令选项
| 选项                     | 说明                                     |
| ------------------------ | ---------------------------------------- |
| --add-host list          | 添加自定义的主机名到IP 的映射            |
| --build-arg list         | 添加创建时的变量                         |
| --cache-from strings     | 使用指定锐像作为缓存源                   |
| --cgroup-parent string   | 继承的上层cgroup                         |
| --compress               | 使用gzi p 来压缩创建上下文数据           |
| --cpu-period int         | 分配的CFS 调度器时长                     |
| --cpu-quota int          | CFS 调度器总份额                         |
| -c, --cpu-shares int     | CPU 权重                                 |
| --cpuset-cpus string     | 多CPU 允许使用的CP U                     |
| --cpuset-mems string     | 多CPU 允许使用的内存                     |
| --disable-content-trust  | 不进行镜像校验， 默认为真                |
| -f, --file string        | Dockerfil e 名称                         |
| --force-rm               | 总是删除中间过程的容器                   |
| --iidfile string         | 将镜像ID 写入到文件                      |
| --isolation string       | 容器的隔离机制                           |
| --label list             | 配置镜像的元数据                         |
| -m, --memory bytes       | 限制使用内存证                           |
| --memory-swap bytes      | 限制内存和缓存的总屈                     |
| --network string         | 指定RUN 命令时的网络模式                 |
| --no-cache               | 创建镜像时不适用缓存                     |
| -o, --output stringArray |                                          |
| --platform string        | 指定平台类型                             |
| --progress string        |                                          |
| --pull                   | 总是尝试获取镜像的最新版本               |
| -q, --quiet              | 不打印创建过程中的日志信息               |
| --rm                     | 创建成功后自动删除中间过程容器，默认为真 |
| --secret stringArray     |                                          |
| --security-opt strings   | 指定安全相关的选项                       |
| --shm-size bytes         | /dev/shm 的大小                          |
| --squash                 | 将新创建的多层挤压放入到一层中           |
| --ssh stringArray        |                                          |
| --stream                 | 持续获取创建的上下文                     |
| -t, --tag list           | 指定镜像的标签列表                       |
| --target string          | 指定创建的目标阶段                       |
| --ulimit ulimit          | 指定ulimit 的配甡                        |

###### 构建三部曲

1. 编写dockerfile文件

2. docker build 命令构建镜像

   ```
   docker build -t 新镜像名字:TAG .
   注意：上面TAG后面有个空格，有个点.（这个点代表当前目录）
   ```

3. docker run 镜像运行容器实例

###### dockerfile构建过程解析

- dockerfile内容基础知识：

  > https://docs.docker.com/engine/reference/builder/

  - 每条保留字指令都必须为大写字母且后面要跟随至少一个参数；
  - 指令按从上到下，顺序执行；
  - \# 标志注释；
  - 每条指令都会创建一个新的镜像层并对镜像进行提交；

- docker执行dockerfile的大致流程：

  1. docker从基础镜像运行一个容器；
  2. 执行一条指令并对容器作出修改；
  3. 执行类似docker commit的操作提交一个新的镜像层；
  4. docker再基于刚提交的镜像运行一个新容器；
  5. 执行dockerfile中的下一条指令直到所有指令都执行完成；

###### dockerfile常用保留字指令

1. FROM

   > 基础镜像，当前新镜像是基于哪个镜像的，指定一个已经存在的镜像作为模板，第一条必须是FROM

2. MAINTAINER

   > 镜像维护者的姓名和邮箱地址

3. RUN

   - 容器构建时需要运行的命令

   - 两种格式

     - shell格式

       ```
       RUN <命令行命令>
       # <命令行命令> 等同于，在终端操作的shell 命令
       ```

     - exec格式

   - RUN是在docker build时运行

4. EXPOSE

   > 当前容器对外暴露出的端口

5. WORKDIR

   > 指定在创建容器后，终端默认登录进来的工作目录，一个落脚点

6. USER

   > 指定该镜像以什么样的用户去执行，如果都不指定，默认是root

7. ENV

   ```
   用来在构建镜像过程中设置环境变量

   ENV MY_PATH=/usr/mytest
   这个环境变量可以在后续的任何RUN指令中使用，这就如同在命令前面指定了环境变量前缀一样；
   也可以在其他指令中直接使用这些环境变量
   如：WORKDIR $MY_PATH
   ```

8. ADD

   > 将宿主机目录下的文件拷贝进镜像且会自动处理URL和解压tar压缩包
   >
   > 注意：文件必须要和Dockerfile文件在同一位置。

9. COPY

   > 类似ADD，拷贝文件和目录到镜像中。
   >
   > 将从侯建上下文目录中<源路径>的文件/目录复制到新的一层镜像内的<目标路径>位置

   - COPY src dest
   - COPY ["src", "dest"]
   - \<src源路径>：源文件或者源目录
   - \<dest目标路径>：容器内的指定路径，该路径不用事先建好，路径不存在的话，会自动创建。

10. VOLUME

    > 容器数据卷，用于数据持保存和持久化工作

11. CMD

    - 指定容器启动后要干的事情
    - CMD指令的格式和RUN相似，也是有两种格式
      - shell 格式：CMD <命令>
      - exec格式：CMD [“可执行文件”, "参数1", "参数2" ...]，在指定了ENTRYPOINT指令后，用CMD指定具体的参数
    - dockerfile中可以有多个CMD指令，但只有最后以一个生效，CMD会被docker run之后的参数替换
    - CMD和RUN命令的区别
      - CMD是在docker run 时运行；
      - RUN是在docker build时运行；

12. ENTRYPOINT

    - 也是用来指定一个容器启动时要运行的命令

      > 类似于CMD指令，但是ENTRYPOINT不会被docker run后面的命令覆盖，而且这些命令行参数会被当做参数送给ENTRYPOINT指令指定的程序。

    - 命令格式

      ```
      ENTRYPOINT ["executable", "param1", "param2"]
      ```

    - ENTRYPOINT可以和CMD一起用，一般是变参才会使用CMD，这里的CMD 等于是在给ENTRYPOINT传参

    - 当指令了ENTRYPOINT后，CMD的含义就发生了变化，不再是直接运行其命令，而是将CMD的内容作为参数传递给ENTRYPOINT指令，他两个组合会变成\<ENTRYPOINT>"\<CMD>"

###### dockerfile/docker镜像/docker容器三者的区别

- dockerfile

  > dockerfile定义了进程的一切东西。
  >
  > dockerfile涉及的内容包括执行代码或者是文件、环境变量、依赖包、运行时环境、动态链接库、操作系统的发行版、服务进程和内核进程（当应用进程需要和系统服务和内核进程打交道，这是需要考虑如何设置namespace的权限控制）等等；

- docker镜像

  > 在dockerfile定义一个文件之后，docker build时会产生一个docker镜像，当运行docker镜像时会真正开始提供服务；

- docker容器

  > 容器是直接提供服务的

##### docker network

```
docker network COMMAND
```

- 查看docker 网络命令：docker network ls
- 创建docker网路：docker network name
- 链接网络到容器：connect
- 断开容器的网络链接：disconnect
- 查看更多网络详细信息：docker network inspect name
- 移除所有的网络：prune
- 移除网络：rm

###### 修改docker的ip网段
> vi /etc/docker/daemon.json
> 新增"bip":"192.166.0.1/24"
- 修改后：
	```
	{
	"bip":"192.166.0.1/24"
	}
	```
- 重启docker
	```
	systemctl restart docker
	```

##### 端口映射与容器互联
###### 端口映射实现容器访问
1. 从外部访问容器应用
	```
	通过-P或-p参数来指定端口映射。当使用-P（大写的）标记时，docker 会随机映射一个49000~49900的端口到内部容器开放的网络端口；
	通过docker ps 或 docker logs命令来查看；
	通过docker inspect +容器IP获取容器的具体信息；
	```
2. 映射所有接口地址
	```
	-p 5000:5000
	默认会绑定本地所有接口上的所有地址；
	可以多次使用-p标记绑定多个端口：
	docker run -d -p 5000:5000 -p 88:80 training/webapp python app.py
	```
3. 映射到指定地址的指定端口
	```
	使用IP:HostPort:ContainerPort格式指定映射使用一个特定地址：
	docker run -d -p 127.0.0.1:5000:5000 training/webapp python app.py
	```
4. 映射到指定地址的任意端口
	```
	使用IP::ContainerPort绑定localhost的任意端口到容器的5000端口，本地主机会自动分配一个端口：
	docker run -d -p 127.0.0.1::5000 training/webapp python app.py
	可以使用udp标记来指定udp端口：
	docker run -d -p 127.0.0.1:5000:5000/udp training/webapp python app.py
	```
5. 查看映射端口配置
	```
	使用docker port来查看当前映射的端口配置，也可以查看到绑定的地址。
	```
###### 互联机制实现便捷互访
> 容器的互联是一种让多个容器中的应用进行快速交互的方式。它会在源和接受容器之间创建连接关系，接受容器可以通过容器名快速访问到源容器，而不用指定具体的IP地址。
1. 自定义容器命名
	```
	使用--name标记可以为容器自定义命名：
	docker run -d -p --name web training/webapp python app.py
	在执行docker run 的时候如果添加--rm标记，则容器在终止后会立刻删除。注意--rm和-d参数不能同时使用。
	```
2. 容器互联
	```
	使用--link参数可以让容器之间安全地进行交互。
	docker run -d -p --name web --link db:db traning/webapp python app.py
	--link参数的格式为--link name:alias，其中name是要链接的容器的名称，alias是别名。
	```

###### 常见网络模式

| 网络模式  | 简介                                                         |
| --------- | ------------------------------------------------------------ |
| bridge    | 为每一个容器分配、设置ip等，并将容器连接到一个docker0 虚拟网络，默认为该模式 |
| host      | 容器将不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的IP和端口 |
| none      | 容器有独立的Network namespace，但并没有对其进行任何网络设置，如分配veth pair和网桥链接，IP等 |
| container | 新创建的容器不会创建自己的网卡和配置自己的IP，而是和一个指定的容器共享IP、端口范围等。 |

###### bridge模式：

>  使用--network bridge 指定，默认使用docker0
>
>  docker服务默认会创建一个docker0网桥（其上存一个docker0内部接口），该桥接网络的名称为docker0，它在内核层连通了其他的物理或虚拟网卡，这就将所有容器和本地主机都放到同一个物理网络。docker默认指定了docker0接口的IP地址和子网掩码，让主机和容器之间可以通过网桥相互通信。

```
# 查看bridge网络的详细信息
docker network inspect bridge
ifconfig | grep docker
```

1. docker使用linux桥接，在宿主机虚拟一个docker容器网桥（docker0），docker启动一个容器时会根据docker网桥的网段分配给容器一个IP地址，称为Container-IP，同时docker网桥是每个容器的默认网关。因为在同一宿主机内的容器都接入同一个网桥。这样容器之间就能够通过容器的container-IP直接通信。

2. docker run 的时候，没有指定network的话默认使用的网桥模式是bridge，使用的是docker0。在宿主机ifconfig就可以看到docker0和自己create的network的eth0，eth1，eth2...代表网卡一，网卡二...，lo代表127.0.0.1,即localhost,inet addr用来表示网卡的ip地址

3. 网桥docker0创建一对对等虚拟设备结构一个叫veth，另一个叫eth0，成对匹配。

   1. 整个宿主机的网桥模式都是docker0，类似一个交换机有一堆借口，每个结构叫veth，在本地主机和容器内分别创建一个虚拟借口，并让他们被此联通（这样一对借口叫veth pair）。
   2. 每个容器实例内部也有一块网卡，每个借口叫eth0。
   3. docker0上面的每个veth匹配某个容器实例内部的eth0，两两匹对，一一匹配。

   通过上述，将宿主机上的所有容器都连接到这个内部网络上，两个容器在同一个网络下，会从这个网关下各自拿到分配的IP，此时两个容器的网络是互通的。

###### host模式：

>  使用--network host指定
>
>  直接使用宿主机IP地址与外界进行通信，不再需要额外进行NAT转换。

###### none模式：

> 使用--network none指定
>
> 在none模式下，并不为docker容器进行任何网络配置
>
> 即这个docker容器没有网卡、IP、路由等信息，只有一个lo，需要自己为docker容器添加网卡、配置IP等。

###### container模式：

>  使用--network container:NAME或者容器ID指定
>
>  新建的容器和已经存在的一个容器共享一个网络ip配置，而不是和宿主机共享。新创建的容器不会创建自己的网卡、配置自己的IP，而是和一个指定的容器共享IP、端口范围等。同样，两个容器除了网络方面，其他的如文件系统、进程列表等还是隔离的。

```
docker run -d -p 8086:8080 --network container:tomcat85 --name tomcat86 bilygoo/tomcat8-jdk8
```

###### 自定义网络

> 自定义网络默认使用的是桥接网络bridge
>
> docker network create my_network

###### 配置容器DNS和主机名
> 容器中主机名和DNS配置信息可以通过三个系统配置文件来管理：
> /etc/resolv.conf
> /etc/hostname
> /etc/hosts
> 启动一个容器，在容器中使用mount命令查看这三个文件挂载信息。

###### 容器访问控制
1. 容器访问外部网络
	```
	# 在宿主机linux系统中，检查转发是否打开：
	sudo sysctl net.ipv4.ip_forward
	net.ipv4.ip_forward = 1
	# 手动打开转发：
	sudo sysctl -w net.ipv4.ip_forward=1
	docker 服务启动时会默认开启--ip-forward-true
	```
2. 容器之间访问
- 容器之间两户访问需要两方面的支持
	- 网络拓扑是否已经连通。默认悄况下， 所有容器都会连接到dockerO 网桥上，这意味着默认情况下拓扑是互通的；
	- 本地系统的防火墙软件iptables 是否允许访问通过。这取决于防火墙的默认规则是允许（大部分情况）还是禁止。
- 访问所有端口
	> 启动Docker 服务时候，默认会添加一条“允许“转发策略到ip 七ables 的FORWARD链上。通过配置-- icc = true I false (默认值为true) 参数可以控制默认的策略。
	> 为了安全考虑，可以在Docker 配置文件中配置DOCKER_OPTS =--icc=false 来默认禁止容器之		  间的相互访问。
	> 同时，如果启动Docker 服务时手动指定－飞ptables =f alse 参数，则不会修改宿主机系统上的 iptables 规则。
- 访问指定端口
	> 在通过-icc=false 禁止容器间相互访问后，仍可以通过- -link=CONTAINER_NAME : ALIAS 选项来允许访问指定容器的开放端口。

###### 映射容器端口到宿主主机的实现
1. 容器访问外部实现
	```
	sudo iptables -t nat -nvL POSTROUTING
	```
2. 外部访问容器实现
	> 容器允许外部访问，可以在docker run 时候通过-p 或- P 参数来启用。
	> iptables -t nat -nvL

###### 配置容器网桥
	```
	--bip=CIDR: IP 地址加掩码格式
	--m 七u=BYTES : 覆盖默认的Docker mtu 配置
	sudo brctl show
	```
###### 自定义网桥
> 在启动Docker 服务的时候，可使用-b BRIDGE 或--bridge=BRIDGE 来指定使用的网桥。
1. 如果服务已经运行，就需要停止服务，并删除旧的网桥
	```
	sudo service docker stop
	sudo ip link set dev docker0 down
	sudo brctl delbr docker0
	```
2. 创建一个网桥bridge0:
	```
	sudo brctl addbr bridge0
	sudo ip addr add 192.168.5.1/24 dev bridge0
	sudo ip link set dev bridge0 up
	```
3. 查看确认网桥创建并启动
	```
	ip addr show bridge0
	```
4. 配置docker 服务，默认桥接到创建的网桥上
	```
	echo 'DOCKER_OPTS="-b=bridge0'' >> /etc/default/docker
	sudo service docker start
	```


##### Docker-Compose

1. 是什么？

   > Docker-Compose是docker官方的开源项目，负责实现对docker容器集群的快速编排。
   >
   > Compose是docker公司推出的一个工具软件，可以管理多个docker容器组成一个应用。你需要定义一个YAML格式的配置文件docker-compose.yml.写好多个容器之间的调用关系。然后，只要一个命令，就能同时启动、关闭这些容器。

2. 能干什么？

   > Compose允许用户通过一个单独的docker-compose.yml模板文件（YAML）格式来定义一组相关联的应用容器为一个项目（project）。
   >
   > 可以很容易地用一个配置文件定义一个多容器的应用，然后使用一条指令安装这个应用的所有依赖，完成构建。Docker-Compose解决了容器与容器之间如何管理编排的问题。

3. 在哪安装下载？

   ```
   https:docs.docker.com/compose/compose-file/compose-file-v3/
   https://docs.docker.com/compose/install/
   ```

###### compose核心概念
- 任务(task)
	> 一个容器被称为一个任务。任务拥有独一无二的ID，在同一个服务中的多个任务需要依次递增。
- 服务(service)
	> 某个相同应用镜像的容器副本集合，一个服务可以横向扩展为多个容器实例。
- 服务栈(stack)
	> 由多个服务组成，相互配合完成特定业务，如web应用服务、数据库服务共同构成web服务栈，一般由一个docker-compose.yml文件定义。
	> compose的默认管理对象是服务栈，通过子命令对栈中的多个服务进行便捷的声明周期管理。

1. 一个文件：docker-compose.yml
2. 两个要素
   1. 服务（service）：一个个应用容器实例
   2. 工程（project）：有一组关联的应用容器组成的一个完整业务单元，在docker-compose.yml文件中定义。

最后执行docker-compose up命令来启动并运行整个应用程序，完成一键部署上线。

###### compose模板文件主要命令
| 命令                                    | 功能                                                         |
| --------------------------------------- | ------------------------------------------------------------ |
| build                                   | 指定Dockerfi le 所在文件夹的路径                             |
| cap_add, cap_drop                       | 指定容器的内核能力(capacity )' 分配                          |
| command                                 | 覆盖容器启动后默认执行的命令                                 |
| cgroup_parent                           | 指定父cgroup 组，意味着将继承该组的资源限制。目前不支持Swam 模式 |
| container_name                          | 指定容器名称。目前不支持Swarm 模式                           |
| devices                                 | 指定设备映射关系，不支持Swam 模式                            |
| depends_on                              | 指定多个服务之间的依赖关系                                   |
| ·ctns                                   | 自定义DNS 服务器                                             |
| dns_search                              | 配置DNS 搜索域                                               |
| dockerfile                              | 指定额外的编译镜像的Dockefile 文件                           |
| entrypoint                              | 裂盖容器中默认的入口命令                                     |
| env_ file                               | 从文件中获取环境变量                                         |
| environment                             | 设置环境变量                                                 |
| expose                                  | 暴露端口，但不映射到宿主机， 只被连接的服务访问              |
| extends                                 | 基于其他模板文件进行扩展                                     |
| external_ links                         | 链接到docker-compose.yml 外部的容器                          |
| extra_hosts 指定额外的host 名称映射信息 |                                                              |
| heal the heck                           | 指定检测应用健康状态的机制                                   |
| image                                   | 指定为镜像名称或镜像ID                                       |
| isolation                               | 配置容器隔离的机制v                                          |
| labels                                  | 为容器添加Docker 元数据信息                                  |
| links                                   | 链接到其他服务中的容器                                       |
| logging                                 | 跟日志相关的配罚                                             |
| network_mode                            | 设置网络模式                                                 |
| networks                                | 所加入的网络                                                 |
| pid                                     | 跟主机系统共享进程命名空间                                   |
| ports                                   | 暴露端口信息                                                 |
| secrets                                 | 配置应用的秘密数据                                           |
| security_opt                            | 指定容跺模板标签( label ) 机制的默认属性（用户、角色、类型、级别等） |
| stop_ grace_period                      | 指定应用停止时，容器的优雅停止期限。过期后则通过SlGK.ILL 强制退出。默认值为10s |
| stop_signal                             | 指定停止容器的信号                                           |
| sysctls                                 | 配置容器内的内核参数。目前不支持Swarm 模式                   |
| ulimits                                 | 指定容器的ulimits 限制值                                     |
| userns_mode                             | 指定用户命名空间模式。目前不支持Swarm 模式                   |
| volumes                                 | 数据卷所挂载路径设置                                         |
| restart                                 | 指定重启策略                                                 |
| deploy                                  | 指定部署和运行时的容器相关配置。该命令只在Swann 模式下生效， 且只支持docker stack deploy 命令部署 |

###### docker-compose命令说明

> 执行命令要在docker-compose.yml目录下进行
```
docker-compose [ -f=<arg> ... ] [options] [COMMAND] [ ARGS ... ]
```
**options**
| 命令                         | 说明                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| -f, --丘le FILE :            | 指定使用的Compose 模板文件，默认为docker-compose.yml,可以多次指定； |
| - p, - -project- name NAME : | 指定项目名称， 默认将使用所在目录名称作为项目名；            |
| --verbose:                   | 输出更多调试信息；                                           |
| -v, --vers i on:             | 打印版本并退出；                                             |
| -H, -host HOST:              | 指定所操作的Docker 服务地址；                                |
| - tls :                      | 启用TLS , 如果指定-tlsverify 则默认开启；                    |
| -tlscacert CA_PATH :         | 信任的TLS CA 的证书；                                        |
| -tlscert CLIENT_CERT_PATH:   | 客户端使用的TLS 证书；                                       |
| tlskey TLS_KEY_PATH :        | TLS 的私钥文件路径；                                         |
| -tlsverify:                  | 使用TLS 校验连接对方；                                       |
| -skip -hostname-check:       | 不使用TLS证书校验对方的主机名；                              |
| -project-directory PATH:     | 指定工作目录，默认为Compose 文件所在路径。命令列表见表24-2 。 |

**COMMAND**
| 命令    | 功能                                                         |
| ------- | ------------------------------------------------------------ |
| build   | 构建（重新构建）项目中的服务容器                             |
| bundle  | 创建一个可分发的配置包， 包括整个服务栈的所有数据，他人可以利用该文件启动服务栈 |
| config  | 校验和查看Compose 文件的配控信息                             |
| down    | 停止服务栈，并删除相关资源，包括容器、挂载卷、网络、创建镜像等。默认情况下只清除所创建的容器和网络资源 |
| events  | 实时监控容片异的串件信息                                     |
| exec    | 在一个运行中的容器内执行给定命令                             |
| help    | 获得一个命令的帮助                                           |
| images  | 列出服务所创建的镜像                                         |
| kill    | 通过发送S IG KJLL 信号来强制停止服务容器                     |
| logs    | 查看服务容器的输出                                           |
| pause   | 暂停一个服务容器                                             |
| port    | 打印某个容器端口所映射的公共端口                             |
| ps      | 列出项目中目前的所有容器                                     |
| pull    | 拉取服务依赖的镜像                                           |
| push    | 推送服务创建的镜像到镜像仓库                                 |
| restart | 项启项目中的服务                                             |
| rm      | 删除所有（停止状态的）服务容器                               |
| run     | 在指定服务上执行一个命令                                     |
| scale   | 设灶指定服务运行的容器个数                                   |
| start   | 启动已经存在的服务容器                                       |
| stop    | 停止已经处于运行状态的容器，但不删除它                       |
| top     | 显示服务栈中正在运行的进程信息                               |
| unpause | 恢复处于暂停状态中的服务                                     |
| up      | 尝试自动完成一系列操作： 包括构建镜像，（重新）创建服务，启动服务，并关联服务相关容器等 |
| version | 打印版本信息                                                 |

**docker-compose环境变量**
| 变量                        | 说明                                                         |
| --------------------------- | ------------------------------------------------------------ |
| COMPOSE_PROJECT_ NAME       | 设置Compose 的项目名称， 默认是当前工作目录( docker-compose. yml文件所在目录）的名字Compose 会为每一个启动的容器前添加的项目名称。例如， 一个名称为proj 的项目， 其中的web 容器名称可能为proj_web_ l |
| COMPOSE_FILE                | 设置要使用的docker-compose.yml 的路径。如果不指定，默认会先查找当前工作目录下是否存在docker-compose.yml 文件，如果还找不到、则继续查找上层目录 |
| COMPOSE_API_VERSION         | 某些情况下， Compose 发出的Docker 请求，其版本可能在服务端并不支持，可以通过指定A P! 版本来临时解决这个问题在生产环境中不推荐使用这个临时方案，要通过适当的升级来保证客户端和服务端版本的兼容性 |
| DOCKER_HOST                 | 设置Docker 服务端的监听地址。默认使用unix:///var/run/ docker.sock ,这其实也是Docker 客户端采用的默认值 |
| DOCKER_TLS_VERIFY           | 如果该环境变狱不为空，则与Docker 服务端的所有交互都通过TLS 协议进行加密 |
| DOCKER_ CERT_ PATH          | 配置TLS 通信所需要的验证文件（包括ca.pem 、cert.pem 和key.pem ) 的路径，默认是-/.docker |
| COMPOSE_HTTP_TIMEOUT        | Compose 向Docker 服务端发送请求的超时，默认值为60s           |
| COMPOSE_TLS_VERSION         | 指定与Docker 服务进行交互的TLS 版本，支持版本为TLSvl (默认值）、TLSvl _ l 、TLSvl_2 |
| COMPOSE_PATH_SEPARATOR      | 指定COMPOSE_FlLE 环境变量中的路径间隔符                      |
| COMPOSE_IGNORE_ORPHANS      | 是否忽略孤儿容楛                                             |
| COMPOSE_PARALLEL_LIMIT      | 设置Compose 可以执行进程的并发数                             |
| COMPOSE_I NTERACTIVE_NO_CLI | 尝试不使用Docker 命令行来执行run 和exec 指令                 |

```dockerfile
version: 'xxx' # 版本号

# docker run -d -p 6001:6001 -v /app/microService:/data --network atguigu_net --name ms01
services: # 固定写死，代表有几个服务实例
  microService: # 自定义服务名
    image: zzyy_docker:1.6 #镜像名字:版本号
    container_name: ms01
    volumes: # 容器数据卷
    	- /app/microService:/data
    network: # docker网络配置
    	- atguigu_net
    depends_on: # 依赖
    	- redis
    	- mysql

# docker run -p 6379:6379 --name redis608 --privileged=true -v /app/redis/redis.conf:/etc/redis/redis.conf -v /app/redis/data:/data -d redis:6.0.8 redis-server /etc/redis/redis.conf
  redis:
  	images: redis:6.0.8
  	ports: # 端口映射
  		- "6379:6379"
  	volumes:
  		- /app/redis/redis.conf:/etc/redis/redis.conf
  		- /app/redis/data:/data
  	networks:
  		- atguigu_net
  	command: redis-server /etc/redis/redis.conf # 命令

# docker run -p 3306:3306 --name mysql5.7 --privileged=true -v /app/mysql/db:/var/lib/mysql -v /app/mysql/mysql_config:/etc/mysql -v /app/mysql/init:/docker-entrypoint-initdb.d -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
  mysql:
    image: mysql:5.7
    environment: # 环境配置
      - MYSQL_ROOT_PASSWORD: "123456"
      - MYSQL_DATABASE: "db"
      - MYSQL_USER: "zzyy"
      - MYSQL_PASSWORD: "zzyy123"
    ports:
      - "3306:3306"
    volumes:
      - /app/mysql/db:/var/lib/mysql
      - /app/mysql/mysql_config:/etc/mysql
      - /app/mysql/init:/docker-entrypoint-initdb.d
    network:
      - auguigu_net
    command: --default-authentication-plugin=mysql_native_password # 解决外部无法访问

# docker network create atguigu_net
network:
	atguigu_net
```
##### docker网络代理配置
- 在执行docker pull时，是由守护进程dockerd来执行。因此，代理需要配在dockerd的环境中。而这个环境，则是受systemd所管控，因此实际是systemd的配置。
	```
	sudo mkdir -p /etc/systemd/system/docker.service.d
	sudo touch /etc/systemd/system/docker.service.d/proxy.conf

 	```
- 在这个proxy.conf文件（可以是任意*.conf的形式）中，添加以下内容：
	```
	[Service]
	Environment="HTTP_PROXY=http://proxy.example.com:8080/"
	Environment="HTTPS_PROXY=http://proxy.example.com:8080/"
	Environment="NO_PROXY=localhost,127.0.0.1,.example.com"
	```
- 重启服务
	```
	重启docker daemon
	sudo systemctl daemon-reload
	sudo systemctl restart docker
	systemctl show --property=Environment docker
	/etc/systemd/system/docker.service.d
	```
##### docker配置镜像加速
- 编辑文件
	```
	vim /etc/docker/daemon.json 
	```
- 添加镜像源
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
- 重启docker服务
	```
	systemctl  daemon-reload     //重启镜像
	systemctl restart  docker.service
	```