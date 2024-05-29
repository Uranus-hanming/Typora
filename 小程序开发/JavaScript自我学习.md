- JavaScript 可以通过不同的方式来输出数据：

  - 使用 **window.alert()** 弹出警告框。
  - 使用 **document.write()** 方法将内容写到 HTML 文档中。
  - 使用 **innerHTML** 写入到 HTML 元素。
  - 使用 **console.log()** 写入到浏览器的控制台。

- 从 JavaScript 访问某个 HTML 元素，您可以使用 document.getElementById(*id*) 方法。

  > 请使用 "id" 属性来标识 HTML 元素，并 innerHTML 来获取或插入元素内容

- \<button onclick="myFunction()"> 点我</button> 点击事件

- JavaScript 字面量（在编程语言中，一般固定值称为字面量）

  - **数字（Number）字面量** 可以是整数或者是小数，或者是科学计数(e)
  - **字符串（String）字面量** 可以使用单引号或双引号
  - **表达式字面量** 用于计算
  - **数组（Array）字面量** 定义一个数组
  - **对象（Object）字面量** 定义一个对象
  - **函数（Function）字面量** 定义一个函数

-  JavaScript 变量

   > 在编程语言中，变量用于存储数据值。
   >
   > JavaScript 使用关键字 **var** 来定义变量， 使用等号来为变量赋值
   >
   > 变量可以通过变量名访问。在指令式语言中，变量通常是可变的。字面量是一个恒定的值。

- JavaScript 的数据类型：

   - **值类型(基本类型)**：字符串（String）、数字(Number)、布尔(Boolean)、空（Null）、未定义（Undefined）、Symbol。
   - **引用数据类型（对象类型）**：对象(Object)、数组(Array)、函数(Function)，还有两个特殊的对象：正则（RegExp）和日期（Date）。

   ```
   在 JavaScript 中有 6 种不同的数据类型：
   string
   number
   boolean
   object
   function
   symbol

   3 种对象类型：
   Object
   Date
   Array

   2 个不包含任何值的数据类型：
   null
   undefined
   ```

-  JavaScript 函数

   > 函数是由事件驱动的或者当它被调用时执行的可重复使用的代码块。
   >
   > 函数就是包裹在花括号中的代码块，前面使用了关键词 function：
   >
   > 引用一个函数** = 调用函数(执行函数内的语句)。
   >
   > function myFunction(a, b) {
   >  return a * b;                                // 返回 a 乘以 b 的结果
   > }

-  JavaScript 语句标识符

   | break        | 用于跳出循环。                                               |
   | ------------ | ------------------------------------------------------------ |
   | catch        | 语句块，在 try 语句块执行出错时执行 catch 语句块。           |
   | continue     | 跳过循环中的一个迭代。                                       |
   | do ... while | 执行一个语句块，在条件语句为 true 时继续执行该语句块。       |
   | for          | 在条件语句为 true 时，可以将代码块执行指定的次数。           |
   | for ... in   | 用于遍历数组或者对象的属性（对数组或者对象的属性进行循环操作）。 |
   | function     | 定义一个函数                                                 |
   | if ... else  | 用于基于不同的条件来执行不同的动作。                         |
   | return       | 退出函数                                                     |
   | switch       | 用于基于不同的条件来执行不同的动作。                         |
   | throw        | 抛出（生成）错误 。                                          |
   | try          | 实现错误处理，与 catch 一同使用。                            |
   | var          | 声明一个变量。                                               |
   | while        | 当条件语句为 true 时，执行语句块。                           |

- 声明变量类型

   > 当您声明新变量时，可以使用关键词 "new" 来声明其类型：
   >
   > var carname=new String;

- HTML 事件

   - HTML 页面完成加载
   - HTML input 字段改变时
   - HTML 按钮被点击

   > HTML 元素中可以添加事件属性，使用 JavaScript 代码来添加 HTML 元素。
   >
   > \<button onclick="getElementById('demo').innerHTML=Date()">现在的时间是?</button>
   >
   > \<button onclick="this.innerHTML=Date()">现在的时间是?</button>
   >
   > JavaScript代码通常是几行代码。比较常见的是通过事件属性来调用：
   >
   > \<button onclick="displayDate()">点这里</button>
   >
   > <script>
   > function displayDate(){
   >
   >      document.getElementById("demo").innerHTML=Date();
   >
   > }
   > </script>
   >
   > <p id="demo"></p>

- 常见的HTML事件

   | 事件        | 描述                                 |
   | ----------- | ------------------------------------ |
   | onchange    | HTML 元素改变                        |
   | onclick     | 用户点击 HTML 元素                   |
   | onmouseover | 鼠标指针移动到指定的元素上时发生     |
   | onmouseout  | 用户从一个 HTML 元素上移开鼠标时发生 |
   | onkeydown   | 用户按下键盘按键                     |
   | onload      | 浏览器已完成页面的加载               |

- 字符串方法

   | 方法                | 描述                                                         |
   | ------------------- | ------------------------------------------------------------ |
   | charAt()            | 返回指定索引位置的字符                                       |
   | charCodeAt()        | 返回指定索引位置字符的 Unicode 值                            |
   | concat()            | 连接两个或多个字符串，返回连接后的字符串                     |
   | fromCharCode()      | 将 Unicode 转换为字符串                                      |
   | indexOf()           | 返回字符串中检索指定字符第一次出现的位置                     |
   | lastIndexOf()       | 返回字符串中检索指定字符最后一次出现的位置                   |
   | localeCompare()     | 用本地特定的顺序来比较两个字符串                             |
   | match()             | 找到一个或多个正则表达式的匹配                               |
   | replace()           | 替换与正则表达式匹配的子串                                   |
   | search()            | 检索与正则表达式相匹配的值                                   |
   | slice()             | 提取字符串的片断，并在新的字符串中返回被提取的部分           |
   | split()             | 把字符串分割为子字符串数组                                   |
   | substr()            | 从起始索引号提取字符串中指定数目的字符                       |
   | substring()         | 提取字符串中两个指定的索引号之间的字符                       |
   | toLocaleLowerCase() | 根据主机的语言环境把字符串转换为小写，只有几种语言（如土耳其语）具有地方特有的大小写映射 |
   | toLocaleUpperCase() | 根据主机的语言环境把字符串转换为大写，只有几种语言（如土耳其语）具有地方特有的大小写映射 |
   | toLowerCase()       | 把字符串转换为小写                                           |
   | toString()          | 返回字符串对象值                                             |
   | toUpperCase()       | 把字符串转换为大写                                           |
   | trim()              | 移除字符串首尾空白                                           |
   | valueOf()           | 返回某个字符串对象的原始值                                   |

- 条件运算符

   ```html
   <!DOCTYPE html>
   <html>
   <head> 
   <meta charset="utf-8"> 
   <title>菜鸟教程(runoob.com)</title> 
   </head>
   <body>

   <p>点击按钮检测年龄。</p>
   年龄:<input id="age" value="18" />
   <p>是否达到投票年龄?</p>
   <button onclick="myFunction()">点击按钮</button>
   <p id="demo"></p>
   <script>
   function myFunction()
   {
   	var age,voteable;
   	age=document.getElementById("age").value;
   	voteable=(age<18)?"年龄太小":"年龄已达到";
   	document.getElementById("demo").innerHTML=voteable;
   }
   </script>

   </body>
   </html>
   ```

- 条件语句

   - **if 语句** - 只有当指定条件为 true 时，使用该语句来执行代码

      ```
      if (condition)
      {
          当条件为 true 时执行的代码
      }
      ```

   - if...else 语句

      ```
      请使用 if....else 语句在条件为 true 时执行代码，在条件为 false 时执行其他代码。
      if (condition)
      {
          当条件为 true 时执行的代码
      }
      else
      {
          当条件不为 true 时执行的代码
      }
      ```

   - if...else if...else 语句

      ```
      使用 if....else if...else 语句来选择多个代码块之一来执行。
      if (condition1)
      {
          当条件 1 为 true 时执行的代码
      }
      else if (condition2)
      {
          当条件 2 为 true 时执行的代码
      }
      else
      {
        当条件 1 和 条件 2 都不为 true 时执行的代码
      }
      ```

- switch 语句用于基于不同的条件来执行不同的动作。

   ```
   switch(n)
   {
       case 1:
           执行代码块 1
           break;
       case 2:
           执行代码块 2
           break;
       default:
           与 case 1 和 case 2 不同时执行的代码
   }
   ```

- default 关键词

   ```
   var d=new Date().getDay();
   switch (d)
   {
       case 6:x="今天是星期六";
       break;
       case 0:x="今天是星期日";
       break;
       default:
       x="期待周末";
   }
   document.getElementById("demo").innerHTML=x;
   ```

- JavaScript 循环

   - **for** - 循环代码块一定的次数

      ```
      语句 1 （代码块）开始前执行
      语句 2 定义运行循环（代码块）的条件
      语句 3 在循环（代码块）已被执行之后执行

      for (语句 1; 语句 2; 语句 3)
      {
          被执行的代码块
      }
      ```

      

   - **for/in** - 循环遍历对象的属性

   - **while** - 当指定的条件为 true 时循环指定的代码块

   - **do/while** - 同样当指定的条件为 true 时循环指定的代码块

- for/in 语句循环遍历对象的属性

- while 循环

   ```
   while (条件)
   {
       需要执行的代码
   }
   ```

- do/while 循环

   ```
   do/while 循环是 while 循环的变体。该循环会在检查条件是否为真之前执行一次代码块，然后如果条件为真的话，就会重复这个循环。
   do
   {
       需要执行的代码
   }
   while (条件);

   do
   {
       x=x + "The number is " + i + "<br>";
       i++;
   }
   while (i<5);
   ```

- break 语句

   > break 语句可用于跳出循环。
   >
   > break 语句跳出循环后，会继续执行该循环之后的代码（如果有的话）：

   ```js
   for (i=0;i<10;i++)
   {
       if (i==3)
       {
           break;
       }
       x=x + "The number is " + i + "<br>";
   }

   for (i=0;i<10;i++)
   {
       if (i==3) break;
       x=x + "The number is " + i + "<br>";
   }
   ```

- continue 语句

   ```js
   continue 语句中断当前的循环中的迭代，然后继续循环下一个迭代。
   for (i=0;i<=10;i++)
   {
       if (i==3) continue;
       x=x + "The number is " + i + "<br>";
   }
   ```

   ```js
   while (i < 10){
     if (i == 3){
       i++;    //加入i++不会进入死循环
       continue;
     }
     x= x + "该数字为 " + i + "<br>";
     i++;
   }
   ```

- JavaScript 标签

   > 通过标签引用，break 语句可用于跳出任何 JavaScript 代码块

- typeof 操作符

   ```
   你可以使用 typeof 操作符来检测变量的数据类型。
   typeof "John"                // 返回 string
   typeof 3.14                  // 返回 number
   typeof false                 // 返回 boolean
   typeof [1,2,3,4]             // 返回 object
   typeof {name:'John', age:34} // 返回 object
   ```

-  null 表示 "什么都没有"。null是一个只有一个值的特殊类型。表示一个空对象引用。

- **undefined** 是一个没有设置值的变量。(null 和 undefined 的值相等，但类型不等)

- 使用 **typeof** 操作符来查看 JavaScript 变量的数据类型。

   ```
   typeof "John"                 // 返回 string
   typeof 3.14                   // 返回 number
   typeof NaN                    // 返回 number
   typeof false                  // 返回 boolean
   typeof [1,2,3,4]              // 返回 object
   typeof {name:'John', age:34}  // 返回 object
   typeof new Date()             // 返回 object
   typeof function () {}         // 返回 function
   typeof myCar                  // 返回 undefined (如果 myCar 没有声明)
   typeof null                   // 返回 object
   ```

   ```
   请注意：

   NaN 的数据类型是 number
   数组(Array)的数据类型是 object
   日期(Date)的数据类型为 object
   null 的数据类型是 object
   未定义变量的数据类型为 undefined
   如果对象是 JavaScript Array 或 JavaScript Date ，我们就无法通过 typeof 来判断他们的类型，因为都是 返回 object。
   ```

- **constructor** 属性返回所有 JavaScript 变量的构造函数。

- JavaScript 类型转换

   -  **toString()** 转换为字符串

   - Date() 返回字符串。

      | getDate()         | 从 Date 对象返回一个月中的某一天 (1 ~ 31)。 |
      | ----------------- | ------------------------------------------- |
      | getDay()          | 从 Date 对象返回一周中的某一天 (0 ~ 6)。    |
      | getFullYear()     | 从 Date 对象以四位数字返回年份。            |
      | getHours()        | 返回 Date 对象的小时 (0 ~ 23)。             |
      | getMilliseconds() | 返回 Date 对象的毫秒(0 ~ 999)。             |
      | getMinutes()      | 返回 Date 对象的分钟 (0 ~ 59)。             |
      | getMonth()        | 从 Date 对象返回月份 (0 ~ 11)。             |
      | getSeconds()      | 返回 Date 对象的秒数 (0 ~ 59)。             |
      | getTime()         | 返回 1970 年 1 月 1 日至今的毫秒数。        |

   - 全局方法 **Number()** 可以将字符串转换为数字。

   - 当你尝试输出一个对象或一个变量时 JavaScript 会自动调用变量的 toString() 方法

- **search() **方法用于检索字符串中指定的子字符串，或检索与正则表达式相匹配的子字符串，并返回子串的起始位置。

- **replace() **方法用于在字符串中用一些字符串替换另一些字符串，或替换一个与正则表达式匹配的子串。

- javascript错误

   ```
   try {
       ...    //异常的抛出
   } catch(e) {
       ...    //异常的捕获与处理
   } finally {
       ...    //结束处理
   }
   ```

- 如果把 throw 与 try 和 catch 一起使用，那么您能够控制程序流，并生成自定义的错误消息。

   ```html
   <!DOCTYPE html>
   <html>
   <head>
   <meta charset="utf-8">
   <title>菜鸟教程(runoob.com)</title>
   </head>
   <body>

   <p>请输出一个 5 到 10 之间的数字:</p>

   <input id="demo" type="text">
   <button type="button" onclick="myFunction()">测试输入</button>
   <p id="message"></p>

   <script>
   function myFunction() {
       var message, x;
       message = document.getElementById("message");
       message.innerHTML = "";
       x = document.getElementById("demo").value;
       try { 
           if(x == "")  throw "值为空";
           if(isNaN(x)) throw "不是数字";
           x = Number(x);
           if(x < 5)    throw "太小";
           if(x > 10)   throw "太大";
       }
       catch(err) {
           message.innerHTML = "错误: " + err;
       }
   }
   </script>

   </body>
   </html>
   ```

- JavaScript 调试

   - console.log() 方法

- 在 JavaScript 中 this 不是固定不变的，它会随着执行环境的改变而改变：

   - 在方法中，this 表示该方法所属的对象。
   - 如果单独使用，this 表示全局对象。
   - 在函数中，this 表示全局对象。
   - 在函数中，在严格模式下，this 是未定义的(undefined)。
   - 在事件中，this 表示接收事件的元素。
   - 类似 call() 和 apply() 方法可以将 this 引用到任何对象。

- let 声明的变量只在 let 命令所在的代码块内有效。

- const 声明一个只读的常量，一旦声明，常量的值就不能改变。

- 在函数外声明的变量作用域是全局的：全局变量在 JavaScript 程序的任何地方都可以访问。

- 在函数内声明的变量作用域是局部的（函数内）：函数内使用 var 声明的变量只能在函数内容访问，如果不使用 var 则是全局变量。

- JSON 是用于存储和传输数据的格式。JSON 通常用于服务端向网页传递数据 。

   - 数据为 键/值 对。
   - 数据由逗号分隔。
   - 大括号保存对象
   - 方括号保存数组

- 使用 JavaScript 内置函数 JSON.parse() 将字符串转换为 JavaScript 对象:

   ```js
   var obj = JSON.parse(text);
   ```

- JSON.stringify()：用于将 JavaScript 值转换为 JSON 字符串。