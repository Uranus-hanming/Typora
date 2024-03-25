[toc]
##### 功能组合键
> 辅助我们进行命令的编写与程序的中断。

- Tab按键

  > 具有***命令补全与文件补齐***的功能。重点是可以避免我们打错命令或文件名。
  >
  > Tab接在一串命令的第一个字段后面，则为命令补全；
  >
  > Tab接在一串命令的第二个字段后面，则为文件补齐。

- Ctrl -c 按键

  > 中断目前程序的按键

- Ctrl -d 按键

  > 代表：键盘输入结束（End Of File, EOF 或 End Of Input）的意思；
  >
  > 也可以用来去掉exit的输入。例如你想直接离开命令行模式，可以直接按下ctrl + d 就能够直接离开（相当于输入exit）

##### linux命令

```
command   [-options]   parameter1   parameter2   ...
   命令		选项		参数（1）	参数（2）
   
命令之后的选项除了前面带减号[ - ]之外，某些特殊情况下，选项或参数前面也会带正号 [ + ]的情况。
```

- 一行命令中第一个输入的部分绝对是命令（command）或可执行文件（例如shell脚本）；
- command为命令的名称；
- 中括号[]并不存在于实际的命令中，表示是可选的，而加入选型设置时，通常选项前会带 - 号，例如 -h；有时候会使用选项的完整全名，则选项前带有 -- 符号，例如 --help;
- parameter1  parameter2 为依附在选项后面的参数，或是command的参数；
- 命令、选项、参数等这几个东西中间以空格来区分，不论空几格shell都视为一格，所以空格是很重要的特殊字符；
- 按下回车键后，该命令就立即执行，回车键代表着一行命令的开始启动。
- 命令太长的时候，可以使用反斜杠（\）来转义回车键，使命令连续到下一行，注意，反斜杠后就立即接着特殊字符才能转义。
- 在linux系统中，英文大小写字母是不一样的；

###### linux常用命令
- 命令 --help求助说明
- man page
- info page
- /usr/share/doc
- 将数据同步写入硬盘中：sync
- 关机：shutdown
- 重启：reboot/poweroff
- 显示目前所支持的语系：locale
- 显示日期：date
- 计算器：bc
- 显示日历：cal
- 

###### 命令执行的判断依据

- cmd; cmd（不考虑命令相关性的连续命令执行）
- cmd1 &&(and) cmd2
  1. 若cmd1执行完毕且正确执行，则开始执行cmd2；
  2. 若cmd1执行完毕且为错误，则cmd2不执行；
- cmd1 ||(or) cmd2
  1. 若cmd1执行完毕且正确执行，则cmd2不执行；
  2. 若cmd1执行完毕且为错误，则开始执行cmd2；

###### 管道命令|（pipe）

- 管道命令仅会处理***标准输出***，对于标准错误会予以忽略；
- 管道命令必须要能够接受来自前一个命令的数据成为标准输入继续处理才行；

###### 选取命令：cut、grep

	> 将一段数据经过分析后，取出我们所想要的，或是经由分析关键词，取得我们所想要的那一行。

- cut

  > 将一段信息的某一段给它切出来，处理的信息是以行为单位；
  >
  > cut主要的用途在于将同一行里面的数据进行分解，最常使用在分析一些数据或文字数据的时候。
  >
  > 将PATH变量取出，然后找出第五个路径：echo $PATH | cut -d ':' -f 5
  >
  > 将export输出的信息，取得第12字符以后的所有字符：export | cut -c 12-

- grep

  > grep是分析一行信息，若当中有我们所需要的信息，就将该行拿出来；

###### 排序命令：sort、wc、uniq

- sort

  > 可以根据不同的数据形式来排序；
  >
  > /etc/passwd 内容是以:来分隔的，以第三栏来排序：cat /etc/passwd | sort -t ':' -k 3

- wc

  > 可以计算输出信息的整体数据；
  >
  > 查询目前账号文件中有多少个账号：cat /etc/passwd | wc -l

- uniq

  > 这个命令用来将重复的行删除掉只显示一个；

###### 双向重定向：tee

> tee会同时将数据流分送到文件与屏幕，而输出到屏幕的，其实是stdout；
>
> ls -l /home | tee ~/homefile | more

###### dpkg的用法

dpkg是一个Debian的一个命令行工具，它可以用来安装、删除、构建和管理Debian的软件包。

1）安装软件

命令行：dpkg -i <.deb file name>

示例：dpkg -i avg71flm_r28-1_i386.deb

2）安装一个目录下面所有的软件包

命令行：dpkg -R

示例：dpkg -R /usr/local/src

3）释放软件包，但是不进行配置

命令行：dpkg –unpack package_file 如果和-R一起使用，参数可以是一个目录

示例：dpkg –unpack avg71flm_r28-1_i386.deb

4）重新配置和释放软件包

命令行：dpkg –configure package_file

如果和-a一起使用，将配置所有没有配置的软件包

示例：dpkg –configure avg71flm_r28-1_i386.deb

5）删除软件包（保留其配置信息）

命令行：dpkg -r

示例：dpkg -r avg71flm

6）替代软件包的信息

命令行：dpkg –update-avail <Packages-file>

7）合并软件包信息

dpkg –merge-avail <Packages-file>

8）从软件包里面读取软件的信息

命令行：dpkg -A package_file

9）删除一个包（包括配置信息）

命令行：dpkg -P

10）丢失所有的Uninstall的软件包信息

命令行：dpkg –forget-old-unavail

11）删除软件包的Avaliable信息

命令行：dpkg –clear-avail

12）查找只有部分安装的软件包信息

命令行：dpkg -C

13）比较同一个包的不同版本之间的差别

命令行：dpkg –compare-versions ver1 op ver2

14）显示帮助信息

命令行：dpkg –help

15）显示dpkg的Licence

命令行：dpkg –licence (or) dpkg –license

16）显示dpkg的版本号

命令行：dpkg –version

17）建立一个deb文件

命令行：dpkg -b direc×y [filename]

18）显示一个Deb文件的目录

命令行：dpkg -c filename

19）显示一个Deb的说明

命令行：dpkg -I filename [control-file]

20）搜索Deb包

命令行：dpkg -l package-name-pattern

示例：dpkg -I vim

21)显示所有已经安装的Deb包，同时显示版本号以及简短说明

命令行：dpkg -l

22）报告指定包的状态信息

命令行：dpkg -s package-name

示例：dpkg -s ssh

23）显示一个包安装到系统里面的文件目录信息

命令行：dpkg -L package-Name

示例：dpkg -L apache2

24）搜索指定包里面的文件（模糊查询）

命令行：dpkg -S filename-search-pattern

25）显示包的具体信息

命令行：dpkg -p package-name

示例：dpkg -p cacti


###### 字符转换命令： tr、col、join、paste、expand

- tr

  > tr可以用来删除一段信息当中的文字，或是进行文字信息的替换；
  >
  > 将last输出的信息中，所有的小写变成大写字符：last | tr '[a-z]' '[A-Z]'

- col

  > 将tab键转换成对等的空格键：col -x

- join

  > 处理两个文件之间的数据（两个文件中，有相同数据的那一行，才将它加在一起）

- paste

  > 直接将两行贴在一起，且中间以tab键隔开；

- expand

  > 将tab案件转成空格键；

###### 划分命令：split

> 将一个大文件，依据文件大小或行数来划分，可以将大文件划分成为小文件；

###### 参数代换：xargs

> 要使用xargs的原因是，很多命令其实并不支持管道命令，因此可以通过xargs来提供该命令使用标准输入；

###### 关于减号 - 的用途

> 在管道命令当中，常常会使用到前一个命令的stdout作为这次的stdin，某些命令需要用到文件名来进行处理时，该stdin与stdout可以利用减号“-”来替代

###### 帮助命令

- --help:几乎Linux上面的命令，在开发的时候，开发者就将可以使用的命令语法与参数写入命令操作过程中。只要使用--help就能够将命令的用法作一个大致的理解。
- man
- ctrl + alt +F1-F6: 命令行模式登陆tty1-tty6终端
- 正常关机的命令：
  - 将数据同步写入硬盘中的命令：sync
  - 常用的关机命令：shutdown
  - 重新启动，关机：reboot, halt, poweroff

##### 用户管理
- 修改文件的权限
	```
	chmod
	-R：进行递归修改，亦即联通子目录下的所有文件、目录都修改。
	```

- 添加用户

  ```
  useradd -m 用户名 （当创建用户成功后，会自动的创建和用户同名的家目录）
  useradd -d 指定目录 用户名 （给新创建的用户指定家目录，d:directory）
  useradd -g 用户组 用户名 （增加用户时直接加上组，g:group）
  ```

- 修改密码

  ```
  passwd 用户名
  ```

- 删除用户

  ```
  userdel 用户名 （但保留其用户的家目录）
  userdel -r 用户名 (删除用户以及用户的主目录)
  ```

- 查询用户信息指令

  ```
  id 用户名
  ```

- 切换用户

  ```
  su - 用户名
  switch user
  ```

- 退出当前用户

  ```
  exit/logout
  ```

- 查看当前用户

  ```
  whoami/ who am i
  ```

##### 用户组管理

- 新增组

  ```
  groupadd 组名
  ```

- 删除组

  ```
  groupdel 组名
  ```

- 修改用户的组

  ```
  chgrp
  -R :进行递归修改
  ```

- 用户和组相关文件

  - /etc/passwd 文件

    ```
    用户（user）的配置文件，记录用户的各种信息
    每行的含义： 用户名：口令：用户标识号：组标识号：注释性描述：主目录：登录Shell
                   1  :  2 :      3   :    4   :      5   :   6  :     7
    ```

  - /etc/shadow 文件

    ```
    口令的配置文件
    每行的含义（9列）：登录名：加密口令：最后一次修改时间：最小时间间隔：最大时间间隔：警告时间：不活动时间：失效时间：标志
    ```

  - /etc/group 文件

    ```
    组（group）的配置文件，记录Linux包含的组的信息
    每行的含义：组名：口令：组标识号：组内用户列表
    ```

##### 权限管理

- 查看文件的所有者：ls -al / ll

  > ls -l --time=ctime/atime: 读取状态时间和读取时间；ls默认显示出来的是该文件的mtime.

  - 修改时间（modification time, mtime）

    > 当该文件的内容数据变更时，就会更新这个时间，内容数据指的是文件的内容，而不是文件的属性或权限。

  - 状态时间（status time, ctime）

    > 当该文件的状态改变时，就会更新这个时间，举例来说，像是权限与属性被更改了，都会更新这个时间

  - 读取时间（access time, atime）

    > 当该文件的内容被读取时，就会更新这个读取时间，举例来说，我们使用cat去读取时，就会更新该文件的atime

- chmod：修改文件或者目录的权限

  - 第一种方式：+、-、=变更权限（+是增加相应的权限，-是删除对应的权限）

    > u：所有者 	g：所有者	o：其他人	a：所有人（u、g、o的总和）

    1. chmod u=rwx,g=rx,o=x 文件/目录名
    2. chmod o+w 文件/目录名
    3. chmod a-x 文件/目录名

  - 第二种方式：通过数字变更权限

    > r=4	w=2	x=1        rwx=4+2+1=7
    >
    > chmod u=rwx,g=rx,o=x 文件/目录名
    >
    > 相当于：chmod 751 文件/目录名

- chown：修改文件所有者

  ```
  改变所有者：chown newowner 文件/目录名
  改变所有者和所在组：chown newowner:newgroup 文件/目录名
  -R：如果是目录，则使其下所有子文件或目录递归生效
  ```

- chgrp：修改文件/目录所在组

  ```
  chgrp newgroup 文件/目录名
  ```

##### 文件目录类
- . 代表此层目录
- .. 代表上一层目录
- \- 代表前一个工作目录
- ~ 代表目前使用者身份所在的家目录
- ~account 代表account这个使用者的家目录
- pwd(print working directory)：显示当前工作目录的绝对路径

- ls(list)：显示当前目录下的文件内容

  - -a：显示当前目录所有的文件和目录，包括隐藏的
  - -l：以列表的方式显示信息

- tree：以树状显示目录结构

- cd(change directory)：切换目录

- mkdir(make directory)：创建文件夹

  - -p：创建多级目录

- rmdir(remove directory)：删除空文件夹

  - rmdir -rf 要删除的目录（删除非空目录，-r：递归删除整个文件夹）

- touch：创建空文件

- cp(copy)：拷贝文件到指定目录

  ```
  cp [选项] source dest
  -r ：递归复制整个文件夹
  强制覆盖不提示的方法：\cp
  \cp -r /home/bbb /opt
  ```

- rm(remove)：移除文件或目录

  - -r：递归删除整个文件夹
  - -f：强制删除不提示

- mv(move)：移动文件与目录或重命名
- file: 观察文件类型

###### 文件的查找
- which: 查找执行文件
	> which命令时根据【PATH】这个环境变量所规范的路径，去查找执行文件的文件名
- whereis:由一些特定的目录中查找
- locate / updatedb
	```
	locate寻找的数据是由自己建立的数据库 /var/lib/mlocate/里面的数据所查找的。
	更新locate数据库的方法：updatedb
	updatedb:根据/etc/updatedb.conf的设置去查找系统硬盘内的文件，并更新/var/lib/mlocate内的数据库文件。
	```
- find

###### 查看文件内容

- cat：查看文件内容

  - -n：显示行号

- nl：显示的时候，同时输出行号

- more：基于vi编辑器的文本过滤器，它以全屏幕的方式按页显示文本文件的内容。

| 操作      | 功能说明                 |
| --------- | ------------------------ |
| space     | 向下翻一页               |
| Enter     | 向下翻一行               |
| q         | 立刻离开more             |
| page up   | 向上滚动一屏             |
| page down | 向下滚动一屏             |
| =         | 输出当前行的行号         |
| :f        | 输出文件名和当前行的行号 |

- less：用来分屏查看文件内容

| 操作        | 功能说明                                       |
| ----------- | ---------------------------------------------- |
| space       | 向下翻动一页                                   |
| Enter       | 向下翻动一行                                   |
| [page up]   | 向上翻动一页                                   |
| [page down] | 向下翻动一页                                   |
| Home        | 回到行首                                       |
| End         | 回到行尾                                       |
| /子串       | 向下搜寻[字幕]的功能；n:向下查找；N:向上查找； |
| ？子串      | 向上搜寻[字幕]的功能；n:向上查找；N:向下查找； |
| q           | 离开less；                                     |

- echo：输出内容到控制台

  ```
  echo $PATH（输出环境变量）
  ```

- head：显示文件的开头部分内容，默认情况下head指令显示文件的钱10行内容

  - -n：显示行数

- tail：输出文件中尾部的内容，默认情况下tail指令显示文件的前10行内容

  - tail 文件 ：查看文件尾10行内容
  - tail -n 5：查看文件尾5行内容
  - tail -f 文件：实时追踪该文档的所有更新

- od：以二进制的方式读取文件内容

- 重定向：>指令和>>指令

  > Shell会自动为我们打开和关闭0、1、2这三个文件描述符，我们不需要显式地打开或关闭它们。标准输入是命令的输入，默认指向键盘；标准输出是命令的输出，默认指向屏幕；标准错误是命令错误信息的输出，默认指向屏幕。
  >
  > 如果没有显式地进行重定向，命令通过文件描述符0从屏幕读取输入，通过文件描述符1和2将输出和错误信息输出到屏幕。但如果我们想从其他文件（再次强调，I/O设备在Unix/Linux中也是文件）读取输入或产生输出，就需要对0、1、2使用重定向了。

  ```
  其语法如下：
  command < filename                         把标准输入重定向到filename文件中
  command 0< filename                       把标准输入重定向到filename文件中

  command > filename                         把标准输出重定向到filename文件中(覆盖)
  command 1> fielname                       把标准输出重定向到filename文件中(覆盖)

  command >> filename                       把标准输出重定向到filename文件中(追加)
  command 1>> filename                     把标准输出重定向到filename文件中(追加)

  command 2> filename                       把标准错误重定向到filename文件中(覆盖)
  command 2>> filename                     把标准输出重定向到filename文件中(追加)

  command > filename 2>&1               把标准输出和标准错误一起重定向到filename文件中(覆盖)
  command >> filename 2>&1             把标准输出和标准错误一起重定向到filename文件中(追加)

  command < filename >filename2        把标准输入重定向到filename文件中，把标准输出重定向到filename2文件中
  command 0< filename 1> filename2   把标准输入重定向到filename文件中，把标准输出重定向到filename2文件中

  重定向的使用有如下规律：
  1）标准输入0、输出1、错误2需要分别重定向，一个重定向只能改变它们中的一个。
  2）标准输入0和标准输出1可以省略。（当其出现重定向符号左侧时）
  3）文件描述符在重定向符号左侧时直接写即可，在右侧时前面加&。
  4）文件描述符与重定向符号之间不能有空格！
  ```

  ```
  >输出重定向和>>追加
  1  ：表示stdout标准输出，系统默认值是1，所以">/dev/null"等同于"1>/dev/null"
  2  ：表示stderr标准错误
  &  ：表示等同于的意思，2>&1，表示2的输出重定向等同于1

  1 > /dev/null 2>&1 语句含义：
  1 > /dev/null ： 首先表示标准输出重定向到空设备文件，也就是不输出任何信息到终端，说白了就是不显示任何信息。
  2>&1 ：接着，标准错误输出重定向（等同于）标准输出，因为之前标准输出已经重定向到了空设备文件，所以标准错误输出也重定向到空设备文件。
  ```

- ln：软链接也称为符号链接，类似于windows里的快捷方式，主要存放了链接其他文件的路径

  ```
  ln -s [源文件或目录] [软链接名]
  给原文件创建一个软链接
  案例：在/home目录下创建一个软连接myroot,连接到/root目录
  ln -s /root /home/myroot
  ```

- history：查看已经执行过的历史命令

  ```
  history n
  ```
- 执行文件路径的变量：$PATH
	```
	echo：显示、打印
	PATH前面加$表示后面接的是变量
	例题：让root在任何目录均可执行/root下面的ls，那么将/root加入PATH当中即可：
	PATH="${PATH}:/root"
	```
###### 文件默认权限：umask
> umask指定目前用户在建立文件或目录时候的权限默认值
> umask的数字指的是该默认值需要减掉的权限。第一组是特殊选线用的。因为r、w、x分别是4、2、1，所以，当拿掉能写的权限，就是输入2；而如果要拿掉能读的权限，也就是4；拿掉读与写的权限，就是6；拿掉执行与写入的权限就是3了。
> 修改umask：/etc/bashrc 或 ~/.bashrc
```
umask
umask -S
```

###### 文件隐藏属性 - chattr
```
chattr [+-=] [ASacdistu] 文件或目录名称
选项与参数：
+ ： 增加某一个特殊参数，其他原本存在参数则不动；
- ： 删除某一个特殊参数，其他原本存在参数则不动；
= ： 直接设置参数，且仅有后面接的参数。
a ： 当设置a之后，这个文件将只能增加数据，而不能删除也不能修改数据，只有root才能设置这属性。
i： 可以让一个文件【不能被删除、改名、设置链接也无法写入或新增数据】

touch attrtest
chattr +i attrtest（连root也没有办法对这个文件进行修改和删除）
chattr -i attrtest
rm attrtest
```
- lsattr（显示文件隐藏属性）

###### 文件特殊权限：SUID、SGID、SBIT
> s与t这两个权限的意义与系统的账号及系统的进程管理较为相关
- Set UID（SUID）
> 当s这个标志出现在文件拥有者的x权限上时，被称为SUID的特殊权限，基本上SUID有这样的限制与功能：
> - SUID权限仅对二进制程序(binary program) 有效；
> - 执行者对于该程序需要具有x的可执行权限；
> - 本权限仅在执行该程序的过程中有效（run-time）；
> - 执行者将具有该程序拥有者（owner）的权限。

- Set GID（SGID）
	与SUID不同的是，SGID可以针对文件或目录来设置。

  -  对文件来说，SGID有如下功能：
	```
	SGID对二进制程序有用；
  	程序执行者对于该程序来说，需具备x的权限；
  	执行者在执行的过程中将会获得该程序用户组的支持。
	```
  - 对目录来说，SGID有如下功能：
	```
	用户若对于此目录具有r与x的权限时，该用户能够进入此目录；
	用户在此目录下的有效用户组（effective group）将会变成该目录的用户组；
	用途：若用户在此目录下具有w的权限（可以新建文件），则用户所建立的新文件，该新文件的用户组与此目录的用户组相同。
	```
- Sticky Bit（SBIT）
	```
	这个Sticky Bit(SBIT)目前只针对目录有效，对于文件已经没有效果了，SBIT对于目录的作用是：
	1. 当用户对于此目录具有x、w权限，即具有写入的权限；
	2. 当用户在该目录下建立文件或目录时，仅有自己与root才有权利删除该文件。
	换句话说：当甲这个用户对于A目录具有用户组或其他人的身份，并且拥有该目录w的权限，这表示甲用户对该目录内任何人建立的目录或文件均可进行删除、更名、移动等操作。不过，如果将A目录加上SBIT的权限选项时，则甲只能够针对自己建立的文件或目录进行删除、更名、移动等操作，而无法删除他人的文件。
	```
- SUID/SGID/SBIT权限设置
  - 4为SUID
  - 2为SGID
  - 1为SBIT
  ```
  假设要将一个文件权限改为【-rwxr-xr-x】时，由于s在用户权限中，所以是SUID，因此，在原先的755之前还要加上4，也就是【chmod 4755 filename】来设置。
  ```

##### linux磁盘与文件系统管理
- 查看linux支持的文件系统有哪些：
	```
	ls -l /lib/modules/$(uname -r) /kernel/fs
	```
- 查看系统目前已加载到内存中支持的文件系统：
	```
	cat /proc/filesystems
	```
###### 文件系统特性
> linux操作系统的文件权限（rwx）与文件属性（拥有者、用户组、时间参数等），这两部分的数据分别存放在不同的区块，权限和属性放置到inode中，至于实际数据则放置到数据区块中。
- 超级区块（superblock）会记录整个文件系统的整体信息，包括inode与数据区块的总量、使用量、剩余量等。
- inode：记录文件的属性，一个文件占用一个inode，同时记录此文件的数据所在的区块号码；
- 数据区块实际记录文件的内容，若文件太大时，会占用多个区块。
- ext2文件系统的区块限制：
  - 原则上，区块的大小与数量在格式化完就不能够再修改（除非重新格式化）；
  - 每个区块内最多能够放置一个文件的数据；
  - 承上，如果文件大于区块的大小，则一个文件会占用多个区块数量；
  - 承上，若文件小于区块，则该区块的剩余容量就不能够被使用了（磁盘空间会浪费）。
- inode table(inode 表)
    - 该文件的读写属性（read、write、excute）;
    - 该文件的拥有者与用户组（owner、group）;
    - 该文件的大小；
    - 该文件建立或状态改变的时间（ctime）；
    - 最近一次的读取时间（atime）;
    - 定义文件特性的标识（flag），如SetUID;
    - 该文件真正内容的指向（pointer）;inode的数量与大小也是在格式化时已经固定了，除非之外inode还有写什么特色？
    - 每个inode大小均固定为128B（新的ext4与xfs可设置到256B）；
    - 每个文件都仅会占用一个inode而已；
    - 承上，因此文件系统能够建立的文件数量与inode的数量有关；
    - 系统读取文件时需要先找到inode，并分析inode所记录的权限与用户是否复合，若符合才能够读取区块的内容。
 - Superblock（超级区块，一般大小为1024B）
   - 记录数据区块与inode的总量；
   - 未使用与已使用的inode与数据区块数量；
   - 数据区块与inode的大小（block为1/2、4K，inode为128B或256B）；
   - 文件系统的挂载时间、最近一次写入数据的时间、最近一次检验磁盘（fsck）的时间等文件系统的相关信息；
   - 一个有效位数值，若此文件系统已被挂载，则有效位为0，若未被挂载，则有效位为1；
- Filesystem Description（文件系统描述说明）
	> 这个区段可以描述每个区块群组的开始与结束的区块，以及说明每个区段（超级区块、对照表、inode对照表、数据区块）分别介于哪一个区块之间，这部分能够用dumpe2fs来观察。
- 区块对照表（block bitmap）
- inode对照表（inode bitmap）
- dumpe2fs：查询ext系列超级区块信息的命令

###### ext2/ext3/ext4文件的存取与日志式文件系统的功能
- 新建一个文件，文件系统的操作：
   1. 先确定用户对于欲新增文件的目录是否具有w与x的权限，若有的话才能新增；
   2. 根据inode对照表找到没有使用的inode号码，并将新文件的权限、属性写入；
   3. 根据区块对照表找到没有使用中的区块号码，并将实际的数据写入区块中，且更新inode的区块指向数据；
   4. 将刚刚写入的inode与区块数据同步更新inode对照表与区块对照表，并更新超级区块的内容。
- 日志式文件系统
  1. 预备：当系统要写入一个文件时，会现在日志记录区块中记录某个文件准备要写入的信息；
  2. 实际写入：开始写入文件的权限与数据；开始更新metadata的数据；
  3. 结束：完成数据与metadata的更新后，在日志记录区块当中完成该文件的记录；

###### linux文件系统的运行
- 系统会将常用的文件数据放置到内存的缓冲区，以加速文件系统的读写操作；
- 承上，因此linux的物理内存最后都会被用光，这是正常的情况，可加速系统性能；
- 你可以手动使用sync来强制内存中设置为Dirty的文件回写到磁盘中；
- 若正常关机时，关机命令会主动调用sync来将内存的数据回写入磁盘内；
- 但若不正常关机（如断电、宕机或其他不明原因），由于数据尚未回写到磁盘内，因此重新启动后可能会花很多时间在进行磁盘校验，甚至可能导致文件系统的损坏（非磁盘损坏）。

###### 文件系统的简单操作
- df :列出文件系统的整体磁盘使用量；
	- df -h:将容量结果以易读的格式显示出来；
	- df -aT:将系统内的所有特殊文件格式及名称都列出来；
	- df -h /etc:将/etc下面的可用的磁盘容量以易读的容量格式显示；
	- df -ih:将目前各个硬盘分区可用的inode数量列出；
- du:查看文件系统的磁盘使用量（常用在查看目录所占磁盘空间）；
	- du -a:累出目前目录下的所有文件容量，同时将文件的容量也列出来；
	- du -sm /*:检查根目录下面每个目录所占用的容量；

###### 硬链接与符号链接：ln
- 硬链接（Hard Link，硬式链接或实际链接）
  - 每个文件都会占用一个inode，文件内容有inode的记录来指向；
  - 想要读取该文件，必须要经过目录记录的文件名来指向到正确的inode号码才能读取。也就是说文件名只与目录有关，但是文件内容则与inode有关。
  - 硬链接只是在某个目录下新增一条文件名链接到某inode号码的关联记录而已。
  - 使用硬链接设置链接文件时，磁盘的空间与inode的数据都不会改变。
  - 不能跨文件系统；
  - 不能链接目录；
- 符号链接（Symbolic Link，亦即是快捷键方式）
	- 建立一个独立的文件，而这个文件会让数据的读取指向它链接的那个文件的文件名。
```
ln [-sf] 源文件 目标文件
-s：如果不加任何参数就进行链接，那就是硬链接，至于-s就是符号链接；
```

###### 磁盘的分区、格式化、检验与挂载
**新增一块磁盘时的操作：**
- 对磁盘进行划分，以建立可用的硬盘分区；
- 对该硬盘分区进行格式化（format），以建立系统可用的文件系统；
- 若想要仔细一点，则可对刚刚建立好的文件系统进行检验；
- 在linux系统上，需要建立挂载点（亦即是目录），并将它挂载上来；
**观察磁盘分区状态：**
- lsblk(list block device):列出系统上的所有磁盘列表
	- NAME:设备是文件名，会省略/dev等前导目录；
	- MAJ:MIN：其实内核识别的设备都是通过这两个代码来实现的，分别是主要与次要设备代码；
	- RM：是否为可卸载设备，如光盘、USE磁盘等；
	- SIZE：容量；
	- RO：是否为只读设备的意思；
	- TYPE：是磁盘（disk）、分区（partion）还是只读存储器（rom）等输出；
	- MOUNTPOINT:挂载点；
	```
	仅列出/dev/vda设备内的所有数据的完整文件名：
	lsblk -ip /dev/vda
	```
- blkid: 列出设备的UUID等参数
> UUID是全局唯一标识符（universally unique identifier），linux会将系统内所有的设备都给予一个独一无二的标识符，这个标识符就可以拿来作为挂载或是使用这个设备或文件系统。
- parted：列出磁盘的分区表类型与分区信息
**磁盘分区：gdisk/fdisk**
- MBR分区表请用fdisk；GPT分区表请使用gdisk分区。
- 你应该要通过lsblk或blkid先找到磁盘，再用parted /dev/xxx print来找到内部的分区表类型，之后才用gdisk或fdisk来操作系统。

**文件系统挂载与卸载 - mount**
- 单一文件系统不应该被重复挂载在不同的挂载点（目录）中；
- 单一目录不应该重复挂载多个文件系统；
- 要作为挂载点的目录，理论上应该都是空目录才行；


##### 时间日期类

- date：显示当前日期

  - date -s 字符串时间

  ```
  设置系统当前时间：
  date -s "2022-08-18 11:30:00"
  ```

- cal(calendar ) + 年份：查看日历

- bc：计算器

##### 搜索查找类

- find：将从指定目录向下递归地遍历其各个子目录，将满足条件的文件或者目录显示在终端

  ```
  find [搜索范围] [选项]
  案例：按文件名，根据名称查找/home目录下的hello.txt文件
  find /home -name hello.txt
  ```

  | :选项           | :功能                            |
  | --------------- | -------------------------------- |
  | -name<查询方式> | 按照指定的文件名查找模式查找文件 |
  | -user<用户名>   | 查找属于指定用户名所有文件       |
  | -size<文件大小> | 按照指定的文件大小查找文件       |

- locate：可以快速完成定位文件路径。

  > locate指令利用事先建立的系统中所有文件名称及路径的locate数据库实现快速定位给定的文件。
  >
  > locate指令无需遍历整个文件系统，查询速度较快。
  >
  > 由于locate指令基于数据库进行查询，所以第一次运行前，必须使用updatedb指令创建locate数据库。

- which：查看某个指令在哪个目录下

- whereis: 只找系统中某些特定目录下面的文件而已

- grep指令和管道符号|

  > grep：过滤查找
  >
  > 管道符号|：表示将前一个命令的处理结果输出传递给后面的命令处理。

- df(disk free): 列出文件系统的整体磁盘使用量；

- du(disk usage): 查看文件系统的磁盘使用量（常用在查看目录所占磁盘空间）；

- lsblk（list block device）: 列出系统上的所有磁盘列表；

##### 压缩和解压类

###### zip/unzip

- zip [选项] xxx.zip 要压缩的文件或文件夹
  - -r：递归压缩
- unzip [选项] xxx.zip
  - -d<目录>：指定解压后文件的存放目录

###### tar指令

```
tar [选项] xxx.tar.gz 打包的内容

案例：
压缩多个文件，将/home/pig.txt 和 /home/cat.txt 压缩成 pc.tar.gz
tar -zcvf pa.tar.gz /home/pig.txt /home/cat.txt

将pc.tar.gz 解压到当前目录
tar -zxvf pc.tar.gz
```

| :选项 | :功能              |
| ----- | ------------------ |
| -c    | 产生.tar打包文件   |
| -v    | 显示详细信息       |
| -f    | 指定压缩后的文件名 |
| -z    | 打包同时压缩       |
| -x    | 解压.tar文件       |

##### Linux文件目录

1. /bin

   > 系统有很多存放执行文件的目录；

2. /boot

   > 主要放置启动会使用到的文件，包括Linux内核文件以及启动选项与启动所需配置文件等。

3. /dev(device)

   > 在Linux系统上，任何设备与接口设备都是以文件的形式存在于这个目录中。只要通过读写这个目录下面的某个文件，就等于读写某个设备。

4. /etc

   > 系统主要的配置文件几乎都放置在这个目录内。

5. /lib

   > 系统的函数库

6. /media

   > 放置可删除的设备，包括软盘、光盘、DVD等设备都暂时挂载于此。

7. /mnt(mount 攀登)

   > 挂载某些额外的设备

8. /opt

   > 给第三方辅助软件放置的目录。

9. /run

   > 放置系统启动后所产生的各项信息

10. /sbin

    > 放置启动过程所需要的，里面包括启动、修复、还原系统所需要的命令。

11. /srv

    > srv可以视为service的缩写，是一些网络服务启动之后，这些服务所需要使用的数据目录。

12. /tmp

    > 这是让一般用户或是正在执行的程序暂时放置文件的地方。

13. /usr

    > UNIX Software Resource的缩写，UNIX操作系统软件资源所放置的目录

    - /usr/bin/

      > 所有一般用户能够使用的命令都放在这里。使用链接文件的方式将/bin链接至此，即/usr/bin与/bin一模一样。

    - /usr/lib/

      > 与/lib功能相同，所以/lib就是链接到此目录中的。

    - /usr/local/

      > 系统管理员在本机安装自己下载的软件。

    - /usr/sbin/

      > /sbin链接到此目录中

    - /usr/share/

      > 主要放置只读的数据文件，当然也包括共享文件。

    - /usr/games/

      > 与游戏比较相关的数据放置处

    - /usr/include/

      > c/c++等程序语言的头文件（head）与包含文件（include）放置处，当我们以Tarball（*.tar.gz）方式安装某些程序时，会使用到里面的许多文件。

    - /usr/libexec

      > 放置某些不被一般用户常用的执行文件或脚本等。

    - /usr/lib<qual>/

      > /lib<qual>链接到此目录

    - /usr/src/

      > 一般源代码建议放置到这里，src有source的意思。至于内核源代码则建议放置到/usr/src/Linux/目录下

14. /var(variable)

    > 主要放置变动性的数据，包括缓存（cache）、日志文件（log file）以及某些软件运行所产生的文件，包括程序文件（lock file、run file），例如MySQL数据库的文件等。

    - /var/cache/

      > 应用程序本身运行过程中会产生的一些缓存。

    - /var/lib/

      > 程序本身执行的过程中，需要使用到的数据文件放置的目录。在此目录下各自的软件应该要有各自的目录。

    - /var/lock/

      > 某些设备或是文件资源一次只能被一个应用程序所使用，如果同时又两个程序使用该设备时，就可能产生一些错误的状况，因此就得要该设备上锁，以确保该设备只会给单一软件使用。

    - /var/log/

      > 这是日志文件放置的目录。

    - /var/mail/

      > 放置个人电子邮箱的目录

    - /var/run/

      > 某些程序或是服务启动后，会将他们的PID放置在这个目录下。

    - /var/spool

      > 这个目录通常放置一些队列数据，所谓的队列就是排队等待其他程序使用的数据，这些数据被使用后通常都会被删除。

15. /home

    > 系统默认的洪湖家目录

16. /root

    > 系统管理员的家目录

17. /lost+found

    > 这个目录是使用标准的ext2, ext3, ext4文件系统格式才会产生的一个目录，目的在于当文件系统发生错误时，将一些遗失的片段放置到这个目录下。

18. /proc

    > 这个目录本身是一个虚拟文件系统，它放置的数据都是在内存当中，例如系统内核、进程信息、外接设备的状态及网络转台等。本身不占据任何硬盘空间。

19. /sys

    > 也是一个虚拟的文件系统，主要也是记录内核与系统硬件信息相关的内容。不占据硬盘空间。

##### 定时任务调度
###### 系统上常见的例行性工作

- 执行日志文件的轮询（logrotate）

- 日志文件分析 logwatch 的任务

- 建立 locate 的数据库

  > 文件名数据库放置位置：/var/lib/mlocate

- manpage查询数据库的建立

- RPM软件日志文件的建立

- 删除缓存

- 与网络服务有关的分析操作：如apache

###### 仅执行一次的计划任务 - at

> /etc/at.allow 与 /etc/at.deny

- at [-mldv] TIME

  - -m：当at的任务完成后，即使没有输出信息，亦发email通知使用者该任务已完成。
  - -l：at -l相当于atq，列出目前系统上面的所有该使用者的at计划。
  - -d：at -d 相当于atrm，可以取消一个在at计划中的任务。
  - -v：可以使用较明显的时间格式列出at计划中的任务列表。
  - -c：可以列出后面接的该项任务的实际命令内容。
  - atq：查询任务
  - atrm (jobnumber)：删除任务
  - batch：系统有空时才执行后台任务

  ```
  1. 再过五分钟后，将/root/.bashrc发给root自己：
  at now + 5 minutes
  使用at时会进入一个at shell的环境来让用户执行任务命令，输入ctrl + d就会出现<EOF>的字样，代表结束。
  建议使用绝对路径来执行你的命令，避免出问题。
  at的执行与终端环境无关，而所有标准输出、标准错误输出都会发送到执行者的mailbox中。
  2. 由于机房预计于2022/11/11停电，我想要在2022/11/11 23:00关机：
  at 23:00 2022/11/11
  at> /bin/sync
  at> /bin/sync
  at> /sbin/shutdown -h now
  at> <EOF>
  3. 五分钟后在终端输出hello：
  at now + 5 minutes
  >at echo "hello" > /dev/tty1
  >at <EOF>
  ```


> at是个可以处理仅执行一次就结束的命令，要执行at，必须有atd这个服务。
>
> 使用at这个命令来产生所要运行的任务，并将这个任务一文本文件的方式写入/var/spool/at/目录中，该任务便能等待atd这个服务的使用与执行了。

- 重新启动atd服务：systemctl restart atd

- 让atd服务开机就自动启动：systemctl enable atd

- 查看atd目前的状态：systemctl status atd

- 为了安全，可以利用/etc/at.allow与/etc/at.deny这两个文件来实现对at的使用限制，at的工作情况如下：

  1. 先找寻/etc/at.allow这个文件，写在这个文件中的用户才能使用at，没有在这个文件中的用户则不能使用at（即使没有卸载at.deny）中；
  2. 如果/etc/at.allow不存在，就查找/etc/at.deny这个文件，写在这个at.deny中的用户则不能使用at，而没有在这个at.allow文件中的用户，就可以使用at；
  3. 如果两个文件都不存在，那么只有root可以使用at这个命令。

- 实际运行单一计划任务

  > at [-mldv] TIME
  >
  > 再过五分钟：at now + 5 minutes

- 脱机继续执行的任务：

  > 由于at计划任务的使用，系统会将该项at任务独立出你的bash环境，直接交给系统的atd程序来接管。因此，当你执行了at的任务之后就可以立刻脱机了，剩下的工作就完全交给Linux管理。

- at常用命令：

  - atq:查询目前主机上面有多少的at计划任务
  - atrm 3: 将第三个任务删除

###### crontab

> crontab这个命令所设置的任务将会循环地一直执行下去，可循环的时间为分钟、小时、每周、每月或每年等。
>
> 循环执行的计划任务是由cron(crond)这个系统服务来空值的；
>
> crontab是Linux提供用户空值计划任务的命令；
>
> crontab的执行可以通过：命令，或者编辑/etc/crontab；
>
> 让crontab可以生效的服务是crond。

- 为了避免安全性问题，可以限制使用crontab的账号：

  - /etc/cron.allow

    > 将可以使用crontab的账号写入其中，不在这个文件内的用户则不可使用crontab

  - /etc/cron.deny

    > 将不可以使用crontab的账号写入其中，未记录到这个文件当中的用户，就可以使用crontab

- crontab的语法

  > crontab [-u username] \[-l | -e | -r]
  >
  > -u ： 只有root才能执行这个任务，亦即帮其他使用者建立/删除crontab计划任务；
  >
  > -e ： 编辑crontab的任务内容；
  >
  > -l ： 查看crontab的任务内容；
  >
  > -r ： 删除所有的crontab的任务内容，若仅要删除一项，请用-e去编辑。
  >
  > 重新启动crond服务：systemctl restart crond

  ```shell
  # 用charles的身份在每天的12:00发信给自己
   0  12 *  *  * mail -s "at 12:00" charles < /home/charles/.bashrc
  #分 时 日 月 周 |<=====================命令串====================>|
  ```

| 代表的意义 | 分钟 | 小时 | 日期 | 月份 | 周   | 命令           |
| ---------- | ---- | ---- | ---- | ---- | ---- | -------------- |
| 数字范围   | 0-59 | 0-23 | 1-31 | 1-12 | 0-7  | 需要执行的命令 |

| 特殊字符 | 代表意义                                     |
| -------- | -------------------------------------------- |
| *        | 代表任何时刻都接受的意思                     |
| ,        | 代表分隔时段的意思                           |
| -        | 代表一段时间范围内                           |
| /n       | 那个n代表数字，亦即是【每隔n单位间隔】的意思 |

- 系统的配置文件：/etc/crontab 、/etc/cron.d/*

  > 1. 可以编辑/etc/crontab这个文件来执行【系统的例行性任务】；设置分为七栏，【分、时、日、月、周、执行者、命令】为其设置根据；
  > 2. crontab -e这个crontab其实是/usr/bin/crontab这个执行文件；分为六栏，【分、时、日、月、周、命令】为其设置根据；
  > 3. cron这个服务的最低检测限制是分钟，所以cron会每分钟去读取一次/etc/crontab与/var/spool/cron

- crond服务读取配置文件的位置

  > 跟系统的运行有关系的两个配置文件是/etc/crontab文件以及/etc/cron.d/*目录内的文件；
  >
  > 跟用户自己的任务有关系的配置文件，就是放在/var/spool/cron里面的文件；

  - /etc/crontab（是大家都能够读取的权限）
  - /etc/cron.d/*
  - /var/spool/cron/*

- crontab的基本应用

  - 个人话的操作使用【crontab -e】
  - 系统维护管理使用【vim /etc/crontab】
  - 自己开发软件使用【vim /etc/cron.d/newfile】：如果你是想要自己开发软件，当然最好就是使用全新的配置文件，并且放置于/etc/cron.d/目录内即可。
  - 固定每小时、每日、每周执行的特别任务：如果与系统运维有关，还是建议放置到/etc/crontab中集中管理较好。

###### anacron

> anacron是一个程序并非一个服务，配置文件放置在/etc/cron.hourly
>
> anacron存在的目的是，用于处理非24小时运行的Linux系统所执行的crontab，以及因为某些原因导致的超过时间而没有被执行的任务。
>
> 其实anacron也是每小时被crond执行一次，然后anacron再去检测相关的计划任务有没有被执行，如果有超过期限的任务，就执行该任务，执行完毕或无须执行任何任务时，anacron就停止。
>
> 由于anacron默认会以一天、七天、一个月为期去检测系统未执行的crontab任务，因此对于某些特殊的使用环境非常有帮助。
>
> anacron是怎么知道我们的系统啥时候关机的呢？这就要使用anacron读取的时间记录文件（timestamps）了。anacron会去分析现在的时间与时间记录文件所记载的上次执行anacron的时间，两者比较后发现有差异，那就是在某些时刻没有执行crontab，此时anacron就会开始执行未执行的crontab任务了。

- anacron [-sfn] \[-sfn] \[job] ..
- anacron的配置文件/etc/anacrontab



- 执行日志文件的轮询（logrotate）

  > logrotate的任务：将日志文件数据移动，让旧的数据与新的数据分别存放，让系统更有效地记录登陆信息，提高文件的读写性能。

- 日志文件分析logwatch的任务

  > 如果系统发生了软件问题、硬件错误、信息安全问题等，绝大部分的错误信息都会被记录到日志文件中。
  >
  > logwatch程序会主动分析登陆信息。

- 建立locate的数据库

  > 文件名数据库放置在/var/lib/mlocate中；
  >
  > 系统会主动地执行updatedb来更新数据库；

- manpage查询数据库的建立

  > 要使用manpage数据库，就要执行mandb才能建立好；

- RPM软件日志文件的建立

  > RPM数据库，将文件名作排序的记录

- 删除缓存

  > 系统通过计划任务执行名为tmpwatch的命令来删除缓存；

- 与网络服务有关的分析操作

  > 如果你安装了类似网站服务器的软件，那么你的Linux系统通常就会主动地分析该软件的日志文件。

##### 磁盘分区、挂载

- lsblk(list block device) 或者 lsblk -f：查看所有设备挂载情况
- df(disk free): 列出文件系统的整体磁盘使用量
  - -s	指定目录占用大小汇总
  - -h    带计量单位
  - -a    含文件
  - --max-depth=1    子目录深度
  - -c    列出明细的同时，增加汇总值
- du(disk usage): 查看文件系统的磁盘使用量（常用在查看目录所占磁盘空间）
- 

##### 网络配置

- ifconfig：查看网络配置

- ping：测试主机之间网络连通性

- lsof(list open files)是一个列出当前系统打开文件的工具

  - lsof -i:8000（查看服务器 8000 端口的占用情况）
    1. COMMAND:进程的名称；
    2. PID:进程标识符；
    3. USER:进程所有者；
    4. FD:文件描述符，应用程序通过文件描述符识别该文件；
    5. DEVICE:指定磁盘的名称；
    6. SIZE:文件的大小；
    7. NODE:索引节点（文件在磁盘上的标识）
    8. NAME:打开文件的确切名称
  - lsof abc.txt：显示开启文件abc.txt的进程
  - lsof -c abc：显示abc进程现在打开的文件
  - lsof -c -p 1234：列出进程号为1234的进程所打开的文件
  - lsof -g gid：显示归属gid的进程情况
  - lsof +d /usr/local/：显示目录下被进程开启的文件
  - lsof +D /usr/local/：同上，但是会搜索目录下的目录，时间较长
  - lsof -d 4：显示使用fd为4的进程
  - lsof -i -U：显示所有打开的端口和UNIX domain文件

- 网络环境配置

  - 第一种方法（自动获取）

    > 登录后，通过界面来设置自动获取ip，linux启动后会自动获取IP，缺点是每次自动获取的ip地址可能不一样。

  - 第二种方法（指定ip）

    > 直接修改配置文件来指定IP，并可以连接到外网
    >
    > 编辑：vi /etc/sysconfig/network-scripts/ifcig-ens33

- 设置主机名

  - hostname：查看主机名
  - 修改文件在/etc/hostname
  - 修改后，重启生效

- 设置hosts映射

  > hosts是什么？用来记录IP和Hostname(主机名)的映射关系
  >
  > 编辑：/etc/hosts

- DNS

  > Domain Name System的缩写，域名系统
  >
  > 是互联网上作为域名和IP地址相互映射的一个***分布式数据库***

##### 进程管理 
- 触发任何一个事件时，系统都会将它定义成为一个进程，并且给予这个进程一个ID，称为PID，同时根据触发这个进程的用户与相关属性关系，给予这个PID一组有效的权限设置。
- 执行一个程序或命令触发一个时间而获得一个PID
- 操作系统用过PID来判断进程是否具有执行权限。
- 当我们登录并执行bash时，系统已经给了我们一个PID，这个PID就是根据登陆者的UID/GID（/etc/passwd）而来。
- /bin/bash是一个程序，当被触发产生一个PID，之后后这个进程衍生出来的其他进程在一般状态下，也会沿用这个进程的相关权限。
- 在linux下面执行一个命令时，系统会将相关的权限、属性、进程代码与数据等均加载到内存，并给予这些进程一个进程标识符（PID），最终该命令可以执行的任务则与这个PID的权限有关。这就是linux的多人多任务的基础。
- 多人环境
	> 在linux 系统上面有多种不同的账号，每种账号都有其特殊的权限，只有一个账户具有至高无上的权力，那就是root（系统管理员）。除了root之外，其他人都必须要收一些限制，而每个人进入linux的环境设置都可以随着每个人的喜好来设置（~/.bashrc），每个人登录后获取的shell的PID不同
- 多任务操作：CPU在各个进程之间快速切换
- 多重登录环境的七个基本终端界面：
  > ALT+F1~F7来切换不同的终端界面，而且每个终端界面的登陆者还可以不同。
- 

###### 子进程与父进程
> 当我们登录系统后，会获取一个bash的shell，然后我们用这个bash提供的接口去执行另一个命令，那些另外执行的命令也会被触发称为PID，那个后来执行命令所产生的PID就是子进程，而在我们原本的bash环境下，就被称为父进程。
> 进程彼此之间是有相关性的。
> 某个进程的父进程通过Parent PID(PPID)来判断。
- fork and exec：程序调用的流程
	> linux的程序调用通常称为 fork-and-exec 的流程，进程都会借由父进程以复制（fork）的方式产生一个一模一样的子进程，然后被复制出来的子进程再以exec的方式来执行实际要执行的进程，最终就称为一个子进程。
- 系统或网络服务：常驻在内存的进程
	> 常驻在内存当中的进程通常都是负责一些系统所提供的功能以服务用户的各项任务，因此这些常驻进程就会被我们称为：服务（daemon）。
	> 系统本身所需要的服务：如crond、atd 以及 rsyslogd 等
	> 负责网络连接的服务：apache、named、postfix、vsftpd 等。网络服务被执行后，会启动一个可以负责网络监听的端口（port）以提供外部客户端（client）的连接请求。

###### ps(Process Status)：用来查看目前系统中，有哪些进程正在执行，以及它们执行的情况
```
ps -l：只能看自己bash的进程；
ps aux：查看系统所有的进程；
ps -lA：也是能够查看所有系统的进程；
ps axjf：连同部分进程树状态
选项与参数：
	-A：所有的进程均显示出来，与-e具有相同的效果；
	-a：不显示与终端有关的所有进程；
	-u：有效使用者（effective user）相关的进程；
	x：通常与a这个参数一起是个，可列出较完整信息
输出格式规划：
	l：较长、较详细的将该PID的信息列出；
	j：任务的格式（jobs format）；
	-f：做一个更为完整的输出
```

###### ps -l：仅查看自己的bash相关进程

- F：代表这个进程标识（process flags），说明这个进程的权限，常见号码有：
  - 若为4，表示此进程的权限为root；
  - 若为1，表示此子进程仅执行复制（fork），而没有实际执行（exec）
- S：代表这个进程的状态（STAT），主要的状态有：
  - R（Running）：该进程正在运行中；
  - S（Sleep）：该进程目前正在睡眠状态（idle），但可以被唤醒（signal）；
  - D：不可被唤醒的睡眠状态，通常这个进程可能在等待I/O的情况（ex>打印）；
  - T：停止状态（stop），可能是在任务空值（后台暂停）或跟踪（traced）状态；
  - Z（Zombie）：僵尸状态，进程已经终止但无法被删除至内存外
- UID/PID/PPID：代表【此进程被该UID所拥有/进程的PID号码/此进程的父进程PID号码】
- C：代表CPU使用率，单位为百分比
- PRI/NI：Priority[praɪˈɔːrəti]/Nice的缩写，代表此进程被CPU所执行的优先级，数值越小代表该进程越快被CPU执行。
- ADDR/SZ/WCHAN：都与内存有关，ADDR是kernel function，指出该进程在内存的哪个部分，如果是个running的进程，一般就会显示[ - ]；SZ代表此进程用掉多少内存；WCHAN表示目前进程是否运行，同样的，若为-表示正在运行中。
- TTY：登陆者的终端位置，若为远程登录则使用动态终端接口名称（pts/n）；
- TIME：使用的CPU时间，注意，是此进程实际话费CPU运行的时间，而不是系统时间；
- CMD：就是command的缩写，表示造成此进程的触发进程的命令是什么。

###### ps aux：查看系统所有进程

- USER：该进程属于所属用户账号；
- PID：该进程的进程ID；
- %CPU：该进程使用掉的CPU资源百分比；
- %MEM：该进程所占用的物理内存百分比；
- VSZ：该进程使用掉的虚拟内存量（KB）；
- RSS：该进程占用的固定的内存量（KB）；
- TTY：该进程是在哪个终端上面运行，若与终端无关则显示？另外，tty1-tty6是本机上面的登录进程，若为pts/0等，则表示是由网络连接进入主机的进程；
- STAT：该进程目前的状态，装填显示与ps -l的S的标识相同（R/S/T/Z）；
- START：该进程被触发启动的时间；
- TIME：该进程实际使用CPU运行的时间；
- COMMAND：该进程的实际命令是什么

###### ps axjf：列出类似进程树的进程显示

###### 僵尸（zombie [ˈzɑːmbi] ）进程

> 造成僵尸进程的原因在于该进程应该已经执行完毕，或是应该要终止了，但是该进程的父进程却无法完整地将该进程结束掉，而造成该进程一直存在内存当中；如果你发现在某个进程的CMD后面接上了\<defunct>时，就代表该进程是僵尸进程。

- 如果发现系统中有很多僵尸进程时，记得要找出该进程的父进程，然后好好做个追踪，好好进行主机的环境优化，看看有什么地方需要改善，不要只是直接将它kill掉；
- 通常僵尸进程都已经无法管理，而直接交给systemd这个进程来负责，偏偏systemd是系统第一个执行的进程，它是所有进程的父进程。如果产生僵尸进程，而系统过一阵子还没有用过内核非经常性的特殊处理来将该进程删除时，那只好通过reboot的方式来将该进程kill掉。

###### top：动态查看进程的变化

> 相比于ps是选取一个时间点的进程状态，top则可以持续监测进程运行的状态。

```
top [-d数字] | top [-bnp]
选项与参数：
-d：后面可以接秒数，就是整个进程界面更新的秒数，默认是5秒；
-b：以批量的方式执行top，还有更多的参数可以使用，通常会搭配数据流重定向来将批量的结果输出为文件；
-n：与-b搭配，意义是，需要执行几次top的输出结果；
-p：指定某些个PID来执行查看监测；
在top执行过程当中可以使用的按键命令：
	？：显示在top当中可以输入的按键命令；
	p：以CPU的使用排序显示；
	M：以Memory的使用排序显示；
	N：以PID来排序；
	T：由该进程使用的cpu时间累积（TIME+）排序；
	k：给予某个PID一个信号（signal）；
	r：给予某个PID重新制定一个nice值；
	q：退出top的按键
	
top上面的界面为整个系统的资源使用状态：
第一行（top...）：这一行显示的信息分别为：
	1.目前的时间；
	2.开机到目前为止所经过的时间；
	3.已经登录系统的用户人数；
	4.系统在1、5、15分钟的平均任务负载
第二行（Tasks...）：显示的是目前进程的总量与个别进程在什么状态（running,sleeping/stopped,zombie）
第三行（%CPU...）：显示的是CPU的整体负载，每个项目可使用？（问好）查看。
第四行与第五行：表示目前的物理内存与虚拟内存（Mem/Swap）的使用情况。
第六行：这个是在top进程当中输入命令时，显示状态的地方。

top下半部分的画面，则是每个进程使用的资源情况：
	1.PID：每个进程的ID；
	2.USER：该进程所属的用户；
	3.PR：Priority的间歇，与Priority有关，也是越小则越早被执行；
	4.NI：Nice的简写，与Priority有关，也是越小则越早被执行；
	5.%CPU：CPU的使用效率；
	6.%MEM：内存的使用效率；
	7.TIME+：CPU使用时间的累加
top默认使用CPU使用率（%CPU）作为排序的依据。如果想要使用内存使用率排序，则可以按下【M】，若要恢复则按下【P】即可。按下【q】退出top
```

###### pstree：查看进程树

```
pstree [-A|U] [-up]
选项与参数：
-A：各进程树之间的连接以ASCII字符来连接；
-U：各进程树之间的链接以Unicode的字符来连接，在某些终端界面下可能会有错误。
-P：并同时列出每个进程的PID；
-u：并同时列出每个进程的所属账号名称
所有的进程都是依附在systemd这个进程下面的。这个进程的PID是一号，因为它是由Linux内核所主动调用的第一个进程，所以PID就是一号了。
```

###### 任务管理 （job control）
> 执行任务管理的操作中，其实每个任务都是目前bash的子进程，即彼此之间是有相关性的，我们无法用任务管理的方式由tty1的环境去管理tty2的bash

- 执行bash的任务管理要注意的限制：
	- 这些任务所触发的进程必须来自于你shell的子进程（只管理自己的bash）
	- 前台：可以控制与执行命令的这个华宁称为前台的任务（foreground）
	- 后台：可以自动执行的任务，你无法使用ctrl + c终止它，可使用bg、fg调用该任务
	- 后台中执行的进程不能等待terminal 或shell 的输入（input）

- 直接将命令丢到后台中【执行】的 &	

- 将【目前】的任务丢到后台中【暂停】：[ctrl]-z

- 查看目前的后台任务状态：jobs

  ```shell
  jobs [-lrs]
  选项与参数：
  -l ：除了列出job number与命令串之外，同时列出PID的号码；
  -r ：仅列出正在后台run的任务；
  -s ：仅列出正在后台当中暂停（stop）的任务
  ```

- 将后台任务拿到前台处理：fg(foreground)

  ```
  fg %jobnumber
  fg: 默认取出那个+的任务
  ```

- 让任务在后台下的状态变成运行中：bg

  ```
  bg %jobnumber
  ```

- 管理后台当中的任务：kill

  ```
  kill -signal %jobnumber
  signal ：代表给予后面接的那个任务什么样的指示
  	-l(L的小写)：重新读取一次参数的配置文件（类似reload）；
  	-2：代表由键盘输入ctrl-c同样的操作；
  	-9：立刻强制删除一个任务；
  	-15：以正常的进程方式终止一项任务，与-9是不一样的
  ```

###### 脱机管理问题

> nohup：可以在退机或注销系统后，该能够让任务继续执行
>
> nohup [命令或参数] ：在终端前台中任务
>
> nohup [命令或参数] &：在终端后台中任务

###### 进程的优先级（Priority）与CPU调度

> Linux给予进程一个所谓的【优先级（priority, PRI）】，这个PRI值越低代表越优先的意思。不过这个PRI值是由内核动态调整的，用户无法直接调整PRI值。如果要调整进程的优先级，就要通过nice（NI）值。
>
> - nice值可调整的范围-20 ~ 19；
> - root可随意调整自己或他人进程的nice值，且范围为-20 ~ 19；
> - 一般用户仅可调整自己进程的nice值，且范围仅为0-19（避免一般用户抢占系统资源）；
> - 一般用户仅可将nice值越调越高

- 如何调整该进程的nice值？

  - 一开始执行进程就立即给予一个特定的nice值：用nice命令；

    ```
    nice [-n 数字] command
    -n:后面接一个数值，数值的范围-20 - 19；
    ```

  - 调整某个已经存在的PID的nice值：用renice命令；

    ```
    renice [number] PID
    ```
###### 查看系统资源信息

- free:查看内存使用情况

  ```
  # 显示目前系统的内存容量
  free -m
  ```

- uname:查看系统与内核相关信息
  - a：所有系统相关的信息，包括下面的数据都会被列出来；
  - s：系统内核名称；
  - r：内核的版本；
  - m：本系统的硬件架构；
  - p：cpu的类型；
  - i：硬件的平台（x86）

- uptime:查看系统启动时间与任务负载

- netstat:追踪网络或socket文件
  - a：将目前系统上所有的链接、监听、socket信息都列出来；
  - t：列出tcp网络封包的信息；
  - u：列出udp网络封包的信息；
  - n：不以进程的服务名称，以端口号（port number）来显示；
  - l：列出目前正在网络监听（listen）的服务：
  - p：列出该网络服务的进程PID；
    ```
    netstat 的结果显示了两个部分，分别是网络的链接，以及linux上面的socket进程相关部分
    一、因特网链接情况的部分：
    	Proto:网络的封包协议，主要分为TCP与UDP封包；
    	Recv-Q：非由用户进程链接到此socket的复制的总Bytes数；
    	Send-Q：非由远程主机传送过来的acknowledged总Byte数；
    	Local Address：本地端的IP:port情况；
    	Foreign Address：远程主机的IP:port情况；
    	State：链接状态，主要有建立（ESTABLISED）及监听（LISTEN）；
    二、socket文件的输出字段：
    	Proto：一般就是unix；
    	RefCnt：连接到此socker的进程数量；
    	Flags：连接的标识；
    	Type：socket存取的类型。主要有确认连接的STREAM与不需要确认的DGRAM两种；
    	State：若为CONNECTED则表示多个进程之间已经建立连接；
    	Path：连接到此socket的相关进程的路径，或是相关数据输出的路径；
    ```

- dmesg:分析内核产生的信息

- vmstat:检测系统资源变化

###### 终止进程kill和killall

- 进程是如何互相管理的？是通过给予该进程一个信号（signal）去告知该进程你想要让它做什么。kill -l

  | 代号 | 名称    | 内容                                                         |
  | ---- | ------- | ------------------------------------------------------------ |
  | 1    | SIGHUP  | 启动被终止的进程，可让该PID重新读取自己的配置文件，类似重新启动。 |
  | 2    | SIGINT  | 相当于用键盘输入ctrl+c来终端一个进程的运行                   |
  | 9    | SIGKILL | 代表强制终端一个进程的执行，如果该进程执行到一半，那么尚未完成的部分可能会有【半成品】产生，类似vim会有.filename.swp保留下来 |
  | 15   | SIGTERM | 以正常的方式结束进程来终止该进程。                           |
  | 19   | SIGSTOP | 相当于用键盘输入ctrl+z来暂停一个进程的运行。                 |

- kill -signal PID

  > kill可以帮我们将这个信号传送给某个任务（%number）或是某个PID（直接输入数字）

- 执行任务管理的操作中，其实每个任务都是目前bash的子进程，即彼此之间是有相关性的，我们无法用任务管理的方式有tty1的环境去管理tty2的bash。

- 可以出现提示字符让你操作的环境称为前台，至于其他任务就可以放入后台去暂停或运行；

- 放入后台的任务想要运行时，它必须不能够与用户进行交互，而且放入后台的任务不可以使用ctrl+c来终止；

###### /proc/* 代表的意义
> 进程都是在内存当中，而内存当中的数据又都是写入到/proc/*这个目录下。
> 基本上，目前主机上面的各个进程的PID都以目录的形式存在于/proc当中。

| 文件名            | 文件内容                                                     |
| ----------------- | ------------------------------------------------------------ |
| /proc/cmdline     | 加载内核时所执行的相关命令与参数，查看此文件，可了解命令是如何启动的 |
| /proc/cpuinfo     | 本机的CPU的相关信息，包含频率、类型与功能等                  |
| /proc/devices     | 这个文件记录了系统各个设备的主要设备代号，与mknod有关        |
| /proc/filesystems | 目前系统已经加载的文件系统                                   |
| /proc/interrupts  | 目前系统上面的IRQ分配状态                                    |
| /proc/ioports     | 目前系统上面各个设备所配置的I/O地址                          |
| /proc/kcore       | 内存的大小                                                   |
| /proc/loadavg     |                                                              |
| /proc/meminfo     | 使用free列出的内存信息，在这里也能够查看到                   |
| /proc/modules     | 目前我们的linux已经加载的模块列表，也可以想成是驱动程序      |
| /proc/swaps       | 到底系统挂载入的内存在哪里？使用的硬盘分区就记录再次         |
| /proc/partitions  | 使用fdisk -l会出现目前所有的硬盘分区吧？在这个文件当中也有记录 |
| /proc/uptime      | 就是用uptime的时候，会出现的信息                             |
| /proc/version     | 内核的版本，就是用uname -a 显示的内容                        |
| /proc/bus*        | 一些总线的设备，还有USB的设备也记录在此                      |

###### 服务（service）管理

> 服务(service)本质就是进程，但是是运行在后台，通常都会监听某个端口，等待其他程序的请求，又称为守护进程。

- systemctl/service 服务名 [start|stop|restart|status]

- service指令管理的服务在/etc/init.d查看

- 服务的运行级别(runlevel)：7种（主要3和5）

- 开机的流程说明

  ```
  开机 -> BIOS -> /boot -> systemd进程1 -> 运行级别 -> 运行级对应的服务
  ```

- chkconfig：给服务的各个运行级别设置自启动/关闭

  - chkconfig指令管理的服务在/etc/init.d查看
  - chkconfig的基本语法
    1. 查看服务 chkconfig --list [| grep xxx]
    2. chkconfig 服务名 --list
    3. chkconfig --level 5 服务名 on/off

- systemctl 管理指令

  > systemctl [start | stop | restart | status] 服务名
  >
  > systemctl 指令管理的服务在 /usr/lib/systemd/system 查看

- systemctl设置服务的自启动状态

  1. systemctl list-unit-files [| grep 服务名]	（查看服务开机启动状态，grep可以进行过滤）
  2. systemctl enable 服务名 （设置服务开机启动）
  3. systemctl disable 服务名 （关闭服务开机启动）
  4. systemctl is-enabled 服务名 （查询某个服务是否是自启动的）

- firewall 指令

  1. 打开端口：firewall-cmd --permanent --add-port=端口号/协议
  2. 关闭端口：firewall-cmd --permanent --remove-port=端口号/协议
  3. 重新载入才能生效：firewall-cmd --reload
  4. 查询端口号是否开放：firewall-cmd --query-port=端口/协议

###### 监控网络状态

> netstat [选项]
>
> -an：按一定顺序排列输出
>
> -p：显示哪个进程在调用
>
> 案例：请查看服务名为sshd的服务的信息
>
> netstat -anp | grep sshd

- netstat -tunlp 用于显示 tcp，udp 的端口和进程等相关情况

  ```
  netstat -tunlp | grep 端口号
  ```

  - -t (tcp) 仅显示tcp相关选项
  - -u (udp)仅显示udp相关选项
  - -n 拒绝显示别名，能显示数字的全部转化为数字
  - -l 仅列出在Listen(监听)的服务状态
  - -p 显示建立相关链接的程序名

- netstat -ntlp //查看当前所有tcp端口

  ```
  netstat -ntulp | grep 80 //查看所有80端口使用情况
  ```


##### RPM 与 YUM

> rpm用于互联网下载包的打包及安装工具；
>
> Yum是一个Shell前端软件包管理器。基于RPM包管理，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软件包。

- rpm -qa | grep xxx：查询已安装的rpm列表
  - rpm -qa：查询所安装的所有rpm软件包
  - rpm -q 软件包名：查询软件包是否安装
  - rpm -qi 软件包名：查询软件包中的文件
  - rpm -qf 文件全路径名：查询文件所属的软件包
- rpm -e RPM包的名称：卸载rpm包(erase：擦除)
  - rpm -e --nodeps rpm包的名称：可以强制卸载
- rpm -ivh RPM包全路径名称：安装rpm包
  - i=install 安装
  - v=verbose 提示
  - h=hash 进度条
- yum list | grep xxx：查询yum服务器是否有需要安装的软件
- yum install xxx：安装指定的yum包

###### yum常用命令
1. 列出所有可更新的软件清单命令：yum check-update

2. 更新所有软件命令：yum update

3. 仅安装指定的软件命令：yum install <package_name>

4. 仅更新指定的软件命令：yum update <package_name>

5. 列出所有可安裝的软件清单命令：yum list

6. 删除软件包命令：yum remove <package_name>

7. 查找软件包命令：yum search <keyword>

8. 清除缓存命令:
    yum clean packages: 清除缓存目录下的软件包
    yum clean headers: 清除缓存目录下的 headers
    yum clean oldheaders: 清除缓存目录下旧的 headers
    yum clean, yum clean all (= yum clean packages; yum clean oldheaders) :清除缓存目录下的软件包及旧的 headers
###### 配置国内yum源
- 首先备份/etc/yum.repos.d/CentOS-Base.repo
  ```
  mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
  ```
- 下载对应版本 repo 文件, 放入 /etc/yum.repos.d/ (操作前请做好相应备份)
  ```
  http://mirrors.163.com/.help/CentOS7-Base-163.repo
  mv CentOS6-Base-163.repo CentOS-Base.repo
  ```
- 运行以下命令生成缓存
  ```
  yum clean all
  yum makecache
  ```

##### APT软件管理

> apt 是 Advanced Packaging Tool的简称，是一款安装包管理工具。在Ubuntu下，我们可以使用apt命令进行软件包的安装、删除、清理等。

- sudo apt-get update：更新源
- sudo apt-get install package：安装包
- sudo apt-get remove package：删除包
- sudo apt-cache search package：搜索软件包
- sudo apt-cache show package：获取包的相关信息，如说明、大小、版本等
- sudo apt-get install package --reinstall：重新安装包
- sudo apt-get -f install：修复安装
- sudo apt-get remove package --purge：删除包，包括配置文件等
- sudo apt-get build-dep package：安装相关的编译环境
- sudo apt-get upgrade：升级系统
- sudo apt-cache depends package：了解使用该报依赖哪些包
- sudo apt-cache rdepends package：查看该报被哪些包依赖
- sudo apt-get source package：下载该包的源代码

###### apt-get 更新源

1. 备份

   ```
   sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
   ```

2. 更新源

   ```
   sudo vim /etc/apt/sources.list
   ```

3. 粘贴内容
- 清华

   ```
   # deb cdrom:[Ubuntu 16.04 LTS _Xenial Xerus_ - Release amd64 (20160420.1)]/ xenial main restricted
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial universe
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates universe
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial multiverse
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates multiverse
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security universe
   deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security multiverse
   ```
- 阿里源
	```
	deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse 
	deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse 
	deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse 
	deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse 
	deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse 
	deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse 
	deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse 
	deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse 
	deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse 
	deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
	```

4. 让更新源生效

   ```
   sudo apt-get update
   ```

5. 单独一次使用

   ```
   sudo apt-get update  更新源
   sudo apt-get upgrade 更新已安装的包
   ```

##### 远程登录Ubuntu

> SSH(secure Shell)：建立在应用层和传输层基础上的安全协议。
>
> SSH服务需要安装相应的***服务器和客户端***。

- sudo apt install net-tools：查看Ubuntu是否安装SSHD服务

- sudo apt-get install openssh-server：安装SSH服务器和客户端

- service sshd restart：启动sshd服务，会监听端口22

- 在windows使用XShell7和XFTP7登录Ubuntu

- 从一台linux系统远程登录另一台linux系统

  ```
  ssh 用户名@IP
  例如：ssh hspedu@192.168.0.1
  使用ssh访问出现错误时，可查看是否有文件 ~/.ssh/known_ssh，尝试删除该文件解决。
  
  登出：exit 或者 logout
  ```

##### 日志管理

###### 系统常用的日志

| :日志文件         | :说明                                                        |
| ----------------- | ------------------------------------------------------------ |
| /var/log/boot.log | 系统启动日志                                                 |
| /var/log/cron     | 记录与系统定时任务相关的日志                                 |
| /var/log/cups     | 记录打印信息的日志                                           |
| /var/log/dmesg    | 记录了系统在开机时内核自检的信息，也可以使用dmesg命令直接查看内核自检信息 |
| /var/log/btmp     | 记录错误登录的日志。这个文件是二进制文件，不能直接使用vi查看，而要使用lastb命令查看 |
| /var/log/lasllog  | 记录系统中所有用户最后一次的登录时间的日志。这个文件也是二进制文件，要使用lastlog命令查看 |
| /var/log/maillog  | 记录邮件信息的日志                                           |
| /var/log/message  | 记录系统重要信息的日志，这个日志文件中会记录linux系统的绝大多数信息。如果系统出现问题，首先要检查的应该就是这个日志文件 |
| /var/log/secure   | 记录验证和授权方面的信息，只要涉及账户和密码的程序都会记录，比如系统的登录，ssh的登录，su切换用户，sudo授权，甚至添加用户和修改用户密码都会记录在这个日志文件中。 |
| /var/log/wtmp     | 永久记录所有用户的登录、注销信息，同时记录系统的启动、重启、关机事件。是二进制文件，要使用lastlog查看。 |
| /var/log/ulmp     | 记录当前已经登录的用户的信息。这个文件会随着用户的登录和注销而不断变化，只记录当前登录用户的信息。这个文件不能用vi查看，而要使用w/who/users等命令查看 |

###### 日志管理服务 rsyslogd

- 查询linux中的rsyslogd服务是否启动

  ```
  ps aux | grep "rsyslog" | grep -v "grep"
  ```

- 查询rsyslogd服务的自启动状态

  ```
  systemctl list-unit-files | grep rsyslog
  ```

- 配置文件：/etc/rsyslog.conf

- 日志类型：

  | ：   | ：   |
  | ---- | ---- |
  |      |      |

- 日志级别：

  | ：   | ：   |
  | ---- | ---- |
  |      |      |

- 日志轮替

- logrotate 配置文件

##### 内核升级

- uname -a：查看当前的内核版本
- yum info kernel -q：检测内核版本，显示可以升级的内核
- yum update kernel：升级内核
- yum list kernel -q：查看已经安装的内核

##### vi/vim

###### 一般命令模式

> [[上下左右]按键移动光标、删除字符、删除整行、复制、粘贴等

- 光标的移动
  1. 上下左右箭头移动（n+箭头：即向指定方向移动n步）
  2. 向上向下翻页（ctrl+f、ctrl+b、ctrl+d、ctrl+u）
  3. +/-:光标移动到非空格符
  4. [home]/[end]:移动到当行的最前/后的字符处
  5. ctrl+Home/End:光标移动到本文件的第一行(gg)/最后一行
  6. nG:移动到本文件的地n行
- 查找与替换
  1. /word:向光标**之下**寻找一个名称为word的字符串；
  2. ?word:向光标之上寻找一个名称为word的字符串；
  3. n：重复前一个查找的操作；
  4. N：与n刚好相反；
  5. :n1,n2/word1/word2/g：在n1与n2行之间寻找word1这个字符串，并将该字符串替换为word2；
  6. :1,$s/word1/word2/g：从第一行到最后一行寻找word1字符串，并将该字符串替换为word2；
  7. :1,$s/word1/word2/gc：从第一行到最后一行寻找word1字符串，并将该字符串替换为word2，且在替换前显示提示字符给用户确认是否需要替换；
- 删除
  1. x与X：在一行中，x为向后删除一个字符；X为向前删除一个字符；
  2. nx/X：向后或向前删除n个字符；
  3. dd：删除（剪切）光标所在的那一整行；
  4. ndd：n为数字，删除（剪切）光标所在的向下n行；
  5. dnG：n为数字，删除（剪切）光标所在到第n行的所有数据；
  6. dG：删除（剪切）光标所在到最后一行的所有数据；
  7. d$：删除（剪切）光标所在处，到该行的最后一个字符；
  8. d0：删除（剪切）光标所在处，到该行的最前面一个字符；
- 复制
  1. yy：复制光标所在的那一行；
  2. nyy：n为数字，复制光标所在的向下n行；
  3. ynG：n为数字，复制光标所在到第n行的所有数据；
  4. yG：复制光标所在到最后一行的所有数据；
  5. y$：复制光标所在处，到该行的最后一个字符；
  6. y0：复制光标所在处，到该行的最前面一个字符；
- 其他常用操作
  1. 鼠标左键选取内容，右键粘贴至光标的后面（复制粘贴最快速的方式）；
  2. p与P：p为将已复制的数据在光标下一行粘贴；P则为贴在光标上一行；
  3. J：将光标所在行与下一行的数据结合成同一行；
  4. u：撤销，即恢复前一个操作；
  5. .：小数点，重做上一个操作

###### 编辑模式

> i 进入编辑模式；
>
> Esc 退出编辑模式或命令行模式

###### 命令行模式

> [: / ?] - 从一般模式进入命令行模式；
>
> 查找数据、读取、保存、批量替换字符、退出vi、显示行号等操作

- :w ：将编辑的数据写入硬盘文件中；
- :w!：若文件属性为【只读】时，强制写入该文件；
- :q ：退出vi；
- :q!：若曾修改过文件，又不想保存，使用！为强制退出不保存；
- :wq：保存后退出，若为:wq!则为强制保存后退出；
- ZZ：大写的z，若文件没有修改，则不保存退出；若文件已经被修改过，则保存后退出；
- :w [filename]：将编辑的数据保存成另一个文件，类似另存为新文件；
- :r [filename]：在编辑的数据中，读入另一个文件的数据，亦即将[filename]这个文件内容加到光标所在行后面；
- :set nu：显示行号，设置之后，会在每一行的前缀显示该行的行号；
- :set nonu：取消行号

###### vim多文件编辑

- vim file1 file2：使用vim打开两个文件；
- :n ：编辑下一个文件；
- :N ：编辑上一个文件；
- :files ：列出目前这个vim开启的所有文件

###### 多窗口功能

- :sp ：打开一个新窗口，如果有加filename，表示在新窗口创建一个新文件，否则表示两个窗口为同一个文件内容；
- ctrl+w+↑/↓：先按下ctrl不放，在按下w后放开所有的按键，之后再按下↑/↓，则光标可向上或下窗口移动；
- ctrl+w+q：先按下ctrl不放，在按下w后放开所有的按键，之后再按下q，即可退出光标所在的窗口

##### linux网络配置
###### 参数说明
| 环境变量    | 描述                                                       |
| ----------- | ---------------------------------------------------------- |
| http_proxy  | 为http变量设置代理；默认不填开头以http协议传输             |
| https_proxy | 为https变量设置代理                                        |
| ftp_proxy   | 为ftp变量设置代理                                          |
| all_proxy   | 全部变量设置代理，设置了这个时候上面的不用设置             |
| no_proxy    | 无需代理的主机或域名；可以使用通配符；多个时使用，号分隔。 |
###### 参数配置
```
export proxy="http://192.168.22.2:1080"
export http_proxy=$proxy
export https_proxy=$proxy
export ftp_proxy=$proxy
export no_proxy="localhost, 127.0.0.1, ::1"
```
###### 固定永久使用
- /etc/profile
- ~/.bashrc
- ~/.zshrc
- 在/etc.profile.d/文件夹下新建一个文件

##### Bash shell 的功能一

> 当我们树立在终端（tty）上面登录后，linux就会根据 /etc/passwd 文件的设置给我们一个shell（默认是bash），然后我们就可以根据下面的命令执行方式来操作shell

- history:历史命令

  ```
  ~./bash_history
  ```

- 命令与文件补全功能：Tab按键

  - [Tab]接在一串命令的第一个字的后面，则为命令补全；
  - [Tab]接在一串命令的第二个字的后面，则为文件补齐；
  - 若安装bash-completion软件，则在某些命令后面使用[Tab]按键时，可以进行【选项、参数的补齐】功能；

- 命令别名设置功能：（alias）

  ```
  alias lm='ls -al'
  ```

- 任务管理、前台、后台控制：（job control、foreground、background）

- 程序化脚本：（shell scripts）

- 通配符：（Wildcard）

  ```
  想要直到/usr/bin下面有多少X为开头的文件：
  ls -l /usr/bin/x*
  ```

- 查询命令是否为Bash shell的内置命令：type

###### echo：读取变量

```
需要在变量名称前面加上$ 或是以${变量}：
echo $PATH
echo $MAIL
```

- 变量的设置规则

  - 变量与变量内容以一个等号【=】来连接，如myname=VBird

  - 等号两边不能直接接空格

  - 变量名称只能是英文字母与数字，但是开头字符不能是数字

  - 变量内容若有空格可使用双引号【""】或单引号【''】将变量内容结合起来

    - 双引号内的特殊字符如$等，可以保有原本的特性；

      ```
      var="lang is $LANG" 则echo $var 可得lang is zh_CN.UTF-8
      ```

    - 单引号内的特殊字符则仅为一般字符（纯文本）；

      ```
      var="lang is $LANG" 则echo $var 可得lang is $LANG
      ```

  - 可用转义符【/】将特殊符号（如 [Enter]、$、\、空格、`等）变成一般字符；

  - 在一串命令的执行中，还需要借由其他额外的命令所提供的信息时，可以使用返单号（``）或【$(命令)】；

  - 若该变量为扩增变量内容时，则可用"$变量名称" 或 \${变量}累加内容：

    ```
    PATH="$PATH":/home/bin 或 PATH=${PATH}:/home/bin
    cd /lib/modules/$(uname -r)/kernel/
    ```

  - 若该变量需要在其他子程序执行，则需要以export来使变量变成环境变量：export PATH

  - 取消变量的方法：unset 变量名称

###### 命令的执行与快速编辑按钮

- ctrl + u：从光标处向前删除命令串
- ctrl + k：从光标处向后删除命令串
- ctrl + a：让光标移动到整个命令串的最前面；
- ctrl + e：让光标移动到整个命令串的最后面；

###### 环境变量(type env /usr/bin/env)

- env：观察环境变量与常见环境变量说明；

  - HOME

    > 代表用户的根目录。使用cd ~返回根目录

  - SHELL

    > 告知我们目前这个环境使用的SHELL是哪个程序

  - HISTSIZE

    > 与历史命令有关，即曾经执行过的命令可以被系统记录下来，而记录的条数则是由这个值来设置。

  - MAIL

    > 当我们使用mail这个命令在收信时，系统会去读取的邮箱文件（mailbox）

  - PATH

    > 执行文件查找的路径，目录与目录中间以冒号（:）分隔，由于文件的查找是依序由PATH的变量内的目录来查询，所以，目录的顺序也是重要的。

  - LANG

    > 语序数据

  - RANDOM（/dev/random）

    > 随机数的变量。

- set：观察所有变量（含环境变量与自定义变量）

- export：自定义变量转成环境变量

  ```
  将自定义变量转成环境变量：
  export 变量名称

  列出所有的环境变量：export
  ```

  - 子进程仅会继承父进程的环境变量，子进程不会继承父进程的自定义变量；
  - 当启动一个shell，操作系统会分配一内存区域给shell使用，此内存中的变量可让子进程使用；
  - 若在父进程利用export功能，可以让自定义变量的内容写到上述的内存区域当中（环境变量）；
  - 当加载另一个shell时（即启动子进程，而离开原本的父进程），子shell可以将父shell的环境变量所在的内存区域导入自己的环境变量区块当中。

- declare、typeset：声明变量的类型

  ```
  1. 让变量sum进行100+200+300的求和结果：
  declare -i sum=100+200+300
  2. 将sum变成环境变量：
  declare -x sum
  3. 让sum变成只读属性，不可修改：
  declare -r sum
  4. 让sum变成非环境变量的自定义变量：
  declare +x sum （将-变成+可以进行【取消】操作）
  ```

- locale：影响显示结果的语系变量

- read：读取来自键盘输入的变量

- 数组（array）变量类型

  ```
  var[index]=content
  ```

###### 与文件系统及程序的限制关系：ulimit

> 我们的bash是可以限制用户的某些系统资源的，包括可以开启的文件数量，可以使用的CPU时间，可以使用的内存总量等。

```
列出你目前身份的所有限制数据数值：
ulimit -a
限制使用者仅能建立10MBytes以下的容量的文件：
ulimit -f 10240
```

###### 命令别名与历史命令

- 命令别名设置：alias、unalias

  ```
  1. 列出目前拥有的命令别名：
  alias
  2. 设置命令别名：
  alias rm='rm -i'
  3. 删除命令别名：
  unalias lm
  ```

- 历史命令：history（~/.bash_history）

  - !number：执行第几条命令的意思
  - !command：由最近的命令向前查找【命令串开头为command】的那个命令，并执行
  - !!：执行上一个命令（相当于按向上键后，按回车）

###### 路径与命令查找顺序

> 查看命令查找顺序：type -a 命令名称

1. 以相对/绝对路径执行命令；
2. 由alias找到该命令来执行；
3. 由bash内置的builtin命令来执行；
4. 通过$PATH这个变量的顺序找到的第一个命令来执行；

###### bash 的登录与欢迎信息：/etc/issue、/etc/motd

| 标识符 | 含义                             |
| ------ | -------------------------------- |
| \d     | 本地端时间的日期                 |
| \l     | 显示第几个终端界面               |
| \m     | 显示硬件的等级                   |
| \n     | 显示主机的网络名称               |
| \O     | 显示domain name                  |
| \r     | 操作系统的版本（相当于uname -r） |
| \t     | 显示本地端时间的时间             |
| \S     | 操作系统的名称                   |
| \v     | 操作系统的版本                   |

###### bash的环境配置文件

- login 与 non-login shell

  - login shell：取得bash时需要完整的登录流程；
  - non-login shell：取得bash的方法不需要重复登录的操作；
  - /etc/profile：这是系统整体的设置，最好不要修改这个文件；
  - ~/.bash_profile 或~/.bash_login 或~/.profile：属于用户个人设置；

- /etc/profile（login shell 才会读）

- /etc/profile.d/*.sh

- /etc/locale.conf

- /usr/share/bash-completion/completions/*

- ~/.bash_profile（login shell 才会读）

- source：读入环境配置文件的命令

  ```
  将家目录的~/.bashrc的设置读入目前的bash环境中：
  source ~/.bashrc
  或 . ~/.bashrc
  ```

- ~/.bashrc（non-login shell 会读）

- /etc/man_db.conf

- ~/.bash_history

- ~/.bash_logout

###### 通配符与特殊符号

| 符号                                                   | 意义                                                         |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| *                                                      | 代表【0个到无穷多个】任意字符                                |
| ?                                                      | 代表【一定有一个】任意字符                                   |
| []                                                     | 代表【一定有一个在括号内】的字符（非任意字符）               |
| [ - ]                                                  | 若有减号在中括号内时，代表【在编码顺序内的所有字符】。例如[0-9] |
| [^ ]                                                   | 若中括号内的第一个字符为指数符号（^），那表示【反向选择】    |
| #                                                      | 注释符号                                                     |
| \                                                      | 转义符                                                       |
| \|                                                     | 管道（pipe）：分隔两个管道命令的符号                         |
| ;                                                      | 连续命令执行分隔符：连续性命令的界定                         |
| ~                                                      | 用户的家目录                                                 |
| $                                                      | 使用变量前导符：亦即是变量之前需要加的变量替换值             |
| &                                                      | 任务管理（job control）：将命令变成后台任务                  |
| !                                                      | 逻辑运算意义上的【非】not 的意思                             |
| /                                                      | 目录符号：路径分隔的符号                                     |
| >、>>                                                  | 数据流重定向：输出定向，分别是【替换】与【累加】             |
| <、<<                                                  | 数据流重定向：输入定向                                       |
| ''                                                     | 单引号，不具有变量替换的功能（$变为纯文本）                  |
| ""                                                     | 双引号，具有变量替换的功能（$ 可保留相关功能）               |
| ``    | 两个【``】中间为可以先执行的命令，亦可使用$( ) |                                                              |
| ( )                                                    | 在中间为子shell的起始与结束                                  |
| {}                                                     | 在中间为命令区块的组合                                       |

##### Bash shell 的功能二

> 当我们树立在终端（tty）上面登录后，linux就会根据 /etc/passwd 文件的设置给我们一个shell（默认是bash），然后我们就可以根据下面的命令执行方式来操作shell

- history:历史命令

  ```
  ~./bash_history
  ```

- 命令与文件补全功能：Tab按键

  - [Tab]接在一串命令的第一个字的后面，则为命令补全；
  - [Tab]接在一串命令的第二个字的后面，则为文件补齐；
  - 若安装bash-completion软件，则在某些命令后面使用[Tab]按键时，可以进行【选项、参数的补齐】功能；

- 命令别名设置功能：（alias）

  ```
  alias lm='ls -al'
  ```

- 任务管理、前台、后台控制：（job control、foreground、background）

- 程序化脚本：（shell scripts）

- 通配符：（Wildcard）

  ```
  想要直到/usr/bin下面有多少X为开头的文件：
  ls -l /usr/bin/x*
  ```

- 查询命令是否为Bash shell的内置命令：type

- last：列出目前与过去登入系统的用户相关信息

- id username：将每个账号内容显示出来

###### echo：读取变量

```
需要在变量名称前面加上$ 或是以${变量}：
echo $PATH
echo $MAIL
```

- 变量的设置规则

  - 变量与变量内容以一个等号【=】来连接，如myname=VBird

  - 等号两边不能直接接空格

  - 变量名称只能是英文字母与数字，但是开头字符不能是数字

  - 变量内容若有空格可使用双引号【""】或单引号【''】将变量内容结合起来

    - 双引号内的特殊字符如$等，可以保有原本的特性；

      ```
      var="lang is $LANG" 则echo $var 可得lang is zh_CN.UTF-8
      ```

    - 单引号内的特殊字符则仅为一般字符（纯文本）；

      ```
      var="lang is $LANG" 则echo $var 可得lang is $LANG
      ```

  - 可用转义符【/】将特殊符号（如 [Enter]、$、\、空格、`等）变成一般字符；

  - 在一串命令的执行中，还需要借由其他额外的命令所提供的信息时，可以使用返单号（``）或【$(命令)】；

  - 若该变量为扩增变量内容时，则可用"$变量名称" 或 \${变量}累加内容：

    ```
    PATH="$PATH":/home/bin 或 PATH=${PATH}:/home/bin
    cd /lib/modules/$(uname -r)/kernel/
    ```

  - 若该变量需要在其他子程序执行，则需要以export来使变量变成环境变量：export PATH

  - 取消变量的方法：unset 变量名称

###### 命令的执行与快速编辑按钮

- ctrl + u：从光标处向前删除命令串
- ctrl + k：从光标处向后删除命令串
- ctrl + a：让光标移动到整个命令串的最前面；
- ctrl + e：让光标移动到整个命令串的最后面；

###### 环境变量(type env /usr/bin/env)

- env：观察环境变量与常见环境变量说明；

  - HOME

    > 代表用户的根目录。使用cd ~返回根目录

  - SHELL

    > 告知我们目前这个环境使用的SHELL是哪个程序

  - HISTSIZE

    > 与历史命令有关，即曾经执行过的命令可以被系统记录下来，而记录的条数则是由这个值来设置。

  - MAIL

    > 当我们使用mail这个命令在收信时，系统会去读取的邮箱文件（mailbox）

  - PATH

    > 执行文件查找的路径，目录与目录中间以冒号（:）分隔，由于文件的查找是依序由PATH的变量内的目录来查询，所以，目录的顺序也是重要的。

  - LANG

    > 语序数据

  - RANDOM（/dev/random）

    > 随机数的变量。

- set：观察所有变量（含环境变量与自定义变量）

- export：自定义变量转成环境变量

  ```
  将自定义变量转成环境变量：
  export 变量名称

  列出所有的环境变量：export
  ```

  - 子进程仅会继承父进程的环境变量，子进程不会继承父进程的自定义变量；
  - 当启动一个shell，操作系统会分配一内存区域给shell使用，此内存中的变量可让子进程使用；
  - 若在父进程利用export功能，可以让自定义变量的内容写到上述的内存区域当中（环境变量）；
  - 当加载另一个shell时（即启动子进程，而离开原本的父进程），子shell可以将父shell的环境变量所在的内存区域导入自己的环境变量区块当中。

- declare、typeset：声明变量的类型

  ```
  1. 让变量sum进行100+200+300的求和结果：
  declare -i sum=100+200+300
  2. 将sum变成环境变量：
  declare -x sum
  3. 让sum变成只读属性，不可修改：
  declare -r sum
  4. 让sum变成非环境变量的自定义变量：
  declare +x sum （将-变成+可以进行【取消】操作）
  ```

- locale：影响显示结果的语系变量

- read：读取来自键盘输入的变量

- 数组（array）变量类型

  ```
  var[index]=content
  ```

###### 与文件系统及程序的限制关系：ulimit

> 我们的bash是可以限制用户的某些系统资源的，包括可以开启的文件数量，可以使用的CPU时间，可以使用的内存总量等。

```
列出你目前身份的所有限制数据数值：
ulimit -a
限制使用者仅能建立10MBytes以下的容量的文件：
ulimit -f 10240
```

###### 命令别名与历史命令

- 命令别名设置：alias、unalias

  ```
  1. 列出目前拥有的命令别名：
  alias
  2. 设置命令别名：
  alias rm='rm -i'
  3. 删除命令别名：
  unalias lm
  ```

- 历史命令：history（~/.bash_history）

  - !number：执行第几条命令的意思
  - !command：由最近的命令向前查找【命令串开头为command】的那个命令，并执行
  - !!：执行上一个命令（相当于按向上键后，按回车）

###### 路径与命令查找顺序

> 查看命令查找顺序：type -a 命令名称

1. 以相对/绝对路径执行命令；
2. 由alias找到该命令来执行；
3. 由bash内置的builtin命令来执行；
4. 通过$PATH这个变量的顺序找到的第一个命令来执行；

###### bash 的登录与欢迎信息：/etc/issue、/etc/motd

| 标识符 | 含义                             |
| ------ | -------------------------------- |
| \d     | 本地端时间的日期                 |
| \l     | 显示第几个终端界面               |
| \m     | 显示硬件的等级                   |
| \n     | 显示主机的网络名称               |
| \O     | 显示domain name                  |
| \r     | 操作系统的版本（相当于uname -r） |
| \t     | 显示本地端时间的时间             |
| \S     | 操作系统的名称                   |
| \v     | 操作系统的版本                   |

###### bash的环境配置文件

- login 与 non-login shell

  - login shell：取得bash时需要完整的登录流程；
  - non-login shell：取得bash的方法不需要重复登录的操作；
  - /etc/profile：这是系统整体的设置，最好不要修改这个文件；
  - ~/.bash_profile 或~/.bash_login 或~/.profile：属于用户个人设置；

- /etc/profile（login shell 才会读）

- /etc/profile.d/*.sh

- /etc/locale.conf

- /usr/share/bash-completion/completions/*

- ~/.bash_profile（login shell 才会读）

- source：读入环境配置文件的命令

  ```
  将家目录的~/.bashrc的设置读入目前的bash环境中：
  source ~/.bashrc
  或 . ~/.bashrc
  ```

- ~/.bashrc（non-login shell 会读）

- /etc/man_db.conf

- ~/.bash_history

- ~/.bash_logout

###### 通配符与特殊符号

| 符号                                                   | 意义                                                         |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| *                                                      | 代表【0个到无穷多个】任意字符                                |
| ?                                                      | 代表【一定有一个】任意字符                                   |
| []                                                     | 代表【一定有一个在括号内】的字符（非任意字符）               |
| [ - ]                                                  | 若有减号在中括号内时，代表【在编码顺序内的所有字符】。例如[0-9] |
| [^ ]                                                   | 若中括号内的第一个字符为指数符号（^），那表示【反向选择】    |
| #                                                      | 注释符号                                                     |
| \                                                      | 转义符                                                       |
| \|                                                     | 管道（pipe）：分隔两个管道命令的符号                         |
| ;                                                      | 连续命令执行分隔符：连续性命令的界定                         |
| ~                                                      | 用户的家目录                                                 |
| $                                                      | 使用变量前导符：亦即是变量之前需要加的变量替换值             |
| &                                                      | 任务管理（job control）：将命令变成后台任务                  |
| !                                                      | 逻辑运算意义上的【非】not 的意思                             |
| /                                                      | 目录符号：路径分隔的符号                                     |
| >、>>                                                  | 数据流重定向：输出定向，分别是【替换】与【累加】             |
| <、<<                                                  | 数据流重定向：输入定向                                       |
| ''                                                     | 单引号，不具有变量替换的功能（$变为纯文本）                  |
| ""                                                     | 双引号，具有变量替换的功能（$ 可保留相关功能）               |
| ``    | 两个【``】中间为可以先执行的命令，亦可使用$( ) |                                                              |
| ( )                                                    | 在中间为子shell的起始与结束                                  |
| {}                                                     | 在中间为命令区块的组合                                       |

###### 数据流重定向

- standard output（标准输出STDOUT） 与 standard error output（标准错误输出STDERR）

  - 标准输出指的是命令执行所返回的正确信息；
  - 标准错误输出可理解为命令执行失败后，所返回的错误信息；

- standard input 标准输入（stdin）：代码为0，使用< 或 <<；

  > 将原本需要由键盘输入的数据，改由文件内容类替换；

  ```
  cat > catfile < ~.bashrc
  ```

  - <<：结束的输入字符

    ```
    cat > catfile << "eof"
    输入eof这个关键词，立刻就结束而不需要输入ctrl + d.
    ```

    

- 标准输出（stdout）：代码为1，使用> 或 >>；

  - 1>：以覆盖的方法将【正确的数据】输出到指定的文件或设备上；
  - 1>>：以累加的方法将【正确的数据】输出到指定的文件或设备上；

- 标准错误输出（stderr）：代码为2，使用2> 或 2>>；

  - 2>：以覆盖的方法将【错误的数据】输出到指定的文件或设备上；
  - 2>>：以累加的方法将【错误的数据】输出到指定的文件或设备上；

- /dev/null 垃圾桶黑洞设备与特殊写法

  ```
  find /home -name .bashrc 2> /dev/null
  ```

- 2>&1：将正确与错误数据统统写入同一个文件中

  ```
  echo "erro message" 2> /dev/null 1>&2
  ```

###### 命令执行的判断根据：;、&&、||

###### 管道命令（pipe）

> 管道命令|仅能处理经由前面一个命令传来的正确信息，也就是标准输出的信息，对于标准错误并没有直接处理的能力。

###### 选取命令：cut、grep

> 将一段数据经过分析后，取出我们想要的，或是由分析关键词，取得我们所想要的那一行；
>
> 选取信息通常是针对【一行一行】来分析的。

- cut

  > 将一段信息的某一段切出来，处理的信息是以行为单位的；

  ```
  将PATH变量取出，然后找出第三，五个路径：
  echo ${PATH} | cut -d ':' -f 3,5
  ```

- grep

  > 分析一行信息，若当中有我们所需要的信息，就将该行拿出来。
  >
  > grep [-acinv] \[--color=auto] '查找字符' filename

###### 排序命令：sort、wc、uniq

- sort：根据不同的数据形式来排序；

- uniq：将重复的数据仅列出一个显示；

- wc：查看文件里面与多少字、多少行、多少字符；

  ```
  wc [-lwm] filename
  -l: 仅列出行；
  -w: 仅列出多少字（英文字母）；
  -m: 多少字符；
  ```

###### 双向重定向：tee

> tee会同时将数据流分送到文件与屏幕，而输出到屏幕的，其实就是stdout
>
> tee [-a] file

###### 字符转换命令：tr、col、join、paste、expand

- tr：可以用来删除一段信息当中的文字，或是进行文字信息的替换

  - -d：删除信息当中的SET1这个字符；
  - -s：踢馆掉重复的字符；

  ```
  1. 将last输出的信息中，所有的小写变成大写字符：
  last | tr '[a-z]' '[A-Z]'
  2. 将/etc/passwd输出的信息中，将冒号（:）删除：
  cat /etc/passwd | tr -d ':'
  ```

- col：可以用来简单地处理将tab按键替换称为空格键

  ```
  利用cat -A显示出所有特殊按键，最后以col将tab转成空白：
  cat -A /etc/man_db.conf 此时会看到很多^I的符号，那就是tab
  cat -A /etc/man_db.conf | col -x | cat -A | more
  ```

- join：处理两个文件之间的数据，在两个文件当中，有相同数据的那一行，才将它加在一起

  ```
  join [-til2] file1 file2
  在使用join之前，需要处理的文件应该要事先经过排序sort处理。
  ```

- paste：直接将两行贴在一起，且中间以tab键隔开

  ```
  paste [-d] file1 file2
  ```

- expand：将tab按键转成空格键

###### split：划分命令

> 将一个大文件，依据文件大小或行数来划分，就可以将大文件划分称为小文件。

- -b：后面可接欲划分成的文件大小，可加单位，例如b、k、m等。
- -l：以行数来进行划分。
- PREFIX：代表前缀字符的意思，可作为划分文件的前缀文字。

```
将/etc/services分成300k一个文件：
split -b 300k /etc/services services
```

###### 参数代换：xargs

> 产生某个命令的参数，xargs可以读入stdin的数据，并且以空格符或换行符作为识别符，将stdin的数据分隔成为参数。

- -0：如果输入的stdin含有特殊字符，例如`、\、空格等字符时，这个-0参数可以将它还原成一般字符，这个参数可以用于特殊状态。
- -e：这是EOF（end of file）的意思，后面可以接一个字符，当xargs分析到这个字符时，就会停止工作。
- -p：在执行每个命令时，都会询问使用者的意思。
- -n：后面接次数，每次command命令执行时，要使用几个参数的意思。

```
将/etc/passwd内的第一栏取出，仅取三行，使用id这个命令将每个账号内容显示出来：
cut -d ':' -f 1 /etc/passwd | head -n 3 | xargs -p -n 1 id
```

###### 关于减号【-】的用途

> 在管道命令当中，常常会使用到前一个命令的stdout作为这次的stdin，某些命令需要用到文件名（例如tar）来进行处理时，该stdin与stdout可以利用减号"-"来替代。

```
tar -cvf - /home | tar -xvf - -C /tmp/homeback
意思是将/home里面的文件给它打包，但打包的数据不是记录到文件，而是传送到stdout，经过管道后，将tar -cvf - /home 传送给后面的tar -xvf -
```

##### linux使用者

- 每个登录的用户至少都会获取两个ID，一个时用户ID（User ID，简称UID），一个是用户组ID（Group ID，简称GID），配置文件在 /etc/passwd 和 /etc/group。详细参考man 5 passwd 及 man 5 shadow

###### 用户账号

- 用户登录的时候，系统做了哪些处理？

  - 先查找/etc/passwd里面是否有你输入的账号？如果没有则退出，如果有的话则将该账号对应的UDI与GID（在/etc/group中）读出来，另外，该账号的家目录与shell设置也一并读出。
  - 再来则是核对密码表。这是linux会进入/etc/shadow里面找出对应的找好与UID，然后核对一下你刚刚输入的密码与里面的密码是否相符
  - 如果一切都OK的话，就进入shell管理的阶段。

- /etc/passwd文件结构

  > 每一行都代表一个账号，有几行就代表有几个账号在你的系统中。
  >
  > 需要特别留意的是，里面很多账号本来就是系统正常运行所必须的，称为系统账号，如bin/daemon/adm/nobody等，这些账号请不要随意删除。
  >
  > 每一行使用:分隔开，共有七个东西分别是：

  1. 账号名称

  2. 密码：x，因为安全问题已将这个字段的数据改放到/etc/shadow中

  3. UID：用户标识符

     - 0：系统管理员

     - 1~999：系统账号

       > 1~200：有linux发行版自行建立的系统账号；
       >
       > 201~999：若用户有系统账号需求时，可以使用的账号UID；

     - 1000~60000：可登录账号

  4. GID：用户组标识符

  5. 用户信息说明栏

  6. 家目录

  7. shell

     > 当用户登录系统后就会获取一个shell来与系统的内核沟通以进行用户的操作任务。
     >
     > 有一个shell可以使账号在登录时无法获得shell环境，那就是/sbin/nologin

- /etc/shadow文件结构

  > 程序的运行都与权限有关，而权限与UID 和 GID有关。因此个程序当然需要读取/etc/passwd来了解不同账号的权限。
  >
  > shadow同样以【:】作为分隔符，共有九个字段：

  1. 账号名称，与/etc/passwd相同

  2. 密码：在此字段前加上！或*修改密码字段，就会让密码暂时失效

  3. 最近修改密码的日期

  4. 密码不可被修改的天数（与第三字段相比）

  5. 密码需要重新修改的天数（与第三字段相比）

  6. 密码需要修改期限前的警告天数（与第五字段相比）

  7. 密码过期后的账号宽限时间（密码失效日，与第五字段相比）

     > 密码过期了，当你登录系统时，系统会强制你必须要重新设置密码才能登录继续使用。
     >
     > 密码过期几天后，如果用户还是没有登录更改密码，那么这个账号的密码将会失效，密码过期与密码失效并不相同。

  8. 张瑶失效日期：这个账号在此字段规定的日期之后，将无法再使用。

  9. 保留

- /etc/group文件结构

  1. 组名
  2. 用户组密码：已经移动到/etc/gshadow中，因此这个字段只会存在一个【x】
  3. GID：/etc/passwd第四个字段使用的GID对应的用户组名
  4. 此用户组支持的账号名称

- groups：有效与支持用户组的观察，第一个输出的用户组即为有效用户组

- newgrp：有效用户组的切换，切换的用户组必须是已经支持的用户组

- /etc/gshadow：建立用户组管理员

  1. 组名
  2. 密码栏，同样的，开头为！表示无合法密码，所以无用户组管理员
  3. 用户组管理员的账号
  4. 有加入该用户组支持的所属账号（与/etc/group内容相同）

###### 账号管理

- useradd：新建账号

  - 在/etc/passwd里面建立一行与账号相关的数据，包括建立UID/GID家目录等；
  - 在/etc/shadow里面将此账号的密码相关参数写入，但是尚未有密码；
  - 在/etc/group里面加入一个与账号名称一模一样的组名；
  - 在/home下面建立一个与账号同名的目录作为用户家目录，且权限为700；

- useradd -D

  | 参数                  | 说明                                |
  | --------------------- | ----------------------------------- |
  | GROUP=100             | 默认的用户组                        |
  | HOME=/home            | 默认的家目录所在目录                |
  | INACTIVE=-1           | 密码失效日，在shadow内的第7栏       |
  | EXPIRE=               | 账号失效日，在shadow内的第8栏       |
  | SHELL=/bin/bash       | 默认的shell                         |
  | SKEL=/etc/skel        | 使用者家目录的内容数据参考目录      |
  | CREATE MAIL SPOOL=yes | 是否主动帮使用者建立邮箱（mailbox） |

- passwd

  > 使用useradd建立账号后，在默认的情况下，该账号时暂时被锁定的。

  - passwd 账号：帮一般账号建立密码；
  - passwd：修改自己的密码

- chage

- usermod：微调useradd增加的用户参数

- userdel

  - 用户账号/密码相关参数：/etc/passwd、/etc/shadow
  - 用户组相关参数：/etc/group、/etc/gshadow
  - 用户个人文件数据：/home/username、/var/spool/mail/username

###### 用户功能

- id：查询某人或自己的相关UID/GID等信息

- finger：查看很多用户相关的信息

- chfn

- chsh(change shell)

  ```
  设置修改自己的shell:
  chsh -s /bin/bash
  ```

###### 新增与删除用户组

> 基本上，用户组的内容都与两个文件有关：/etc/group、/etc/gshadow

- groupadd：新建用户组
- groupmod：修改用户组
- groupdel：删除用户组
- gpasswd

###### 用户身份切换

- su
- sudo
  1. 当用户执行sudo时，系统于/etc/sudoers文件中查找该用户是否有执行sudo的权限；
  2. 若用户具有可执行sudo 的权限后，便让用户【输入用户自己的密码】来确认；
  3. 若密码输入成功，便开始进行sudo 后续接的命令（但root执行sudo 时，不需要输入密码）；
  4. 若欲切换的身份与执行者身份相同，那也不需要输入密码。
- visudo与/etc/sudoers
  1. 【用户账号】：操作系统的哪个账号可以使用sudo这个命令；
  2. 【登陆者的来源主机名】：可以指定客户端计算机
  3. 【可切换的身份】：这个账号可以切换成什么身份来执行后续的命令；
  4. 【可执行的命令】：可用该身份执行什么命令？这个命令请务必使用绝对路径；

###### linux主机上的用户信息传递

- 查询用户：w、who、last、lastlog

  - w/who：查看目前已登录在系统上面的用户

- 用户对谈：write、mesg、wall

  - write 使用者账号 [使用者所在终端界面]，ctrl -d结束输入
  - mesg：不接受任何信息

- 用户邮箱：mail

  ```
  mailbox在/var/spool/mail/username
  mail -s "邮件标题" username@localhost
  结束时，最后一行输入小数点.即可
  数据流重定向：mail -s "nice to meet you" vbird < filename
  ```

##### 认识系统服务（daemon）

###### init的管理机制（/etc/init.d）

- 服务的启动、关闭、与查看等方式

  > 所有的服务启动脚本放置于/etc/init.d/目录

  - 启动：/etc/init.d/daemon start
  - 关闭：/etc/init.d/daemon stop
  - 重新启动：/etc/init.d/daemon restart
  - 查看状态：/etc/init.d/daemon status

- 服务启动的分类

  - 独立启动模式：服务独立启动，该服务直接常驻于内存中，提供本机或用户的服务操作，反应速度快
  - 超级守护进程：由特殊的xinetd或inetd这两个总管程序提供socket对应或端口对应的管理。

- 服务的依赖性问题

- 运行级别的分类

  > init是启动后内核主动调用的，然后init可以根据用户自定义的运行级别来唤醒不同的服务，以进入不同的操作界面。
  >
  > 基本上linux提供7个运行级别，分别是0、1、2、3、4、 5、6，比较重要的是1）单人维护模式、3）纯命令行模式、5）图形界面。
  >
  > 各个运行级别的启动脚本是用过/etc/rc[0-6].d/Sxxdaemon 链接到/etc/init.d/daemon，链接文件名（SXXdaemon）的功能为：S为启动该服务，XX是数字，为启动的顺序。

- 制定运行级别默认要启动的服务

  - 默认要启动：chkconfig daemon on
  - 默认不启动：chkconfig daemon off
  - 查看默认为启动与否：chkconfig --list daemon

- 运行级别的切换操作：init 5

###### systemd的使用

- systemd的配置文件放置目录

  > 到底操作系统启动会不会执行某些服务其实看/etc/systemd/system/下面的设置，所以该目录下面是一大堆链接文件。而实际执行的systemd启动脚本配置文件，其实都是放置在/usr/lib/systemd/system/（ubuntu：/lib/systemd/system）

  - /usr/lib/systemd/system/（ubuntu：/lib/systemd/system）：每个服务最主要的启动脚本设置，有点类似以前的/etc/init.d下面的文件。
  - /run/systemd/system：系统执行过程中所产生的服务脚本，这些脚本的优先级要比/usr/lib/systemd/system/高。
  - /etc/systemd/system/：管理员根据主机系统的需求所建立的执行脚本，执行优先级比/run/systemd/system/高。

- systemd的unit类型分类说明：

  > /usr/lib/systemd/system/（ubuntu：/lib/systemd/system）以下的数据根据扩展名来区分不同的类型

  | 扩展名                | 主要服务功能                                                 |
  | --------------------- | ------------------------------------------------------------ |
  | .service              | 一般服务类型（service unit）；主要是系统服务，包括服务器本身所需要的本地服务以及网络服务等。 |
  | .socket               | 内部程序数据交换的socket服务（socket unit）：主要是IPC的传输信息socket文件功能。 |
  | .target               | 执行环境类型（target unit）：其实是一群unit的集合，执行multi-user.target就是执行一堆其他.service或.socket之类的服务。 |
  | .mount<br />.automout | 文件系统挂载相关的服务（automount unit/mount unit）：例如来自网络的自动挂载、NFS文件系统挂载等于文件系统相关性较高的进程管理。 |
  | .path                 | 检测特定文件或目录类型（path unit）：某些服务需要检测某些特定的目录来提供队列服务。 |
  | .timer                | 循环执行的服务（timer unit）                                 |

###### 通过systemctl管理服务

```
systemctl [command] [unit]
```

command:

- start：立刻启动后面接的unit
- stop：立刻关闭后面接的unit
- restart：立刻重新启动后面接的unit，亦即执行stop再start的意思
- reload：不关闭后面接的unit的情况下，重新加载配置文件，让设置生效
- enable：设置下次开机时，后面接的unit会被启动
- disable：设置下次开机时，后面接的unit不会被启动
- status：目前后面接的这个unit的状态，会列出有没有正在执行，开机默认执行与否，登录信息等
- is-active：目前有没有正在运行中
- is-enable：开机时有没有默认要启用这个unit
- daemon-reload：重新加载服务的配置文件

###### 通过systemctl查看系统上所有的服务

```
systemctl [command] [--type=TYPE] [--all]
```

command:

- list-units：依据unit显示目前有启动的unit，若加上--all才会列出没启动的。
- list-unit-files：依据/usr/lib/systemd/system/（ubuntu：/lib/systemd/system）内的文件，将所有文件列表说明。

--type=TYPE：unit类型，主要有service、socket、target等

- systemctl 列出的项目：
  - UNIT：项目的名称，包括各unit的类型（看副文件名）
  - LOAD：开机时是否会被加载，默认systemctl显示的是有加载的项目而已
  - ACTIVE：目前的状态，须与后续的SUB搭配，就是我们用systemctl status查看时，active的项目
  - DESCRIPTION：详细描述
  - cups

###### 通过systemctl分析各服务之间的依赖性

```
systemctl list-dependencies [unit] [--reverse]
```

###### 网路服务

> 会产生一个网络监听端口（port）的进程被称为网络服务。

- /etc/services：配置服务与端口
- netstat -tlunp：查看网络端口

###### systemctl配置文件相关目录

- 服务的管理时通过systemd来完成，而system的配置文件大部分放置于/usr/lib/systemd/system/目录中。但是修改的位置放置于/etc/systemd/system目录中。
- 举例来说，如果你想要额外修改vsftpd.service：
  - /usr/lib/systemd/system/vsftpd.service：官方发布的默认配置文件。
  - /etc/systemd/system/vsftpd.service.service.d/custom.conf：在/etc/systemd/system下面建立与配置文件相同文件名的目录，但是要加上.d的扩展名，然后然后在该目录下建立配置文件即可。另外，配置文件的扩展名最好使用.conf。在这个目录下的文件会【累加其他设置】到/usr/lib/systemd/system/vsftpd.service中。
  - /etc/systemd/system/vsftpd.service.wants/*：此目录内的文件尾链接文件，设置依赖服务的链接，意思是启动vsftpd.service之后，最好在加上该目录下面建议的服务。
  - /etc/systemd/system/vsftpd.service.requires/*：此目录内的文件尾链接文件，设置依赖服务的链接，意思是启动vsftpd.service之前，最好在加上该目录下面建议的服务。

###### systemctl配置文件的设置

- 整个设置分三个部分：
  - [Unit]：unit本身的说明，以及与其他依赖daemon的设置，包括在什么服务之后才启动此unit之类的设置值。
  - [Service]、[Socket]、[Timer]、[Mount]、[Path]：不同的unit类型就得要使用相对应的设置项目。主要用来规范服务启动的脚本、环境配置文件名、重新启动的方式等。
  - [Install]：这个项目就是将此unit安装到那个target里面去的意思。
- 配置文件内的配置规则：
  - 设置项目通常可以重复，不过后面的设置会替换前面。如果将设置值归零，可以使用类似【After=】的设置，亦即该项目的等号后面什么都没有，就将该设置归零了。
  - 如果设置参数需要由【是/否】的项目，你可以使用1、yes、true、on代表启动，用0、no、false、off代表关闭。
  - 空白行、开头为# 或; 的那一行，都代表注释
- 每个部分的设置：

##### 认识与分析日志文件

###### 什么是日志文件？

> 记录系统活动信息的几个文件，例如：何时、何地（来源IP）、何人（什么服务名称）、做了什么操作（信息登录）。
>
> 换句话说就是记录系统在什么时候由哪个进程做了什么样的操作时，发生了何种的事件。

###### linux常见的日志文件文件名

- /var/log/boot.log
  - 开机启动的时候系统内核会去检测与启动硬件，接下来开始启动各种内核支持的功能等。
- /var/log/cron
  - crontab任务的监控
- /var/log/dmesg
  - 记录系统上面所有的账号最近一次登录系统时的相关信息。lastlog命令就是利用这个文件的记录信息来显示。
- /var/log/maillog 或 /var/log/mail/*
  - 记录邮件的往来信息
- /var/log/messages
  - 几乎系统发生的错误信息（或是重要的信息）都会记录在这个文件中，如果系统发生莫名的错误时，这个文件是一定要查看的日志文件之一。
- /var/log/secure
  - 基本上，只要牵涉到【需要输入账号密码】的软件，那么当登录时（不管登录正确或错误）都会被记录在此文件中。包括系统的login程序、图形用户界面模式登录所使用的gdm、su、sudo等程序，还有网络连接的ssh、telnet等程序，登录信息都会被记录在这里。
- /var/log/wtmp、/var/log/faillog
  - 记录正确登录系统者的账户信息（wtmp）与错误登录时所使用的账户信息（faillog）
- /var/log/httpd/*、/var/log/samba/\*
  - 不同的网络服务会使用它们自己的日志文件来记录它们自己产生的各项信息。

###### 日志文件所需相关服务（daemon）与程序

- 日志文件产生的方式：
  1. 一种是由软件开发商自行定义写入的日志文件与相关格式。
  2. 另一种是由linux发行版本提供的日志文件关系系统服务来统一管理。CentOS提供rsyslog.service这个服务来统一管理日志文件。
- 可以通过logrotate（日志文件轮询）工具来自动化处理日志文件容量与更新的问题。
- 针对日志文件所需的功能，我们需要的服务与程序有：
  - systemd-journal.service：最主要的信息记录者，有systemd提供。
  - rsyslog.service：主要收集登录系统与网络等服务的信息。
  - logrotate：主要在进行日志文件的轮询功能。

###### 日志文件内容的一般格式

- 一般来说，系统产生的信息并记录下来的内容中，每条信息均会记录下面的几个重要内容：
  - 事件发生的日期与时间；
  - 发生此事件的主机名；
  - 启动此事件的服务名称（如systemd、crond等）或命令与函数名称（如su、login...）;
  - 该信息的实际内容。

###### rsyslo.service的配置文件：/etc/rsyslog.conf

- rsyslogd针对各种服务与信息记录在某些文件的配置文件就是/etc/rsyslog.conf，这个文件规定了1）什么服务、2）的什么等级信息、3）需要被记录在哪里（设备或文件）这三个东西；

  ```
  语法格式：
  服务名称[.=!]信息等级	信息登录的文件名或设备或主机
  ```

###### logrotate的配置文件

- /etc/logrotate.conf
- /etc/logrotate.d/

###### 使用journalctl查看登录信息

```
journalctl [-nrpf] [--since TIME] [--until TIME] _optional

1. 显示目前系统中所有的journal日志数据：
journalctl
2. (1)仅显示出2015/08/18整天以及(2)仅今天及(3)仅昨天的日志数据内容：
（1）journalctl --since "2015-08-18 00:00:00" --until "2015-08-19 00:00:00"
 (2) journalctl --since today
 (3) journalctl --since yesterday --until today
```

###### logger命令的应用

```
logger [-p 服务名称.等级] "信息"
```

###### 日志分析工具：logwatch

##### linux的启动流程分析

###### 操作系统启动的流程：

- 加载BIOS的硬件信息与进行自我检测（自检），并根据设置取得第一个可启动的设备；
- 读取并执行第一个启动设备内MBR的启动引导程序（亦即是grub2、spfdisk等程序）；
- 根据启动引导程序的设置加载kernel，kernel会开始检测硬件与加载驱动程序；
- 在硬件驱动成功后，kernel会主动调用systemd程序，并以default.target流程启动：
  - systemd 执行 sysinit.target 初始化系统及basic.target 准备操作系统；
  - systemd 启动 multi-user.target 下的本机与服务器服务；
  - systemd 执行 multi-user.target 下的 /etc/rc.d/rc.local 文件；
  - systemd 执行 multi-user.target 下的getty.target 及登录服务；
  - systemd 执行 graphical 需要的服务。

###### 第一个程序systemd及使用default.target进入启动程序分析

> 在内核加载完毕、进行完硬件检测与驱动程序加载后，此时你的主机硬件应该已经准备就绪了（ready）。此时内核会主动地调用第一个程序，那就是systemd。
>
> systemd最重要的功能就是准备软件执行的环境，包括系统的主机名、网络设置、语言设置、文件系统格式及其他服务的启动等。
>
> 而所有的操作都会通过systemd的默认启动服务集合，亦即是/etc/systemd/system/default.target来规划。

- systemctl list-dependencies graphical.target：列出所有systemd的调用所需要服务的流程
- systemctl list-dependencies multi-user.target
- systemctl list-dependencies basic.target
- systemctl list-dependencies getty.target
- systemctl list-dependencies remote-fs.target
- systemctl list-dependencies sysinit.target
- 当系统完成启动后，还想要让系统额外执行某些程序的话，可以将该程序命令或脚本的绝对路径，直接写一个systemd的启动脚本配置文件到/etc/systemd/system下面，然后使用systemctl enable的方式来设置启用它

###### 查看内核模块

- lsmod：查看目前内核加载了多少的模块
- modinfo [-adln] \[module name | filename]：查看某个文件代表的意义是什么

##### 网络设置

- IP
- 子网掩码（netmask）
- 网关（gateway）
- DNS主机的IP
- 网络参数可自动获取（DHCP协议自动获取）

###### nmcli：地址配置工具

- nmcli connection show：查看当前连接状态
  - NAME：连接代号，通常与后面的网卡DEVICE会一样
  - UUID：特殊的设备代号
  - TYPE：网卡的类型，通常就是以太网卡
  - DEVICE：网卡名称
- nmcli connection show [网卡名称]：显示指定接口属性
  - connection.autoconnect [yes|no]：是否于开机时启动这个连接，默认通常是yes
  - ipv4.method [auto|manual]：自动还是手动设置网络参数的意思
  - ipv4.dns [dns_server_ip]：填写DNS的IP地址
  - ipv4.addresses [IP/Netmask]：IP与netmask的集合，中间用斜线/来隔开
  - ipv4.gatemay [gw_ip]：gateway的IP地址
- nmcli connection reload：重启服务
- nmcli device status：显示设备状态
- nmcli device show：显示全部接口属性
- nmcli con add help：查看帮助

###### hostnamectl：修改主机名

```
hostnamectl [set-hostname 你的主机名]
hostnamectl set-hostname myhostname
cat /etc/hostname
```

###### 日期与时间设置：timedatectl

```
timedatectl [command]
选项与参数：
list-timezones：列出系统上所有支持的时区名称
set-timezone：设置时区位置
set-time：设置时间
set-ntp：设置网络校时系统
```

- 时间的调整

  ```
  timedatectl set-time "2022-11-08 12:02"
  ```

###### ubuntu日期时间设置（/usr/share/zoneinfo/Asia    /etc/localtime）

- 查看当前系统的时间：date -R
- tzselect：选择时区
- 设置日期：date -s 08/11/2022
- 设置时间：date -s 09:09:30
- 修改硬件的CMOS时间：hwclock --systohc

###### 语系设置（/etc/locale.conf）：locale

> ubuntu的语系设置：/etc/locale.gen

- locale：查看系统语系

```
localectl set-locale LANG=en_US.utf8
systemctl isolate multi-user.target
systemctl isolate graphical.target
```

###### 防火墙设置

###### dmidecode：查看硬件设备

- 1：详细的系统信息，含主板的型号与硬件的基础信息等
- 4：CPU的相关信息，包括倍频、外频、内核数、内核线程等
- 9：系统弄的插槽格式，包括PCI、PCI-E等的插槽规格说明
- 17：每一个内存插槽的规格，若有内存，则列出该内存的容量与型号


- dmidecode -t 1：显示整个系统的硬件信息

###### 硬件资源的收集与分析

> 内核所检测到的各项硬件设备，后来就会被记录在/proc与/sys当中。

- gdisk：可以使用gdisk -l将分区表列出
- demesg：查看内核运行过程当中所显示的各项信息记录
- vmstat：分析系统（CPU/RAM/IO）目前的状态
- lspci：列出整个CPU系统的PCI接口设备
- isusb：列出目前系统上面各个USB端口的状态，与链接的USB设备
- iostat：与vmstat类似，可实时列出整个CUP与接口设备的输入/输出状态

###### 了解磁盘的健康状态：smartctl

##### 软件安装

- file：查看文件类型

  ```
  file /bin/bash
  如果是二进制而且是可以执行的时候，它就会显示执行文件类别（ELF 64-bit LSE executable），同时会说明是否使用动态函数库（shared libs），而如果是一般的脚本，那它就会显示出text executables之类的字样。
  ```

###### 函数库

> 内核相关信息大多放置在/usr/include、/usr/lib、/usr/lib64里面

###### 预先编译号程序的机制发行版

- Red Hat系列（含Fedora/CentOS系列），使用的RPM软件管理机制与yum在线更新模式；
- Debian使用的dpkg软件管理机制与APT在线更新模式；

###### 使用Tarball进行软件安装

1. 将Tarball由厂商的网站下载；
2. 将Tarball解开，产生很多的源代码文件；
3. 开始以gcc进行源代码的编译（会产生目标文件object files）；
4. 然后以gcc进程函数库、主、子程序的链接，以形成主要的二进制文件；
5. 将上述的二进制文件以及相关的配置文件安装至自己的主机上面。

###### make与makefile

- 简化编译时所需要执行的命令；
- 若在编译完成之后，修改了某个源代码文件，则make仅会针对被修改了的文件进行编译，其他的目标文件不会被修改；
- 最后可以依照依赖性来更新（update）执行文件。

###### 文件名含义

```
rp-pppoe-3.11-5.el7.x86_64.rpm
rp-pppoe：软件名称
-3.11-：软件的版本信息
5：发布的次数
.el7.x86_64：适合的硬件平台
.rpm：扩展名
```

###### RPM软件管理程序：rpm

| 目录           | 功能                             |
| -------------- | -------------------------------- |
| /etc           | 一些配置文件放置的目录           |
| /usr/bin       | 一些可执行文件                   |
| /usr/lib       | 一些程序使用的动态函数库         |
| /usr/share/doc | 一些基本的软件使用手册与说明文件 |
| /usr/share/man | 一些man page文件                 |

```
rpm -ivh package_name
-i：install安装的意思
-v：查看更详细的安装信息
-h：显示安装进度
```

- 一次性安装多个软件，后面可以直接接上多个安装文件，也可使用正则匹配。
- 直接有网络上的某个文件地址来安装：rpm -ivh http://xxx/xxx.rpm

| 可执行的选项   | 代表意义                                                     |
| -------------- | ------------------------------------------------------------ |
| --nodeps       | 当发生软件属性依赖问题而无法安装，但你执意安装时；           |
| --replacefiles | 如果在安装的过程中出现了【某个文件已经安装在你的系统上面】的信息，<br />又或许出现版本不合的信息（confilcting files）时，可以使用这个参数来<br />直接覆盖文件。 |
| --replacepkgs  | 重新安装某个已经安装过的软件，如果你要安装一堆RPM文件时，<br />可以使用rpm -ivh *.rpm，但若某些软件已经安装过了，此时系统会出现<br />【某软件已安装】的信息，导致无法继续安装，此时可使用这个选项来重复安装。 |
| --test         | 想要测试以下该软件是否可以被安装到用户的linux环境当中，可找出是否有属性<br />依赖的问题。范例：rpm -ivh pagname.rpm --test |
| --force        | 这个参数其实就是--replacefiles与--replacepkgs的综合体        |
| --justdb       | 由于RPM数据库损坏或是某些缘故产生错误时，可使用这个选项来更新软件在<br />数据库内的相关信息。 |
| --nosignature  | 想要跳过数字签名的检查时，可以使用这个选项。                 |
| --prefix新路径 | 要将软件安装到其他非正规目录时。比如，你想要将某软件安装到/usr/local<br />而非正规的/bin、/etc等目录，就可以使用【--prefix /usr/local】来处理。 |
| --noscripts    | 不想容该软件在安装过程中自行执行某些系统命令。               |

- RPM升级与更新（upgrade/freshen）

  | -Uvh | 后面接的软件即使没有安装过，则系统将予以直接安装；若后面的软件有安装过旧版，则系统自动更新至新版 |
  | ---- | ------------------------------------------------------------ |
  | -Fvh | 如果后面接的软件并未安装到你的linux系统上，则该软件不会被安装；亦即只有已安装至你linux系统内的软件会被升级 |

- RPM查询（query）

  > 查新主要分为两部分：
  >
  > 	一个是查找已安装到系统上面的软件信息，这部分的信息都是由/var/lib/rpm所提供；
  > 	
  > 	另一个则是查找某个rpm文件内容，等于是由RPM文件内找出一些要写入数据库内的信息，这部分就得要使用-qp（p是package的意思）

  - -q：仅查询，后面接的软件名称是否有安装；
  - -qa：列出已经安装在本机linux系统上面的所有软件名称；
  - -qi：列出该软件的详细信息，包含开发商、版本与说明等；
  - -ql：列出该软件所有的文件与目录所在完整文件名（list）；
  - -qc：列出该软件的所有配置文件（找出在/etc/下面的文件名而已）；
  - -qd：列出该软件的所有说明文件（找出与man有关的文件而已）；
  - -qR：列出与该软件有关的依赖软件所含的文件（Required的意思）；
  - -qf：由后面接的文件名，找出该文件属于哪一个已安装的软件；
  - -q --scripts：列出是否含有安装后需要执行的脚本文件，可用以debug；
  - -qp[icdlP]：查询某个RPM文件内含有的信息；

  ```
  1. 我想要直到我的系统中，以c开头的软件有几个？
  rpm -qa | grep ^c|wc -l
  ```

- RPM验证

  > 使用/var/lib/rpm下面的数据库内容来比对目前linux系统的环境下的所有安装文件。目的是，当你有数据不小心丢失或是因为你误删了某个软件的文件，或是不小心不知道修改到某一个软件的文件内容，就用这个简单的方法来验证以下原本的文件，好让你了解这一阵子到底是修改到哪些文件内容。

  - -V：后面跟软件名，若该软件所含的文件被修改过才会显示；rpm -V /etc/crontab
  - Va：列出目前系统上面所有可能被修改过的文件；
  - Vp：后面跟文件名，列出该软件内可能被修改过的文件；
  - Vf：显示某个文件是否被修改过。

- 数字签名

  - 首先要安装原厂发布的公钥文件；
  - 实际安装RPM软件时，rpm命令会读取RPM文件的签名信息并与本机系统内的签名信息比对；
  - 若签名相同则予以安装，若找不到相关的签名信息时，则给予警告并且停止安装；

- RPM反安装（卸载）与重建数据库（erase/rebuilddb）

  ```
  重建数据库：
  rpm --rebuilddb
  ```

###### YUM在线升级功能

> YUM是通过分析RPM的标头数据后，根据各软件的相关性制作出属性依赖时的解决方案，然后可以自动处理软件的依赖属性问题，以解决软件安装或删除与升级的问题。

- 查新功能：yum [list、info、search、provides、whatprovides]

  ```
  yum [opton] [查询工作选项] [相关参数]
  [option]：
  -y：当yum要等待使用者输入时，这个选项可以自动提供yes的回应；
  --installroot=/some/path：将该软件安装在/some/path而不适用默认路径；
  [查询工作选项] [相关参数]：
  search：查找某个软件名称或是描述的重要关键字；
  list：列出目前yum所管理的所有的软件与版本，优点类似rpm -qa；
  info：同上，不过优点类似rpm -qai的执行结果；
  provides：从文件去查找软件，类似rpm -qf的功能；

  1. 列出YUM服务器上面提供的所有软件名称
  yum list
  2. 列出提供passwd这个命令的软件有哪些
  yum provides passwd
  3. 列出目前服务器上可供本机进行升级的软件有哪些
  yum list updates
  ```

- 安装、升级功能：yum [install、update] 软件

  ```
  yum [option] [安装与升级的工作选项] [相关参数]
  [option]：
  install：后面接要安装的软件；
  update：后面接要升级的软件，若要整个系统都要升级，就直接update即可；
  ```

- 删除功能：yum [remove] 软件

- YUM的配置文件：/etc/yum.repos.d

  - [base]：代表软件源的名字，中括号一定要存在，里面的名称则可以随意取。但是不能有两个相同的软件源名称，否则yum会不知道该到哪里去找软件园相关的软件列表；
  - name：只是说明一下这个软件源的意义而已，重要性不高；
  - mirrorlist=：列出这个软件源可以使用的镜像站，如果不想使用，可以注释掉这行；
  - baseurl：这个最重要，因为后面接的就是软件源的实际地址，mirrorlist是由YUM程序自行去识别镜像站，baseurl则是指定固定的一个软件源网址；
  - enable=1：就是让这个软件源被启用，如果不想启动可以使用enable=0；
  - gpgcheck=1：指定是否需要查看RPM文件内的数字签名；
  - gpgkey=：数字签名的公钥文件所在位置，使用默认值即可

- YUM的软件群组功能

  ```
  yum [群组功能] [软件群组]
  选项与参数：
  	grouplist：列出所有可使用的【软件群组】；
  	groupinfo：后面接group name，则可了解该group内含的所有软件名；
  	groupinstall：可以安装一整组的软件群组；
  	groupremove：删除某个软件群组；
  ```

- 全系统自动升级

  ```
  echo '10 1 * * * root /usr/bin/yum -y --enablerepo=epel update' > /etc/cron.d/yumupdate
  ```

- yum安装步骤

  1. 先检查一下有哪些软件没有安装或已安装

     ```
     rpm -q httpd php mysql
     ```

  2. 安装需要的软件

     ```
     yum install xxx xxx xxx
     ```

  3. 启动与开机启动

     ```
     systemctl daemon-reload
     systemctl start httpd
     systemctl enable httpd
     systemctl status httpd
     ```

  4. 防火墙

     ```
     firewall-cmd --add-service="http"
     firewall-cmd --permanent --add-service="http"
     firewall-cmd --list-all
     ```

  5. 测试：用软件去查看你的服务正常与否

##### 镜像资源

- linux内核官网

  ```
  https://www.kernel.org
  ```

- centos官方网站

  ```
  http://mirror.centos.org/
  http://mirror.centos.org/centos/7/isos
  ```

- ubuntu官网

  ```
  https://ubuntu.com/
  ```

- 中科大镜像

  ```
  http://centos.ustc.edu.cn/
  http://centos.ustc.edu.cn/centos/7/isos
  http://centos.ustc.edu.cn/centos/7/os/x86_64
  ```

- 清华大学镜像站

  ```
  https://mirrors.tuna.tsinghua.edu.cn/
  https://mirrors.tuna.tsinghua.edu.cn/centos/7/isos
  https://mirrors.tuna.tsinghua.edu.cn/centos/7/os/x86_64
  ```

  