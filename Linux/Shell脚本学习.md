[toc]
##### #!/bin/bash

> **#!** 是一个约定的标记，它告诉系统这个脚本需要什么解释器来执行，即使用哪一种 Shell。

- echo 命令用于向窗口输出文本。
- chmod +x ./test.sh  #使脚本具有执行权限
- ./test.sh  #执行脚本

##### shell 变量

- 定义变量时，变量名不加美元符号$

  ```shell
  # 显式地直接赋值
  your_name="runoob.com"
  
  # 用语句给变量赋值
  for file in `ls /etc` # 将 /etc 下目录的文件名循环出来
  或
  for file in $(ls /etc)
  ```

- 使用一个定义过的变量，只要在变量名前面加美元符号$即可

  ```shell
  your_name="qinjx"
  echo $your_name
  echo ${your_name}
  ```

- 加花括号是为了帮助解释器识别变量的边界

  ```shell
  for skill in Ada Coffe Action Java; do
      echo "I am good at ${skill}Script"
  done
  ```

- 使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。

  ```shell
  #!/bin/bash
  
  myUrl="https://www.google.com"
  readonly myUrl
  ```

- 使用 unset 命令可以删除变量

  ```shell
  # 变量被删除后不能再次使用。unset 命令不能删除只读变量。
  unset variable_name
  ```

##### shell 字符串

###### 单引号

```shell
str='this is a string'
# 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的；
```

###### 双引号

```shell
# 双引号里可以有变量
# 双引号里可以出现转义字符
your_name="runoob"
str="Hello, I know you are \"$your_name\"! \n"
echo -e $str
```

###### 拼接字符

```shell
your_name="runoob"
# 使用双引号拼接
greeting="hello, "$your_name" !"
greeting_1="hello, ${your_name} !"
echo $greeting  $greeting_1
```

###### 获取字符串长度

```shell
string="abcd"
echo ${#string}   # 输出 4
```

###### 提取子字符串

```shell
string="runoob is a great site"
echo ${string:1:4} # 输出 unoo
```

###### 查找子字符串

```shell
# 查找字符 i 或 o 的位置(哪个字母先出现就计算哪个)：

string="runoob is a great site"
echo `expr index "$string" io`  # 输出 4
```

##### shell数组

- bash支持一维数组（不支持多维数组），并且没有限定数组的大小。
- 数组元素的下标由 0 开始编号。获取数组中的元素要利用下标，下标可以是整数或算术表达式，其值应大于或等于 0。

###### 定义数组

- 在 Shell 中，用括号来表示数组，数组元素用"空格"符号分割开。

  ```shell
  数组名=(值1 值2 ... 值n)
  ```

- 单独定义数组的各个分量：

  ```shell
  array_name[0]=value0
  array_name[1]=value1
  array_name[n]=valuen
  ```

###### 读取数组

```shell
${数组名[下标]}

# 使用 @ 符号可以获取数组中的所有元素
echo ${array_name[@]}
```

###### 获取数组的长度

```shell
# 取得数组元素的个数
length=${#array_name[@]}
# 或者
length=${#array_name[*]}
# 取得数组单个元素的长度
lengthn=${#array_name[n]}
```

##### shell注释

- 以 **#** 开头的行就是注释，会被解释器忽略。

- 多行注释

  ```shell
  :<<EOF
  注释内容...
  EOF
  
  :<<'
  注释内容...
  注释内容...
  注释内容...
  '
  
  :<<!
  注释内容...
  注释内容...
  注释内容...
  !
  ```

##### shell 基本运算符

> 原生bash不支持简单的数学运算，但是可以通过其他命令来实现，例如 **awk 和 expr，expr **最常用。

- 表达式和运算符之间要有空格
- 完整的表达式要被``包含

###### 算数运算符

> 假定变量 a 为 10，变量 b 为 20：

| 运算符 | 说明                                          | 举例                          |
| :----- | :-------------------------------------------- | :---------------------------- |
| +      | 加法                                          | `expr $a + $b` 结果为 30。    |
| -      | 减法                                          | `expr $a - $b` 结果为 -10。   |
| *      | 乘法                                          | `expr $a \* $b` 结果为  200。 |
| /      | 除法                                          | `expr $b / $a` 结果为 2。     |
| %      | 取余                                          | `expr $b % $a` 结果为 0。     |
| =      | 赋值                                          | a=$b 把变量 b 的值赋给 a。    |
| ==     | 相等。用于比较两个数字，相同则返回 true。     | [ $a == $b ] 返回 false。     |
| !=     | 不相等。用于比较两个数字，不相同则返回 true。 | [ $a != $b ] 返回 true。      |

```shell
a=5
b=6

result=$[a+b] # 注意等号两边不能有空格；代码中的 [] 执行基本的算数运算
echo "result 为： $result"
```

###### 关系运算符

> 关系运算符只支持数字，不支持字符串，除非字符串的值是数字。

| 运算符 | 说明                                                  | 举例                       |
| :----- | :---------------------------------------------------- | :------------------------- |
| -eq    | 检测两个数是否相等，相等返回 true。                   | [ $a -eq $b ] 返回 false。 |
| -ne    | 检测两个数是否不相等，不相等返回 true。               | [ $a -ne $b ] 返回 true。  |
| -gt    | 检测左边的数是否大于右边的，如果是，则返回 true。     | [ $a -gt $b ] 返回 false。 |
| -lt    | 检测左边的数是否小于右边的，如果是，则返回 true。     | [ $a -lt $b ] 返回 true。  |
| -ge    | 检测左边的数是否大于等于右边的，如果是，则返回 true。 | [ $a -ge $b ] 返回 false。 |
| -le    | 检测左边的数是否小于等于右边的，如果是，则返回 true。 | [ $a -le $b ] 返回 true。  |

###### 布尔运算符

> 下表列出了常用的布尔运算符，假定变量 a 为 10，变量 b 为 20：

| 运算符 | 说明                                                | 举例                                     |
| :----- | :-------------------------------------------------- | :--------------------------------------- |
| !      | 非运算，表达式为 true 则返回 false，否则返回 true。 | [ ! false ] 返回 true。                  |
| -o     | 或运算，有一个表达式为 true 则返回 true。           | [ $a -lt 20 -o $b -gt 100 ] 返回 true。  |
| -a     | 与运算，两个表达式都为 true 才返回 true。           | [ $a -lt 20 -a $b -gt 100 ] 返回 false。 |

###### 逻辑运算符

> 以下介绍 Shell 的逻辑运算符，假定变量 a 为 10，变量 b 为 20:

| 运算符 | 说明       | 举例                                       |
| :----- | :--------- | :----------------------------------------- |
| &&     | 逻辑的 AND | [[ $a -lt 100 && $b -gt 100 ]] 返回 false  |
| \|\|   | 逻辑的 OR  | [[ $a -lt 100 \|\| $b -gt 100 ]] 返回 true |

###### 字符串运算符

> 下表列出了常用的字符串运算符，假定变量 a 为 "abc"，变量 b 为 "efg"：

| 运算符 | 说明                                         | 举例                     |
| :----- | :------------------------------------------- | :----------------------- |
| =      | 检测两个字符串是否相等，相等返回 true。      | [ $a = $b ] 返回 false。 |
| !=     | 检测两个字符串是否不相等，不相等返回 true。  | [ $a != $b ] 返回 true。 |
| -z     | 检测字符串长度是否为0，为0返回 true。        | [ -z $a ] 返回 false。   |
| -n     | 检测字符串长度是否不为 0，不为 0 返回 true。 | [ -n "$a" ] 返回 true。  |
| $      | 检测字符串是否不为空，不为空返回 true。      | [ $a ] 返回 true。       |

###### 文件测试运算符

| 操作符  | 说明                                                         | 举例                      |
| :------ | :----------------------------------------------------------- | :------------------------ |
| -b file | 检测文件是否是块设备文件，如果是，则返回 true。              | [ -b $file ] 返回 false。 |
| -c file | 检测文件是否是字符设备文件，如果是，则返回 true。            | [ -c $file ] 返回 false。 |
| -d file | 检测文件是否是目录，如果是，则返回 true。                    | [ -d $file ] 返回 false。 |
| -f file | 检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。 | [ -f $file ] 返回 true。  |
| -g file | 检测文件是否设置了 SGID 位，如果是，则返回 true。            | [ -g $file ] 返回 false。 |
| -k file | 检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。  | [ -k $file ] 返回 false。 |
| -p file | 检测文件是否是有名管道，如果是，则返回 true。                | [ -p $file ] 返回 false。 |
| -u file | 检测文件是否设置了 SUID 位，如果是，则返回 true。            | [ -u $file ] 返回 false。 |
| -r file | 检测文件是否可读，如果是，则返回 true。                      | [ -r $file ] 返回 true。  |
| -w file | 检测文件是否可写，如果是，则返回 true。                      | [ -w $file ] 返回 true。  |
| -x file | 检测文件是否可执行，如果是，则返回 true。                    | [ -x $file ] 返回 true。  |
| -s file | 检测文件是否为空（文件大小是否大于0），不为空返回 true。     | [ -s $file ] 返回 true。  |
| -e file | 检测文件（包括目录）是否存在，如果是，则返回 true。          | [ -e $file ] 返回 true。  |

其他检查符：

- **-S**: 判断某文件是否 socket。
- **-L**: 检测文件是否存在并且是一个符号链接。

##### Shell echo命令

1. 显示普通字符串

   ```shell
   echo "It is a test"
   
   # 省略双引号
   echo It is a test
   ```

2. 显示转义字符

   ```shell
   echo "\"It is a test\""
   ```

3. 显示变量

   ```shell
   # read 命令从标准输入中读取一行,并把输入行的每个字段的值指定给 shell 变量
   
   #!/bin/sh
   read name 
   echo "$name It is a test"
   ```

4. 显示换行

   ```shell
   echo -e "OK! \n" # -e 开启转义
   echo "It is a test"
   ```

5. 显示不换行

   ```shell
   #!/bin/sh
   echo -e "OK! \c" # -e 开启转义 \c 不换行
   echo "It is a test"
   ```

6. 显示结果定向至文件

   ```shell
   echo "It is a test" > myfile
   ```

7. 原样输出字符串，不进行转义或取变量(用单引号)

   ```shell
   echo '$name\"'
   ```

8. 显示命令执行结果

   ```shell
   echo `date`
   ```

##### shell test 命令

> Shell中的 test 命令用于检查某个条件是否成立，它可以进行数值、字符和文件三个方面的测试。

###### 数值测试

```shell
num1=100
num2=100
if test $[num1] -eq $[num2]
then
    echo '两个数相等！'
else
    echo '两个数不相等！'
fi
```

###### 字符串测试

```shell
num1="ru1noob"
num2="runoob"
if test $num1 = $num2
then
    echo '两个字符串相等!'
else
    echo '两个字符串不相等!'
fi
```

###### 文件测试

```shell
cd /bin
if test -e ./bash
then
    echo '文件已存在!'
else
    echo '文件不存在!'
fi
```

- Shell 还提供了与( -a )、或( -o )、非( ! )三个逻辑操作符用于将测试条件连接起来，其优先级为： **!** 最高， **-a** 次之， **-o** 最低

  ```shell
  cd /bin
  if test -e ./notFile -o -e ./bash
  then
      echo '至少有一个文件存在!'
  else
      echo '两个文件都不存在'
  fi
  ```

##### shell 流程控制

###### 条件判断

1. if 语句语法格式：

   ```shell
   if condition
   then
       command1 
       command2
       ...
       commandN 
   fi
   
   # 写成一行（适用于终端命令提示符）：
   if [ $(ps -ef | grep -c "ssh") -gt 1 ]; then echo "true"; fi
   ```

2. if else 语法格式：

   ```shell
   if condition
   then
       command1 
       command2
       ...
       commandN
   else
       command
   fi
   ```

3. if else-if else 语法格式：

   ```shell
   if condition1
   then
       command1
   elif condition2 
   then 
       command2
   else
       commandN
   fi
   ```

   - if else 的 **[...]** 判断语句中大于使用 **-gt**，小于使用 **-lt**。

     ```shell
     if [ "$a" -gt "$b" ]; then
         ...
     fi
     ```

   - 如果使用 **((...))** 作为判断语句，大于和小于可以直接使用 **>** 和 **<**。

     ```shell
     if (( a > b )); then
         ...
     fi
     ```

###### for 循环

```shell
for var in item1 item2 ... itemN
do
    command1
    command2
    ...
    commandN
done

# 写成一行：
for var in item1 item2 ... itemN; do command1; command2… done;
```

```shell
for loop in 1 2 3 4 5
do
    echo "The value is: $loop"
done
```

```shell
#!/bin/bash

for str in This is a string
do
    echo $str
done
```

###### while 语句

> while 循环用于不断执行一系列命令，也用于从输入文件中读取数据。

```shell
while condition
do
    command
done
```

```shell
#!/bin/bash
int=1
while(( $int<=5 ))
do
    echo $int
    let "int++"
done
```

- let 命令

  > let 命令是 BASH 中用于计算的工具，用于执行一个或多个表达式，变量计算中不需要加上 $ 来表示变量。如果表达式中包含了空格或其他特殊字符，则必须引起来。

  ```shell
  #!/bin/bash
  
  let a=5+4
  let b=9-3 
  echo $a $b
  ```

###### 无限循环

```shell
while :
do
    command
done
```

```shell
while true
do
    command
done
```

###### case ... case

> **case ... esac** 为多选择语句，与其他语言中的 switch ... case 语句类似，是一种多分支选择结构，每个 case 分支用右圆括号开始，用两个分号 **;;** 表示 break，即执行结束，跳出整个 case ... esac 语句，esac（就是 case 反过来）作为结束标记。

```shell
case 工作方式如上所示，取值后面必须为单词 in，每一模式必须以右括号结束。取值可以为变量或常数，匹配发现取值符合某一模式后，其间所有命令开始执行直至 ;;。
取值将检测匹配的每一个模式。一旦模式匹配，则执行完匹配模式相应命令后不再继续其他模式。如果无一匹配模式，使用星号 * 捕获该值，再执行后面的命令。

case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2)
    command1
    command2
    ...
    commandN
    ;;
esac
```

```shell
echo '输入 1 到 4 之间的数字:'
echo '你输入的数字为:'
read aNum
case $aNum in
    1)  echo '你选择了 1'
    ;;
    2)  echo '你选择了 2'
    ;;
    3)  echo '你选择了 3'
    ;;
    4)  echo '你选择了 4'
    ;;
    *)  echo '你没有输入 1 到 4 之间的数字'
    ;;
esac
```

##### 跳出循环

###### break 命令

```shell
#!/bin/bash
while :
do
    echo -n "输入 1 到 5 之间的数字:"
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的! 游戏结束"
            break
        ;;
    esac
done
```

###### continue

```shell
#!/bin/bash
while :
do
    echo -n "输入 1 到 5 之间的数字: "
    read aNum
    case $aNum in
        1|2|3|4|5) echo "你输入的数字为 $aNum!"
        ;;
        *) echo "你输入的数字不是 1 到 5 之间的!"
            continue
            echo "游戏结束"
        ;;
    esac
done
```

##### shell 函数

```shell
[ function ] funname [()]

{

    action;

    [return int;]

}
```

| 参数处理 | 说明                                                         |
| :------- | :----------------------------------------------------------- |
| $#       | 传递到脚本或函数的参数个数                                   |
| $*       | 以一个单字符串显示所有向脚本传递的参数                       |
| $$       | 脚本运行的当前进程ID号                                       |
| $!       | 后台运行的最后一个进程的ID号                                 |
| $@       | 与$*相同，但是使用时加引号，并在引号中返回每个参数。         |
| $-       | 显示Shell使用的当前选项，与set命令功能相同。                 |
| $?       | 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。 |

##### shell 输入/输出重定向

| 命令            | 说明                                               |
| :-------------- | :------------------------------------------------- |
| command > file  | 将输出重定向到 file。                              |
| command < file  | 将输入重定向到 file。                              |
| command >> file | 将输出以追加的方式重定向到 file。                  |
| n > file        | 将文件描述符为 n 的文件重定向到 file。             |
| n >> file       | 将文件描述符为 n 的文件以追加的方式重定向到 file。 |
| n >& m          | 将输出文件 m 和 n 合并。                           |
| n <& m          | 将输入文件 m 和 n 合并。                           |
| << tag          | 将开始标记 tag 和结束标记 tag 之间的内容作为输入。 |

###### 输出重定向

> 重定向一般通过在命令间插入特定的符号来实现。

```shell
command1 > file1
# 执行command1然后将输出的内容存入file1。
# 注意任何file1内的已经存在的内容将被新内容替代。如果要将新内容添加在文件末尾，请使用>>操作符。
```

##### Shell 文件包含

```shell
. filename   # 注意点号(.)和文件名中间有一空格

或

source filename
```

- test1.sh

  ```shell
  #!/bin/bash
  # author:菜鸟教程
  # url:www.runoob.com
  
  url="http://www.runoob.com"
  ```

- test2.sh

  ```shell
  #!/bin/bash
  # author:菜鸟教程
  # url:www.runoob.com
  
  #使用 . 号来引用test1.sh 文件
  . ./test1.sh
  
  # 或者使用以下包含文件代码
  # source ./test1.sh
  
  echo "菜鸟教程官网地址：$url"
  ```

- 为 test2.sh 添加可执行权限并执行：

  ```shell
  $ chmod +x test2.sh 
  $ ./test2.sh 
  菜鸟教程官网地址：http://www.runoob.com
  ```