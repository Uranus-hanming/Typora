[toc]
#### 1. 远程终端连接

###### 项目介绍

> 背景：原来为了远程连接产线上的设备，每台设备都安装一个TightVNC/UltraVNC（开源免费），每次连接时都需要输入ip、port和密码，而且产线上的设备很多，ip对应的设备关系就很容易搞混，管理起来很麻烦。
>
> 需求：为了方便自动化团队在办公室管理和远程连接产线上的设备，自动化团队提出需求，希望开发一个系统，统一管理这些远程连接，通过这个远程终端连接系统可以方便地远程连接到任何一个产线上的终端设备。
>
> 前后端分离，前端使用vue框架，后端使用flask框架，数据库使用MySQL；实现的功能是：用户可以添加终端设备的ip/port/自定义名称，也可以删除和修改这些配置信息，最重要的是用户可以对已经添加的设备进行connect跳转远程桌面。
>
> 原来是一对一连接，现在通过跳转平台可以一对多。合入FTMS平台项目

###### 功能细节

1. 查询数据

2. 添加信息：name/ip/port

3. 修改信息

4. 删除信息

5. 远程连接：通过端口映射

   ```shell
   import subprocess
   cmd = r"node C:\Users\Administrator\node_modules\noVNC\websockify-js-master\websockify-js-master\websockify\websockify.js --web C:\Users\Administrator\node_modules\noVNC %s %s:%s" % (url_port, ip, port)
   back = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
   ```

###### 什么是VNC和noVNC?

> VNC (Virtual Network Console)是**虚拟网络控制台**的缩写，分为server端和client端两部分，分别部署完成后在server端简单的配置即可使用，基于TCP的通信。noVNC项目是通过取消VNC Client的安装，直接通过浏览器访问noVNC，然后由noVNC间接访问VNC server来达到client web化。从上面部署方式看到，VNC server仍然保留且没有任何修改，处理的始终是TCP流量，但是浏览器和noVNC之间是在http基础上使用WebSocket交互，由于VNC server 无法处理websocket流量，因此引入了 [websockify](https://link.zhihu.com/?target=https%3A//github.com/novnc/websockify) ，noVNC的姐妹项目，负责把WebSocket流量转换为普通的TCP流，使VNC server正常工作。noVNC其实是一个HTML形式的APP，[websockify](https://link.zhihu.com/?target=https%3A//github.com/novnc/websockify)并充当了一个mini web server的角色，当浏览器访问时，会通过网络加载运行noVNC。

###### 解决问题的过程

> 遇到的问题：理解需求（what/why/how：要开发的是一个什么样的系统？有哪些功能？为什么要开发这个系统？技术难点在哪里？），首先遇到的难题是：到底能通过什么方式，充当一个跳转平台，来连接远程的TightVNC，因为原来是通过TightVNC远程控制软件来远程连接，每次都需要输入ip、port和密码。
>
> 如何解决：跟科长和自动化团队负责人讨论需求，了解清楚需求的产生背景，和需求要实现哪些功能和达到什么样的效果，详细了解需求之后就开始去寻找现有哪些工具可以满足我的需求，通过CSND、stack overflow和官网查阅资料，了解什么是TightVNC和VNC，然后发现noVNC这个协议可以用来反向代理VNC服务，而且是一个开源项目，然后在github上去详细了解这个协议具体是什么？怎么使用？最后安装noVNC协议，可以通过在终端运行一行脚本，这行脚本包含本地的port，以此来映射远程的ip、port，然后就可以在本地浏览器访问来跳转到远程桌面。后面就可以围绕这条脚本来进行开发了。
>
> 因为是前后端分离，前后端同步进行开发，所以随时需要跟前端开发的同事进行沟通，确定接口的形式和返回的数据结构、类型等。

###### 技术栈

1. flask框架
2. MySQL数据库
3. git分布式管理
4. 项目测试：接口测试postman
5. 项目部署：docker/supervisor

###### 技术细节

> 使用flask框架，和MySQL数据库，使用flask自带的SQLAlchemy模块和数据库进行交互，设计表结构来存储用户的配置信息，然后写接口来实现用户配置信息的增删改查功能，前端通过访问接口来获取后端返回的JSON数据，来进行前端页面的渲染；用户每次远程连接的时候，都需要进行connect连接，向noVNC协议中传入本地的port和目的远程连接的ip、port，使用标准库中的subprocess模块和其Popen()方法下发脚本命令来起一个进程服务，用户就可通过就浏览器来访问并跳转了。

- 数据库表的设计，字段的数据类型和其他参数（主键，是否唯一，默认值等），主键和外键
  - mysql中的数据类型：
    1. 整数类型：int/smallint/tinyint
    2. 浮点类型：float/double双精度浮点类型
    3. 定点数类型：decimal
    4. 位类型：bit
    5. 日期和时间类型：
    6. 文本字符串类型：char/varchar
    7. 枚举类型：enum
    8. 集合类型：set
    9. 二进制字符串类型
    10. JSON类型：JSON对象、JSON数组
    11. 空间数据类型

- python对数据库的操作：
  - 查询全部记录：User.query.all()
  - 根据条件进行查询：db.session.query(User).filter(User.ip == ip).first()
  - 添加记录：db.session.add(info)、db.session.commit()
- 接口的访问方式有哪些？GET/POST...以及它们之间的区别
  - get请求一般是去获取数据，post请求一般是去提交数据；
  - get请求把数据放在url中，安全和隐私性较差，请求的长度也有限制；post请求把数据放在body中，也没有长度的限制；
  - get请求刷新服务器或者回退没有影响；post请求回退会重新提交数据；
  - get请求可以被缓存；post请求不会被缓存；

- HTTP的8种请求方式
  - GET/POST/PUT/DELETE/OPTIONS/HEAD/CONNECT/TRACE
  - get取，是查询数据，对应select操作；从服务器取出资源
  - post贴，常用于新增数据，对应insert操作；在服务器新建一个资源
  - put放，常用于修改数据，对应update操作；在服务器更新资源
  - delete删，是删除数据，对用delete操作；从服务器删除资源

- 数据格式的转化：json/jsonify
- 常用的标准库：os/sys/time/subprocess

###### 项目总结

- 项目开发流程：

  > 需求分析 -》 开发 -》功能测试 -》项目部署 -》 项目维护
  >
  > 在需求分析阶段：需要了解需求的产生背景、需要实现哪些功能或者提出需求的人想要达到什么效果，开发人员需要考虑的是使用什么技术工具可以实现这些功能，确定使用的框架和数据库，然后进行数据库和表的设计，接口的设计（增删改查等），和前端的同时讨论前后端交互的问题（接口的访问和返回的数据类型）；
  >
  > 开发阶段：根据在需求分析阶段梳理的开发思路进行开发，在具体的开发细节中遇到什么问题，都需要重新梳理需求，和提供需求的人进行更加详细地讨论分析；每个借口开发完都要进行测试，和前端同事进行联通，直至开发完成；然后给用户试运行，确认是否符合客户需求；
  >
  > 功能测试阶段：前后端一起进行功能测试，有问题就修改；
  >
  > 项目部署：
  >
  > 项目维护：解决用户在使用过程中遇到的bug，或者客户提出其他需求，也需要不断地开发维护升级。

- 沟通能力很重要：需求分析跟领导和客户沟通，前后端分离同步开发时和前端的同事沟通

- 解决问题的能力：遇到问题解决问题的能力，学会识别核心问题，将大问题切分为小问题，一大化小直到能够付出行动来解决

- 搜索能力：很多问题都是已经被别人解决过的问题，提高搜索能力，善于借鉴别人的经验，避免重新造轮子，提高开发效率

- 英语阅读能力：大部分的技术文档和官方都是英文的，凡技术必官网，提高英文阅读能力有助于自己去阅读官方的技术文档，能够直接接触一手资料对技术的提升也是很有帮助的，有良好的英文阅读能力能够更容易接触到更多的开源项目，方便查阅更多的技术文档，也能够提高解决问题的能力。

- 编程语言只是一种工具，如何使用工具来实现具体的业务才是最重要的。

#### 2. 自动化报表

> 产线上每个专案每个项目每个工站的每个测试步骤完成都会产生一笔数据，根据这些测试记录来统计产量的变化情况，通过率和失败率，告警情况等，以此来监控每个生产的环节，解决测试失败问题，提高生产效率
>
> 功能：
>
> 1. 同站内各种报警类别的次数
> 2. 每條線UPH比較與趨勢：每天的uph值（將一天劃分為24個小時區間單位，然後統計每個區間的S3和S6的產量數量，最後取每個區間中S3+S6的最大值作為當天的UPH值）
> 3. 同條線內各站UPH數值：將一天劃分為24個小時區間，然後統計各工站每個小時區間內的產量，最後取24小時區間內產量最大的最為當天各工站的UPH值
> 4. 同站內各種報警類別的次數

- 数据库查询和优化：分页和索引
- CPU密集型，多进程多线程
- 需求分析，理解需求，了解实际的业务，以及如何使用代码来实现具体的业务逻辑，也就是代码的实现能力
- 性能分析和优化
- 项目部署：supervisor

###### 技术栈

1. python3.6
2. flask2.0.3
3. mysql5.7
4. supervisor
5. git2.17.1

#### 3. 数据爬虫：selenium

- selenium
  - from selenium import webdriver
    - browser = webdriver.Chrome(chrome_options=chrome_options)
      - browser.get()
      - browser.find_element_by_name()
      - browser.find_element_by_id()
      - browser.find_element_by_xpath()
      - browser.find_element_by_class_name
      - browser.close()
  - from selenium.webdriver.support.ui import Select
  - from selenium.webdriver.chrome.options import Options
    - chrome_options = Options()
- xlwt：办公自动化
- datetime
  - datetime
  - timedelta
- threading
- schedule
- ftplib.FTP()
- from logtrace import create_logger
  - logger = create_logger(\_\_name\_\_)

- 测试框架的使用
- 多进程多线程的使用
- 定时任务：crontab/python微型框架/celery
- ftp的使用

###### 技术栈

1. python3.6
2. selenium3.141.0
3. xlwt
4. threading
5. crontab/schedule
6. git

#### 4. 邮件预警系统

- 每天的FBU截图

  - selenium/mail/crontab

- 产线上服务器磁盘内存剩余告警

  - mysql/django/mail
  - flask框架和django框架的对比
  - 寻找满足业务需求的工具，遇到问题解决问题，不懂就学，学会就用。

- 空气大气压监测系统

  - selenium/mysql/mail/crontab

- 邮件的发送：简单文本传输协议smtp

  - smtplib.SMTP()
  - from email.mime.text import MIMEText
  - from email.mime.multipart import MIMEMultipart
  - from email.header import Header

  ```python
  import smtplib
  from email.mime.text import MIMEText
  from email.mime.multipart import MIMEMultipart
  from email.header import Header

  # 生成可放文字+图片的容器
  msg = MIMEMultipart('related')
  # 添加文本
  msgTxt = MIMEText(html, _subtype='html')
  msg.attach(msgTxt)
  msg['From'] = str(Header(''))
  msg['To'] = ','.join('')
  msg['Subject'] = Header(subject, 'utf-8').encode()
  recipient = [''...]
  s = smtplib.SMTP('')

  s.sendmail(msg['From'], recipient, msg.as_string())
  s.quit()
  ```

- 测试框架爬虫的使用：selenium

- 定时任务的实现：celery/crontab（分时天周月年 执行命令）

###### 技术栈

1. python3.6
2. selenium
3. mysql
4. smtplib
5. crontab
6. git

#### 5. 自动化版本管理系统

> 前后端分离项目，前端使用vue，使用flask框架搭建服务，数据库使用mysql5.7，使用ftp协议存储文件，使用docker部署项目
>
> 需求是什么？自动化部署客户软体
>
> 编写shell脚本完成项目自动化部署
>
> 负责项目的需求讨论分析，项目的开发测试，以及项目的部署和运维工作

###### 系统功能

1. 用户的注册和登录
2. 用户管理员：添加删除用户、修改密码
3. 用户上传依赖包
4. 用户查看依赖包

###### 功能细节

> package/framework/spec/configuration/third group/test stations
>
> 用户把各种依赖包通过FTP上传，然后可以根据测试的要求合成所需要的版本，测试时用户通过.agen_conf配置文件进行配置，然后下载安装对应版本的依赖包（在本地创建一个文件夹，下载对应版本的压缩包并进行解压，下载公共包并安装，然后下载第三方依赖包并安装，下载fox开头的依赖包并安装，最后launch美杜莎），最后启动美杜莎进行测试。美杜莎是客户开发的测试工具，通过autoupdater server进行版本管理和发布。

1. package
   - platform/ftp/upload
   - name/version/platform/upload time/
   - search/delete/archive/recover
2. framework
   - platform/ftp/fox-framework/fox-services/fox-relay 将三个包压缩成一个包
   - name/version/platform/upload time
   - search/delete/archive/recover
3. spec
   - project/platform/ftp/upload
   - project/version/platform/upload time
4. configuration
   - platform/project/station/framework/package group/package/spec/stage
5. third packages：不同项目project下的公共包和第三方依赖包
6. test stations：新增project和stations

###### 开发任务

> 完成了开发任务？

###### 技术架构

1. python3.6
2. flask、django相关的技术
3. MySQL5.7
4. ftp
5. docker19.03.12
6. git

###### 项目总结

##### 目概况

> 37个接口，12张表

##### 需求分析

> 开发一个项目，专门用来管理客户的的测试软体
> 开发一个测试软件管理平台，管理员将测试软件的不同组件上传，然后用户可以针对不同的project/station/platform/version来组合成所需要的测试软件来启动测试，比如针对声学的测试，针对摄像的测试，针对不同的模块的测试需要使用不同的组件来合成的。package/spec/config/third package
> 客户的软体有不同的版本、不同的软体类型，以及不同的平台linux/windows，
>
> 管理员通过页面上传版本，系统后台会把软体上传到FTP，然后把相应的数据记录到数据库，管理员可以对数据进行增删改查，线上的用户进行测试的时候就可以下载对应的版本进行测试
>
> 自动化部署测试平台：有很多依赖包，依赖包的安装有先后顺序，管理员按顺序上传文件，文件的顺序可以修改，然后用户在线上可以一键部署：按顺序下载和安装依赖包，调用客户的接口启动测试平台等

##### 接口功能

1. token验证
2. 返回用户列表
3. 用户注册功能
4. 用户登录功能
5. 密码修改
6. 用户角色更改

#### 6. 路由器二次开发

> 产线上的手机测试需要链接wifi来测试，为了统一管理产线上多台路由器设备。
>
> 设置4/5G频段、频道带宽、防火墙、频道、租约时间等，通过后台找出对应的key:value
>
> 产线上有多台路由器，原来每次修改设备的参数都需要单独连接过去修改，为了统一管理，对需要修改的设置找出对应的key:value，开发一个子平台进行管理，并合入FTMS平台。用户就可以通过FTMS平台，添加对应路由器的信息，查看各个路由器的配置信息，修改对应路由器的配置信息进行测试。
>
> 功能：
>
> 1. 获取所有的基础信息
> 2. ssh连接app服务查询配置参数
> 3. 配置当前的配置信息
> 4. 新增一条基础信息
> 5. 删除一条基础信息
> 6. 更新一条基础信息

- linux系统
- 参数的查询
- Github
- 柳暗花明又一村
- 多进程多线程
- 项目部署

#### 7. mattermost项目部署

> 因为内部团队沟通需要一款保证安全和隐私的沟通工具，让我去开源项目中去寻找一款合适的工具，我在github上找到了mattermost这款免费开源的工具，正好适合团队内部的需要，因此我部署了这款工具并一直在维护和管理。

- linux操作系统
- mysql数据库
- 阅读英文技术文档（github开源项目）
- 解决问题的能力


#### Django项目-邮件告警定时任务

> 搭建Django项目，利用django_celery_beat插件，和celery中间件构建定时任务，通过Django后台管理系统有个crontabs功能，通过此功能可以管理后台的celery定时任务，可以灵活地设定时间间隔，而不用暂停后台的服务和修改源代码

1. 创建Django项目：django-admin startproject name
2. 



#### 工具

- pycharm/vscode
- navicat/workbench
- git/github
- notepad/markdown
- Beyond compare
- xshell/MobaXterm
- Vim
- postman
- CSDN/Stack Overflow/docker Hub
- 官网
  - python官网：https://www.python.org/、第三方包查询：https://pypi.org/
  - docker官网：https://www.docker.com/、docker官方仓库：https://hub.docker.com/
  - linux官网：https://www.linux.org/
  - MySQL官网：https://dev.mysql.com/
  - flask官网：https://flask.palletsprojects.com/en/2.2.x/
  - django官网：https://www.djangoproject.com/