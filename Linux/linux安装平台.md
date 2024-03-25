[toc]

##### centos常用命令

- service ：服务管理（淘汰不用）

- systemctl：服务管理

- source：点命令

- gcc：gcc命令使用GNU推出的基于C/C++的编译器

  ```
  yum install -y gcc gcc-c++
  ```

- tar：解压工具

  ```
  tar -xvf Python-3.10.0.tgz
  -xvf：参数的含义？
  ```

- yum：软件包管理器

  ```
  yum install -y xxx
  默认为yes
  ```

- wget

  > wget 是一个 GPL 许可证下的自由软件，支持 HTTP、FTP 等下载方式，支持代理服务器，支持断点续传等功能。

  ```
  yum install wget -y
  ```

- curl：利用URL规则在命令行下工作的文件传输工具，是一款强大的http命令行工具

  ```
  下载：
  curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-8.repo
  ```

- make：编译工具

- rpm：RPM软件包的管理工具

  ```
  rpm -i gitlab-ce-10.0.0-ce.0.el7.x86_64.rpm
  ```

- vim

  ```
  yum install vim -y
  ```

- firewall：防火墙

  ```
  yum install firewalld 
  ```

- 查看当前操作系统发行版信息

  ```
  cat /etc/issue 或 cat /etc/redhat-release 或 cat /etc/os-release
  ```

- 查看当前操作系统版本信息

  ```
  cat /proc/version
  ```

- 查看当前操作系统内核信息

  ```
  uname -a
  ```

- ln

- cp

- 系统环境变量：echo $PATH

  ```
  /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
  
  环境变量的设置:
  直接用export命令：export PATH=$PATH:/opt/build_tools/bin
  修改profile文件：
  vi /etc/profile 在里面加入: export PATH="$PATH:/opt/build_tools/bin"
  修改.bashrc文件：
  vi /root/.bashrc 在里面加入：export PATH="$PATH:/opt/build_tools/bin"
  ```

  



###### service: 服务管理

> 服务(service) 本质就是进程，但是是运行在后台的，通常都会监听某个端口，等待其它程序的请求，比如(mysqld , sshd、防火墙等)，因此我们又称为**守护进程**

- service 管理指令
  1. `service 服务名 [start | stop | restart | reload | status]`
  2. 在 **CentOS7.0** 后 很多服务不再使用 `service` ,而是 `systemctl`
  3. `service` 指令管理的服务在 `/etc/init.d` 查看

###### systemctl

> 独立服务的服务启动脚本都在目录 **/usr/lib/systemd/system**里
>
> systemctl [OPTIONS…] {COMMAND} …

1. 查看命令帮助

   ```
   systemctl --help
   ```

2. 操作服务

   ```
   systemctl [start | stop | restart | reload | status | is-active] 服务名
   分别对应启动、停止、重启、重新加载、查看状态、是否活跃
   ```

3. 列出所有可用单元

   ```
   systemctl list-unit-files
   ```

4. 

5. 列出所有已加载单元

   ```
   systemctl list-units
   ```

6. 查看可用systemctl 管理的所有服务

   ```
   systemctl list-units --type=service
   ```

7. 注销服务

   ```
   systemctl mask 服务名（守护进程都是以d结尾，即daemon）
   ```

8. 取消注销服务

   ```
   systemctl unmask 服务名
   ```

9. 设置服务开机自启动

   ```
   systemctl enable 服务名
   ```

10. 取消服务开机自启动

    ```
    systemctl disable 服务名
    ```

11. 查看服务是否开机自启动

    ```
    systemctl is-enabled 服务名
    ```

12. 查看系统环境变量

    ```
    systemctl show-environment
    ```

13. 重新加载unit文件

    ```
    systemctl daemon-reload
    ```

14. 杀死服务

    ```
    systemctl kill 服务名
    ```

15. 关闭系统

    ```
    systemctl poweroff
    ```

16. 重启机器

    ```
    systemctl reboot
    ```

###### unit

**unit的常见类型**

- Service unit: 文件扩展名.service, 用于定义系统服务；

- Target unit: 文件扩展名.target, 用于模拟实现"运行级别"；

- Device unit: 文件扩展名.device, 用于定义内核识别的设备；

- Mount unit: 文件扩展名.mount, 用于定义文件系统的挂载点；

- Socket unit: 文件扩展名.socket, 用于标识进程间通信用到的socket文件；

- Snapshot unit: 文件扩展名.snapshot, 用于管理系统快照；

- Swap unit: 文件扩展名.swap, 用于标识swap设备；

- Automount unit: 文件扩展名.automount, 用于定义文件系统自动点设备；

- Path unit: 文件扩展名.path, 用于定义文件系统中的一文件或目录；

**unit file结构**

- `[Unit]`:定义与Unit类型无关的通用选项；用于提供unit的描述信息，unit行为及依赖关系等。
- `[Service]`:与特定类型相关的专用选项；此处为Service类型。
- `[Install]`:定义由"systemctl enable"及"systemctl disable"命令在实现服务启用或禁用时用到的一些选项。

**Unit段的常用选项**

- Description：描述信息，意义性描述；
- After：定义unit的启动次序；表示当前unit应晚于哪些unit启动；其功能与Before相反
- Requies：依赖到其它的units；强依赖，被依赖的units无法激活时，当前的unit即无法激
- Wants：依赖到其它的units；弱依赖；
- Confilcts：定义units 的冲突关系；

**Service段的常用选项**

- Type：用于定义影响ExecStart及相关参数的功能的unit进程类型；类型有：simple、forking、oneshot、dbus、notify、idle。
- EnvironmentFile：环境配置文件；
- ExecStart：指明启动unit要运行的命令或脚本；ExecStart, ExecStartPost
- ExecStop：指明停止unit要运行的命令或脚本；
- Restart:

**Install段的常用配置**

- Alias：
- RequiredBy：被哪些unit所依赖；
- WantBy：被哪些unit所依赖；

**Unit文件样例**

```
[root@s153 system]# cat chronyd.service
[Unit]
Description=NTP client/server
Documentation=man:chronyd(8) man:chrony.conf(5)
After=ntpdate.service sntp.service ntpd.service
Conflicts=ntpd.service systemd-timesyncd.service
ConditionCapability=CAP_SYS_TIME

[Service]
Type=forking
PIDFile=/var/run/chronyd.pid
EnvironmentFile=-/etc/sysconfig/chronyd
ExecStart=/usr/sbin/chronyd $OPTIONS
ExecStartPost=/usr/libexec/chrony-helper update-daemon
PrivateTmp=yes
ProtectHome=yes
ProtectSystem=full

[Install]
WantedBy=multi-user.target
```

###### source

- source命令也称为“点命令”，也就是一个点符号（.），是bash的内部命令。

- 注意：该命令通常用命令“.”来替代

- source命令通常用于重新执行刚修改的初始化文件，使之立即生效，而不必注销并重新登录。因为linux所有的操作都会变成文件的格式存在。

- “source filename”与“sh filename”、“./filename”这三个命令都可以用于执行一个脚本文件，那么它们之间的区别又如何呢？

  ```
  （1）当shell脚本具有可执行权限时，用sh filename与./filename是没有区别的。./filename是因为当前目录没有在PATH中，所以"."是用来表示当前目录的。
  
  （2）sh filename会重新建立一个子shell，在子shell中执行脚本里面的语句，该子shell继承父shell的环境变量，但子shell是新建的，其改变的变量不会被带回父shell，除非使用export。
  
  （3）source filename读取脚本里面的语句依次在当前shell里面执行，没有建立新的子shell。那么脚本里面所有新建、改变变量的语句都会保存在当前shell里面。
  ```

###### yum

> [yum](http://www.yanghengfei.com/tag/yum/)（全称为 Yellow dog Updater, Modified）是一个在Fedora和RedHat以及SUSE中的Shell前端**软件包管理器**。**yum基于rpm包管理**，能够从指定的服务器自动下载并安装rpm包，可以自动处理依赖关系，并且一次安装所有依赖包。

- yum [options] [command] [package ...]

  - options是可选的，选项包括-h（帮助）、-y（当安装过程提示选择时全部为yes）、-q（不显示安装过程）等。
  - command是所要进行的操作，包括install、update、remove、list、info等。
  - package是操作的对象。

- 安装

  ```
  #yum install xxx    
  安装指定程序包。
  ```

- 升级

  ```
  #yum update xxx
  更新指定程序包。
  #yum check-update
  检查可更新的程序。
  #yum upgrade xxx
  升级指定程序包。
  ```

- 查找

  ```
  #yum info xxx
  显示安装包信息。
  #yum info
  列出所有已安装包信息
  #yum list
  显示所有已经安装和可以安装的程序包。
  #yum list xxx
  显示指定程序包安装情况。
  #yum list updates
  列出所有可以更新的程序包。
  #yum list installed
  列出所有已安装的程序包。
  #yum list extras
  列出所有已安装但不在yum Repository中的程序包。
  #yum deplist xxx
  查看指定程序包的依赖关系。
  #yum search xxx
  查找指定程序包，xxx可以是包名的一部分，会列出所有包含xxx的包名。
  ```

- 卸载

  ```
  #yum remove xxx
  卸载指定程序包。
  ```

- 缓存

  ```
  #yum clean packages
  清除缓存目录下的软件包。
  #yum clean headers
  清除缓存目录下的headers。
  #yum clean oldheaders
  清除缓存目录下旧的headers。
  #yum clean,yum clean all
  清除缓存目录下的软件包及旧的headers。
  ```

###### apt



###### wget

> `wget` 是一个在命令行中使用的用于下载文件的工具。它支持通过 HTTP、HTTPS 和 FTP 协议下载文件，并提供了丰富的选项和参数来控制下载过程。本文将详细介绍 `wget` 命令的常用选项和参数，帮助您更好地理解和使用 `wget` 命令。

- `wget` 命令的基本语法

  ```
  wget [选项] [URL]
  ```

- 常用的wget命令选项

  - -O 文件名：将下载的文件保存为指定的文件名。
  - -P 目录：将下载的文件保存到指定的目录。
  - -c：继续下载中断的文件，支持断点续传。
  - -r：递归下载，下载指定 URL 中的所有链接。
  - -np：不递归下载上级目录。
  - -nH：不创建主机目录，将文件保存在当前目录。
  - -b：后台下载，将下载任务放到后台执行。
  - -q：静默模式，减少输出信息。
  - -v：详细模式，增加输出信息。
  - -h 或 --help：显示帮助信息，列出可用的选项和参数。
  - -y：在执行操作时自动回答 “yes”，省去用户确认步骤。

###### curl

> curl是一个利用URL规则在命令行下工作的文件传输工具，是一款强大的http命令行工具。它支持文件的上传和下载，是综合传输工具。
>
> 可以取代 Postman 这一类的图形界面工具

- 语法结构：

  ```
  curl [option] [url]
  ```

- 常见参数：

  ```
  -A/--user-agent <string>              设置用户代理发送给服务器
  -b/--cookie <name=string/file>    cookie字符串或文件读取位置
  -c/--cookie-jar <file>                    操作结束后把cookie写入到这个文件中
  -C/--continue-at <offset>            断点续转
  -D/--dump-header <file>              把header信息写入到该文件中
  -e/--referer                                  来源网址
  -f/--fail                                          连接失败时不显示http错误
  -o/--output                                  把输出写到该文件中
  -O/--remote-name                      把输出写到该文件中，保留远程文件的文件名
  -r/--range <range>                      检索来自HTTP/1.1或FTP服务器字节范围
  -s/--silent                                    静音模式。不输出任何东西
  -T/--upload-file <file>                  上传文件
  -u/--user <user[:password]>      设置服务器的用户和密码
  -w/--write-out [format]                什么输出完成后
  -x/--proxy <host[:port]>              在给定的端口上使用HTTP代理
  -#/--progress-bar                        进度条显示当前的传送状态
  ```

###### rpm

> RPM软件包的管理工具

- 安装命令

  ```
  rpm (选项)(参数) 包名
   rpm -ivh 包全名
  ```

- 参数

| 命令                         | 作用                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| -a                           | 查询所有套件；                                               |
| -e<套件档>或–erase<套件档>   | 删除指定的套件；                                             |
| -h或–hash                    | 套件安装时列出标记；                                         |
| -U<套件档>或–upgrade<套件档> | 升级指定的套件档；                                           |
| -v                           | 显示指令执行过程；                                           |
| –force                       | 强制安装                                                     |
| –nodeps                      | 忽略依赖；安装此包需要依赖，如果你不需要这些依赖可以忽略依赖，强制安装 |
|                              |                                                              |
|                              |                                                              |

- RPM包的升级

  ```
   rpm -Uvh 包全名
   -U（大写）：升级安装。如果没有安装过，则系统直接安装。如果安装过的版本较低，则升级到新版本（upgrade）;
   
   rpm -Fvh 包全名
   -F（大写）：升级安装。如果没有安装过，则不会安装。必须安装有较低版本才能升级（freshen）;
  ```

- RPM包的卸载

  ```
  rpm -e 包名
  ```

- 默认安装路径

  | 安装路径        | 含 义                      |
  | --------------- | -------------------------- |
  | /etc/           | 配置文件安装目录           |
  | /usr/bin/       | 可执行的命令安装目录       |
  | /usr/lib/       | 程序所使用的函数库保存位置 |
  | /usr/share/doc/ | 基本的软件使用手册保存位置 |
  | /usr/share/man/ | 帮助文件保存位置           |





##### win下docker中安装centos

1. 搜索镜像：docker search centos

2. 拉取镜像，直接拉取官方最新的系统镜像：docker pull centos

3. 启动centos

   ```shell
   #运行centos镜像 并把centos的22端口映射到本机的8022端口，做shh连接使用
   #--privileged 付给容器root权限，不然系统级别的操作都搞不了
   docker run -it -d --name=centos_test --privileged -p 8022:22 -p 8080:8080  centos /usr/sbin/init
   ```

4. 进入centos：docker exec -it [容器id]  /bin/bash

5. 配置centos - 配置appstream、仓库、镜像列表URL

   > centos官方停止了对centos8的维护，使用yum命令时候 会提示 appstream 镜像仓库没有url地址

   1. repos 目录：cd /etc/yum.repos.d/

   2. 修改centos 设置url地址

      ```
      sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
      
      sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
      ```

   3. 手动缓存：yum makecache

   4. 更新Yum： yum update -y

6. 检查有无安装ssh：yum list installed | grep openssh-server

7. 安装 密码和ssh服务：yum install passwd openssl openssh-server -y

8. ```
   使用vim 查看 /etc/ssh/sshd_config 文件
   PermitRootLogin 需要打卡
   监听端口：22端口 和启动的端口对应
   开启用户名密码验证关键字：PasswordAuthentication
   以上配置一般是默认的，最好查看一下
   ```

9. 启动sshd：systemctl start sshd

10. 配置开机启动：systemctl enable sshd

11. 配置密码：passwd

- 自定义命令

  ```
  vim .bashrc
  alias ll='ls -l'
  source .bashrc
  ```

- source命令的作用？

- systemctl

- yum install -y xxx

##### centos8更新源

> 阿里云开源镜像站：https://developer.aliyun.com/mirror/

1. 备份

   ```
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
   ```

2. 下载新的CentOS-Base.repo到/etc/yum.repos.d/

   ```
   wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-8.repo
   或者
   
   curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-8.repo
   ```

3. 运行yum makecache生成缓存

   ```
   yum makecache
   ```

4. 更新

   ```
   yum -y update
   ```

##### ubuntu更新源

1. 备份

   ```
   mv /etc/apt/source.list /etc/apt/source.list.bak
   ```

2. 编辑/etc/apt/source.list

   ```
   vim /etc/apt/source.list
   ```

3. Ubuntu版本代号

   > 将所有`focal`更改为其他版本代号
   >
   > 查看当前操作系统发行版本：cat /etc/issue

   - Ubuntu 22.04：jammy
   - Ubuntu 20.04：focal
   - Ubuntu 18.04：bionic
   - Ubuntu 16.04：xenial

4. 常用国内源

   > 建议将所有常用镜像源保存在`/etc/apt`目录下，并命名为类似`source.list.aliyun`的形式，需要使用时直接复制替换`source.list`文件即可。

   - 阿里云：/etc/apt/source.list.aliyun

     ```
     deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
     deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
     deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
     deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
     
     # deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
     # deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
     # deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
     # deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
     
     ## Pre-released source, not recommended.
     # deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
     # deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
     ```

   - 清华：/etc/apt/source.list.tsinghua

     ```
     deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
     deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
     deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
     deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse
     
     # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
     # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
     # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
     # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse
     
     ## Pre-released source, not recommended.
     # deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
     # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
     ```

   - 中科大：/etc/apt/source.list.edu

     ```
     deb https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse
     deb https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
     deb https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
     deb https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse
     
     # deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse
     # deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
     # deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
     # deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse
     
     ## Pre-released source, not recommended.
     # deb https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
     # deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
     ```

##### centos8安装python3.10

> https://www.python.org/ftp/python：python安装包ftp地址

1. linux版本

   ```
   uname -r
   ```

2. 部署依赖包

   ```
   yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel libffi-devel gcc make -y
   ```

3. 查看openssl包

   > python3.10要求openssl版本1.1.1以上

   ```
   openssl version
   ```

4. 创建python安装目录

   ```
   #在配置文件时通过--prefix指定安装路径
   mkdir /usr/local/python3.10
   ```

5. 下载并解压python3.10包

   ```
   cd /tmp
   wget https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz
   tar -xvf Python-3.10.0.tgz
   ```

6. 执行配置文件

   ```
   cd /tmp/Python-3.10.0
   ./configure --prefix=/usr/local/python3.10
   #根据提示执行如下代码对python解释器进行优化
   #执行后无序额外配置可直接使用python3调用python编辑器
   ./configure --enable-optimizations
   ```

7. 编译并安装程序

   ```
   make && make install
   ```

8. 升级pip版本

   ```
   pip3 install --upgrade pip
   ```

9. 查看版本

   ```
   python3 --version
   pip3 --version
   ```

##### ubuntu安装python3.8
1. 更新源
```
apt-get update
apt-get install zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat1-dev liblzma-dev libffi-dev libc6-dev
```
2. 下载Python源代码
```
wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz
wget https://cdn.npm.taobao.org/dist/python/3.8.3/Python-3.8.3.tgz
```
3. 解压
```
tar -xzf Python-3.8.3.tgz
```
4. 配置安装位置
```
cd Python-3.8.3
./configure --prefix=/usr/local/python3.8
```
5. 编译
```
make
```
6. 安装
```
sudo make install
```
7. 设置软连接
```
sudo ln -s /usr/local/python3.8/bin/python3.8 /usr/bin/python3.8
sudo ln -s /usr/local/python3.8/bin/python3.8-config /usr/bin/python3.8-config
```
8. 检查版本
```
python3 -V
```
##### centos8安装mysql5.7

1. ##### 先检查虚拟机中是否有mysql软件

   ```
   rpm -qa|grep mysql
   ```

2. ##### 卸载旧版的mysql

   ```
   yum remove mysql mysql-server mysql-libs mysql-common
   rm -rf /var/lib/mysql
   ```

3. 下载mysql源安装包

   ```
   wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
   ```

4. 安装mysql源

   ```
   yum localinstall mysql57-community-release-el7-8.noarch.rpm -y
   ```

5. 验证安装

   ```
   yum repolist enabled | grep "mysql.*-community.*"
   ```

6. 避免错误Error: Unable to find a match: mysql-community-server

   ```
   yum module disable mysql
   ```

7. 避免错误Error: GPG check FAILED 

   ```
   rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
   ```

8. 开始安装mysql

   ```
   yum install mysql-community-server -y
   ```

9. 启动mysql

   ```
   systemctl start mysqld
   ```

10. 查看启动状态

    ```
    systemctl status mysqld
    ```

11. 设置开机启动

    ```
    systemctl enable mysqld
    systemctl daemon-reload
    ```

12. 查看mysql临时密码

    > mysql安装完成之后，在`/var/log/mysqld.log`文件中有一个默认临时密码，用户名是root

    ```
    grep 'temporary password' /var/log/mysqld.log
    ```

13. 登录并修改密码

    ```
    ALTER USER 'root'@'localhost' IDENTIFIED BY '你的密码';
    
    注：你的密码必须包含以下5个要求：至少8位／大写／小写／特殊符号（@!～等）／数字
    如果你不需要太难的密码，通过以下方式修改：
    SET GLOBAL validate_password_length=4;
    SET GLOBAL validate_password_mixed_case_count=0; 
    SET GLOBAL validate_password_policy=LOW;
    SET GLOBAL validate_password_special_char_count=0;
    ```

14. 设置root账号可远程访问，远程访问MySQL

    1. 进入mysql数据库

       ```
       use mysql;
       ```

    2. 添加远程访问密码

       ```
       GRANT ALL ON *.* TO root@'%' IDENTIFIED BY '###密码###' WITH GRANT OPTION;
       ```

    3. 刷新修改

       ```
       flush privileges;
       ```

    4. 重启服务

       ```
       sudo systemctl restart mysqld
       ```

15. 开启防火墙

    ```
    sudo firewall-cmd --permanent --zone=public --add-port=3306/tcp
    sudo firewall-cmd --reload
    ```

##### centos8安装redis

1. 安装编译工具

   ```
   yum install -y gcc gcc-c++
   ```

2. 检查gcc的版本

   ```
   gcc --version
   ```

3. 下载redis

   > redis版本地址：https://download.redis.io/releases/

   ```
   //将文件下载到这个位置
   cd usr/local/src
   //下载
   wget https://download.redis.io/releases/redis-6.0.9.tar.gz
   //解压文件
   tar -zxvf redis-6.0.9.tar.gz
   ```

4. 安装redis

   ```
    cd redis-6.0.9/
    //编译安装
    //PREFIX redis安装位置
    make PREFIX=/usr/local/redis install
   ```

5. 生成配置文件

   ```
   //创建安装目录
   mkdir /usr/local/redis/conf
   //把源码目录下的redis.conf复制到安装目录
   cp /usr/local/src/redis-6.0.9/redis.conf /usr/local/redis/conf/
   ```

6. 查看核心数量

   ```
   lscpu
   
   CPU(s): redis的IO线程数
   ```

7. 创建供redis运行的目录

   ```
   mkdir /usr/local/redis/logs # logs:存放日志
   mkdir /usr/local/redis/data # //data:存放快照数据
   
   //修改redis的配置文件
   cd /usr/local/redis/conf
   vim redis.conf
        //绑定运行访问的ip
        bind 8.8.8.8
        //使以daemon(守护进程)方式运行
        daemonize yes
        //日志保存
        logfile "/usr/local/redis/logs/redis.log"
        // 数据保存目录
        dir /usr/local/redis/data/
        //使用的最大内存数量
        maxmemory 128MB 
        // io线程数（系统建议设置为cpu核心数量的3/4）
        io-threads 1
        // 添加密码
        requirepass 123456
   ```

8. 启动redis

   ```
   //以前端方式启动（这个只是看能否启动成功，关闭之后redis进程杀死）
    ./usr/local/redis/bin/redis-server
   ```

9. 创建redis服务（后台启动）

   > 要启动后台进程，redis.conf中 daemonize必须是yes

   - 创建服务：vim /lib/systemd/system/redis.service

   ```
   [Unit]
   Description=Redis
   After=network.target
   
   [Service]
   Type=forking
   PIDFile=/var/run/redis_6379.pid
   ExecStart=/usr/local/redis/bin/redis-server /usr/local/redis/conf/redis.conf
   ExecReload=/bin/kill -s HUP $MAINPID
   ExecStop=/bin/kill -s QUIT $MAINPID
   PrivateTmp=true
   
   [Install]
   WantedBy=multi-user.target
   ```

   - 重新加载service文件

   ```
   systemctl daemon-reload 
   ```

   - 再次启动redis

   ```
   //启动redis
    systemctl start redis
    //查看状态
     systemctl status redis
   //  或者是直接查看进程
     ps -ef | grep redis
   ```

   - redis客户端的使用

   ```
   ./usr/local/redis/bin/redis-cli
   然后输入账户密码
   auth "123456"
   ```

   - redis客户端建立软连接

     > echo $PATH：打印系统环境变量
     >
     > 要执行其他路径中的redis-cli得执行./redis-cli，环境变量中可以执行命令redis-cli

   ```
   ln -s /usr/local/redis/bin/redis-cli /usr/bin/redis-cli
   ```

10. 其他配置

    ```
    //启动
    systemctl start redis    
    //关闭
    systemctl stop redis    
    //重启
    systemctl restart redis     
    //查看状态
    systemctl status redis
    //使开机启动
    systemctl enable redis  
    ```

11. 开启防火墙 外网连接

    ```
    firewall-cmd  --zone=public --add-port=6379/tcp --permanent 
    ```

12. 外网访问

    > 注意，上面配置好了之后，外网依然不能连接，因为没有开启外网访问

    ```
    //网络保护（yes就是禁止外网访问 no允许外网访问）
    protected-mode no
    //bind 与其他的IP配置不一样，
    //bind的意思不是绑定外部服务器的IP，而是绑定本机可以接受访问的IP（一般指的是内网ip）
    //下面的意思只允许内网是8.8.8.8的IP访问
    bind:8:8:8:8
    如果要允许外部访问
    bin 127.0.0.1 前加#
    #bin 127.0.0.1
    ```

##### ssh服务

###### centos操作ssh

- 安装：yum install openssh-server
- 卸载：yum remove ssh
- 查看ssh的安装包：rpm -qa | grep ssh
- 查看ssh是否安装成功：ps -ef | grep ssh
- 开启sshd服务 ：service sshd start
- 开启sshd服务 ：systemctl start sshd.service
- 重启ssh服务：systemctl restart sshd.service
- 查看sshd服务的网络连接情况：netstat -ntlp
- 修改Port参数：vim /etc/ssh/sshd_config
- 将SSH服务设置成开机自启动，安装命令：sudo systemctl enable sshd 

###### ubuntu操作ssh

- 停掉SSH服务：sudo stop ssh
- 卸载openssh-client: apt-get remove openssh-server
- 安装openssh-server：apt-get install openssh-server
- 开启sshd服务 ：service sshd start
- 查看服务是否正确启动： ps -e|grep ssh
- 确认ssh-server已经正常工作： netstat -tlp

##### 防火墙

###### centos

- 安装firewalld

  ```
  yum install firewalld
  ```

- firewalld的基本使用

  - 启动： systemctl start firewalld
  - 关闭： systemctl stop firewalld
  - 查看状态： systemctl status firewalld
  - 开机禁用 ： systemctl disable firewalld
  - 开机启用 ： systemctl enable firewalld
  - 查看开放的端口：firewall-cmd --list-ports
  - 添加端口：firewall-cmd --add-port=8080/tcp --permanent （–permanent永久生效，没有此参数重启后失效）

- 防火墙服务
  1、启动、关闭、重启防火墙服务。
      systemctl start  firewalld.service
      systemctl stop  firewalld.service
      systemctl restart  firewalld.service
  2、显示防火墙的状态。
      systemctl status firewalld.service
  3、开机启动防火墙。
      systemctl enable firewalld.service
  4、开机时禁用防火墙。
      systemctl disable firewalld.service
  5、查看防火墙是否开机启动。
      systemctl  is-enabled  firewalld.service
  6、查看防火墙是否开机启动。
      systemctl  is-enabled  firewalld.service
  7、查看已启动的服务列表。
      systemctl list-unit-files|grep enabled
  8、查看启动失败的服务列表。
      systemctl  --failed
  9、启动、停止、重启httpd服务。
      systemctl   start    httpd
      systemctl   stop     httpd
      systemctl   restart  httpd

- 防火墙配置
  1、查看版本。
      firewall-cmd --version
  2、查看帮助。
      firewall-cmd  --help
  3、显示防火墙状态。
      firewall-cmd --state
  4、查看所有打开的端口。
      firewall-cmd --zone=public --list-ports
  5、查看区域信息
      firewall-cmd --get-active-zones
  6、查看指定接口所属区域。
      firewall-cmd --get-zone-of-interface=eth0
  7、拒绝所有包、取消拒绝状态、查看是否拒绝
      firewall-cmd --panic-on
      firewall-cmd --panic-off
      firewall-cmd --query-panic
  8、开启3306端口，–permanent永久生效，没有此参数重启后失效。
      firewall-cmd --zone=public --add-port=3306/tcp --permanent   
  9、重新载入，更新防火墙规则。
      firewall-cmd --reload
  10、查看3306端口是否开放。
      firewall-cmd --zone=public --query-port=3306/tcp 
  11、删除3306端口配置。
      firewall-cmd --zone=public --remove-port=3306/tcp --permanent 

##### 其他问题

- 一个应用程序的文件类型有哪些？

  > 下载压缩包，解压文件，编译安装，配置文件配置，配置服务（以守护进程方式运行），配置服务随系统启动，建立软连接（不同的目录具有不同的功能，如在系统环境变量中，/etc/配置目录，/var/日志等，软件一般安装的目录在哪里？linux系统中一切皆文件），配置防火墙以及网络

- linux如何卸载已安装的应用软件