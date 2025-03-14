[toc]

##### go学习资料

- Go基础篇：https://www.yuque.com/aceld/mo95lb
- Gin框架介绍及使用：https://www.liwenzhou.com/posts/Go/gin/
- gin框架源码解析：https://www.liwenzhou.com/posts/Go/gin-sourcecode/
- GORM入门指南：https://www.liwenzhou.com/posts/Go/gorm/
- GORM CRUD指南：https://www.liwenzhou.com/posts/Go/gorm-crud/
- Go语言之依赖管理：https://www.liwenzhou.com/posts/Go/dependency/
- 
- Golang HTTP 标准库实现原理：https://mp.weixin.qq.com/s?__biz=MzkxMjQzMjA0OQ==&mid=2247484040&idx=1&sn=b710f4429188ea5f49f6a9155381b67f
- 解析 Golang 网络 IO 模型之 EPOLL：https://mp.weixin.qq.com/s?__biz=MzkxMjQzMjA0OQ==&mid=2247484057&idx=1&sn=50e57108f736bc47137ac57dfb643893
- 解析 Gin 框架底层原理：https://mp.weixin.qq.com/s?__biz=MzkxMjQzMjA0OQ==&mid=2247484076&idx=1&sn=9492d326c820625700345a881b58a849
- Golang context 实现原理：https://mp.weixin.qq.com/s?__biz=MzkxMjQzMjA0OQ==&mid=2247483677&idx=1&sn=d1c0e52b1fd31932867ec9b1d00f4ec2
- Go语言基础之并发：https://www.liwenzhou.com/posts/Go/concurrence/
- 
- 为Go项目编写Makefile：https://www.liwenzhou.com/posts/Go/makefile/
- 使用Docker部署Go Web应用：https://www.liwenzhou.com/posts/Go/deploy-in-docker/
- 部署Go语言项目的 N 种方法：https://www.liwenzhou.com/posts/Go/deploy/



##### 大小写命名规则

- **大写开头** = **Public**（公开）：允许跨包访问。
- **小写开头** = **Private**（私有）：仅限当前包内使用。
- 该规则统一适用于函数、方法、结构体、字段、变量等所有标识符。
- Go通过这种简洁的命名约定替代了传统的关键字（如`public`/`private`），强调代码的明确性和一致性。

##### 声明变量

###### 1. 标准声明（使用 `var` 关键字）

- **显式指定类型**：

  ```go
  var 变量名 类型 = 表达式
  
  var x int = 10
  var name string = "Alice"
  ```

- **类型推断**（省略类型）：

  ```go
  var 变量名 = 表达式
  
  var x = 10          // 类型推断为 int
  var name = "Alice"  // 类型推断为 string
  ```

- **批量声明**：

  ```go
  var (
      变量1 类型1 = 表达式1
      变量2 类型2 = 表达式2
  )
  
  var (
      a int = 5
      b string
      c bool
  )
  ```

- **多变量声明**：

  ```go
  var 变量1, 变量2 类型 = 表达式1, 表达式2
  
  var x, y int = 1, 2
  ```

###### 2. 短变量声明（使用 `:=`）

- **语法**：

  ```go
  变量名 := 表达式
  
  x := 10             // 类型推断为 int
  name := "Alice"     // 类型推断为 string
  a, b := 1, "hello"  // 多变量短声明
  ```

- **限制**：

  - 仅能在函数内部使用（不可用于全局变量）。
  - 左侧必须至少有一个新变量。

###### 3. 默认初始化（零值机制）

```go
// 零值就是变量没有做初始化时系统默认设置的值：

var x int       // x = 0
var y bool		// y = false
var s string    // s = ""

// 以下几种类型为 nil：
var a *int					// 指针pointer
var a []int					// 切片slice
var a map[string] int		// 映射map
var a chan int				// 通道channel
var a func(string) int		// 函数类型function
var a error 				// error 是接口interface
```

###### 4. 其他方式

- **`new` 函数**：创建指针并初始化为零值。

  ```go
  p := new(int)    // p 类型为 *int，指向的值为 0
  ```

- **`make` 函数**：初始化切片、映射、通道等引用类型。

  ```go
  slice := make([]int, 5)  // 长度为5的切片
  m := make(map[string]int)  // 初始化空映射
  ```

###### 支持的数据类型

1. **基本数据类型**

   - **整型**：
     `int`, `int8`, `int16`, `int32`, `int64`
     `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr`

   - **浮点型**：
     `float32`, `float64`

   - **复数型**：
     `complex64`, `complex128`

   - **布尔型**：
     `bool`（值为 `true`/`false`）

   - **字符串**：
     `string`（UTF-8编码）

2. **复合数据类型**

   - **数组（Array）**：
     固定长度，如 `var arr [3]int`。

   - **切片（Slice）**：
     动态数组，如 `slice := []int{1, 2, 3}`。

   - **映射（Map）**：
     键值对集合，如 `m := map[string]int{"a": 1}`。

   - **结构体（Struct）**：

     ```go
     // 自定义类型
     
     type Person struct {
         Name string
         Age  int
     }
     func main() {
     	var p Person
     	var q *Person
     	fmt.Println(p)  // { 0}
     	fmt.Println(q)  // <nil>
     }
     ```

   - **指针（Pointer）**：
     存储内存地址，如 `var p *int`。

   - **函数类型（Function）**：
     函数作为变量，如 `var f func(int) int`。

   - **接口（Interface）**：
     定义方法集合，如 `var w io.Writer`。

   - **通道（Channel）**：
     用于协程通信，如 `ch := make(chan int)`。

3. **特殊类型**

   - **类型别名（Type Alias）**：
     通过 `type Alias = T` 定义，如 `type Byte = uint8`。

   - **自定义类型（Type Definition）**：
     通过 `type NewType T` 定义，如 `type MyInt int`。

   - **空接口（`interface{}`）**：
     可接受任意类型的值，如 `var any interface{} = 42`。

4. **零值对照表**

   | **类型**                     | **零值**         |
   | :--------------------------- | :--------------- |
   | 数值类型（int等）            | `0`              |
   | 布尔类型                     | `false`          |
   | 字符串                       | `""`（空字符串） |
   | 指针、切片、映射、通道、接口 | `nil`            |
   | 结构体                       | 各字段的零值     |



##### 条件语句

###### if 语句

> **if 语句** 由一个布尔表达式后紧跟一个或多个语句组成。

```go
if 布尔表达式 {
   /* 在布尔表达式为 true 时执行 */
}
```

###### if...else 语句

> if 语句 后可以使用可选的 else 语句, else 语句中的表达式在布尔表达式为 false 时执行。

```go
if 布尔表达式 {
   /* 在布尔表达式为 true 时执行 */
} else {
  /* 在布尔表达式为 false 时执行 */
}
```

###### if 嵌套语句

> 在 if 或 else if 语句中嵌入一个或多个 if 或 else if 语句。

```go
if 布尔表达式 1 {
   /* 在布尔表达式 1 为 true 时执行 */
   if 布尔表达式 2 {
      /* 在布尔表达式 2 为 true 时执行 */
   }
}

/* 同样的方式在 if 语句中嵌套 else if...else 语句
```

###### switch语句

> switch 语句用于基于不同条件执行不同动作，每一个 case 分支都是唯一的，从上至下逐一测试，直到匹配为止。

```go
switch var1 {
    case val1:
        ...
    case val2:
        ...
    default:
        ...
}
```

###### Type Switch

> switch 语句还可以被用于 type-switch 来判断某个 interface 变量中实际存储的变量类型。

```go
package main

import "fmt"

func main() {
   var x interface{}
     
   switch i := x.(type) {
      case nil:   
         fmt.Printf(" x 的类型 :%T",i)                
      case int:   
         fmt.Printf("x 是 int 型")                       
      case float64:
         fmt.Printf("x 是 float64 型")           
      case func(int) float64:
         fmt.Printf("x 是 func(int) 型")                      
      case bool, string:
         fmt.Printf("x 是 bool 或 string 型" )       
      default:
         fmt.Printf("未知型")     
   }   
}
```

###### fallthrough

> 使用 fallthrough 会强制执行后面的 case 语句，fallthrough 不会判断下一条 case 的表达式结果是否为 true。

```go
package main

import "fmt"

func main() {

    switch {
    case false:
            fmt.Println("1、case 条件语句为 false")
            fallthrough
    case true:
            fmt.Println("2、case 条件语句为 true")
            fallthrough
    case false:
            fmt.Println("3、case 条件语句为 false")
            fallthrough
    case true:
            fmt.Println("4、case 条件语句为 true")
    case false:
            fmt.Println("5、case 条件语句为 false")
            fallthrough
    default:
            fmt.Println("6、默认 case")
    }
}
```

###### select 语句

> select 是 Go 中的一个控制结构，类似于 switch 语句。
>
> select 语句只能用于通道操作，每个 case 必须是一个通道操作，要么是发送要么是接收。
>
> select 语句会监听所有指定的通道上的操作，一旦其中一个通道准备好就会执行相应的代码块。
>
> 如果多个通道都准备好，那么 select 语句会随机选择一个通道执行。如果所有通道都没有准备好，那么执行 default 块中的代码。

```go
package main

import "fmt"

func main() {
  // 定义两个通道
  ch1 := make(chan string)
  ch2 := make(chan string)

  // 启动两个 goroutine，分别从两个通道中获取数据
  go func() {
    for {
      ch1 <- "from 1"
    }
  }()
  go func() {
    for {
      ch2 <- "from 2"
    }
  }()

  // 使用 select 语句非阻塞地从两个通道中获取数据
  for {
    select {
    case msg1 := <-ch1:
      fmt.Println(msg1)
    case msg2 := <-ch2:
      fmt.Println(msg2)
    default:
      // 如果两个通道都没有可用的数据，则执行这里的语句
      fmt.Println("no message received")
    }
  }
}
```

##### 循环语句

> for 循环是一个循环控制结构

1. 第一种形式

   ```go
   for init; condition; post { }
   
   /*
   init： 一般为赋值表达式，给控制变量赋初值；
   condition： 关系表达式或逻辑表达式，循环控制条件；
   post： 一般为赋值表达式，给控制变量增量或减量。
   ```

2. 第二种形式

   ```go
   for condition { }
   ```

3. 第三种形式

   ```go
   // 无限循环
   
   for { }
   ```

4. for 循环的 range 格式

   > for 循环的 range 格式可以对 slice、map、数组、字符串等进行迭代循环。

   - 针对map

   ```go
   for key, value := range oldMap {
       newMap[key] = value
   }
   
   // 只想读取 key，格式如下：
   for key := range oldMap
   for key, _ := range oldMap
   
   // 只想读取 value，格式如下：
   for _, value := range oldMap
   ```

   - 针对字符串、切片等

   ```go
   package main
   import "fmt"
   
   func main() {
      strings := []string{"google", "runoob"}
      for i, s := range strings {   // i 是索引值
         fmt.Println(i, s)
      }
   
   
      numbers := [6]int{1, 2, 3, 5} 
      for i,x:= range numbers {
         fmt.Printf("第 %d 位 x 的值 = %d\n", i,x)
      }  
   }
   ```

##### 基本数据类型

- 在 Go 编程语言中，数据类型用于声明函数和变量。
- 数据类型的出现是为了把数据分成所需内存大小不同的数据，编程的时候需要用大数据的时候才需要申请大内存，就可以充分利用内存。

###### 1. 布尔型(bool)

```go
// 布尔型的值只可以是常量 true 或者 false
var b bool = true
```

###### 2. 数字类型

- 整型：int
  - uint8、int8
  - uint16、int16
  - uint32、int32
  - uint64、int64
- 浮点型：float32、float64、complex64、complex128

###### 3. 字符串类型

> 字符串就是一串固定长度的字符连接起来的字符序列。Go 的字符串是由单个字节连接起来的。Go 语言的字符串的字节使用 UTF-8 编码标识 Unicode 文本。

###### 4. 派生类型

1. 指针类型（Pointer）
2. 数组类型
3. 结构化类型（struct）
4. Channel 类型
5. 函数类型（fun）
6. 切片类型（slice）
7. 接口类型（interface）
8. Map 类型（map）

##### 指针类型

> 变量是一种使用方便的占位符，用于引用计算机内存地址。
>
> Go 语言的取地址符是 &，放到一个变量前使用就会返回相应变量的内存地址。

- 声明指针

  ```go
  // 一个指针变量指向了一个值的内存地址
  // 类似于变量和常量，在使用指针前你需要声明指针
  
  var var_name *var-type
  // ar-type 为指针类型，var_name 为指针变量名，* 号用于指定变量是作为一个指针
  ```

- 使用指针：在指针类型前面加上 * 号（前缀）来获取指针所指向的内容

- 空指针

  ```go
  // 当一个指针被定义后没有分配到任何变量时，它的值为 nil
  // 一个指针变量通常缩写为 ptr，即Pointer
  
  // 空指针判断：
  if(ptr != nil)     /* ptr 不是空指针 */
  if(ptr == nil)    /* ptr 是空指针 */
  ```

- 指针数组

  ```go
  // ptr 为整型指针数组
  var ptr [MAX]*int;
  ```

- 向函数传递指针数组

##### 数组类型

> 数组是具有**相同唯一类型**的一组已编号且长度固定的数据项序列
>
> 在 Go 语言中，数组的大小是类型的一部分，因此不同大小的数组是不兼容的

- 使用声明

  ```go
  // Go 语言数组声明需要指定元素类型及元素个数
  // 其中，arrayName 是数组的名称，size 是数组的大小，dataType 是数组中元素的数据类型。
  var arrayName [size]dataType
  ```

- 使用初始化列表来初始化数组的元素

  ```go
  // 初始化数组中 {} 中的元素个数不能大于 [] 中的数字
  
  var numbers = [5]int{1, 2, 3, 4, 5}
  ```

- 使用 **:=** 简短声明语法来声明和初始化数组

  ```go
  numbers := [5]int{1, 2, 3, 4, 5}
  ```

- 如果数组长度不确定，可以使用 **...** 代替数组的长度，编译器会根据元素个数自行推断数组的长度

  ```go
  var balance = [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
  或
  balance := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
  ```

- 如果设置了数组的长度，我们还可以通过指定下标来初始化元素

  ```go
  //  将索引为 1 和 3 的元素初始化
  balance := [5]float32{1:2.0,3:7.0}
  ```

##### 结构化类型（struct）

> 结构体是由一系列具有相同类型或不同类型的数据构成的数据集合
>
> Go 语言中数组可以存储同一类型的数据，但在结构体中我们可以为不同项定义不同的数据类型。

- 定义结构体

  ```go
  // truct 语句定义一个新的数据类型，结构体中有一个或多个成员
  // ype 语句设定了结构体的名称
  
  type struct_variable_type struct {
     member definition
     member definition
     ...
     member definition
  }
  ```

- 用于变量的声明

  ```go
  variable_name := structure_variable_type {value1, value2...valuen}
  或
  variable_name := structure_variable_type { key1: value1, key2: value2..., keyn: valuen}
  
  var Book1 Books        /* 声明 Book1 为 Books 类型 */
  ```

- 访问结构体成员

  ```go
  结构体.成员名
  ```

- 结构体指针：定义指向结构体的指针类似于其他指针变量

  ```go
  var struct_pointer *Books
  
  // 使用结构体指针访问结构体成员，使用 "." 操作符：
  struct_pointer.title
  
  //查看结构体变量地址，可以将 & 符号放置于结构体变量前：
  struct_pointer = &Book1
  ```

##### 函数类型

> 函数声明告诉了编译器函数的**名称**、**参数**和**返回类型**。
>
> 函数是基本的代码块，用于执行一个任务。
>
> 通过函数来划分不同功能，逻辑上每个函数执行的是指定的任务。

- 函数的定义

  ```go
  func function_name( [parameter list] ) [return_types_list] {
     函数体
  }
  /*
  func：函数由 func 开始声明
  function_name：函数名称，参数列表和返回值类型构成了函数签名。
  parameter list：参数列表，参数就像一个占位符，当函数被调用时，你可以将值传递给参数，这个值被称为实际参数。参数列表指定的是参数类型、顺序、及参数个数。参数是可选的，也就是说函数也可以不包含参数。
  return_types：返回类型，函数返回一列值。return_types 是该列值的数据类型。有些功能不需要返回值，这种情况下 return_types 不是必须的。
  函数体：函数定义的代码集合。
  /*
  ```

- 函数的参数传递

  > 函数如果使用参数，该变量可称为函数的形参。
  >
  > 形参就像定义在函数体内的局部变量。

  - 值传递：值传递是指在调用函数时将实际参数复制一份传递到函数中，这样在函数中如果对参数进行修改，将不会影响到实际参数。
  - 引用传递：引用传递是指在调用函数时将实际参数的地址传递到函数中，那么在函数中对参数所进行的修改，将影响到实际参数。

- 函数作为另一个函数的实参：函数定义后可作为另外一个函数的实参数传入

- 函数闭包（匿名函数）

  > 匿名函数是一种没有函数名的函数，通常用于在函数内部定义函数，或者作为函数参数进行传递。
  >
  > 匿名函数的优越性在于可以直接使用函数内的变量，不必申明。

  - 将匿名函数赋值给变量、在函数内部使用匿名函数以及将匿名函数作为参数传递给其他函数

    ```go
    package main
    
    import "fmt"
    
    func main() {
    	// 定义一个匿名函数并将其赋值给变量add
    	add := func(a, b int) int {
    		return a + b
    	}
    
    	// 调用匿名函数
    	result := add(3, 5)
    	fmt.Println("3 + 5 =", result)
    
    	// 在函数内部使用匿名函数
    	multiply := func(x, y int) int {
    		return x * y
    	}
    
    	product := multiply(4, 6)
    	fmt.Println("4 * 6 =", product)
    
    	// 将匿名函数作为参数传递给其他函数
    	calculate := func(operation func(int, int) int, x, y int) int {
    		return operation(x, y)
    	}
    
    	sum := calculate(add, 2, 8)
    	fmt.Println("2 + 8 =", sum)
    
    	// 也可以直接在函数调用中定义匿名函数
    	difference := calculate(func(a, b int) int {
    		return a - b
    	}, 10, 4)
    	fmt.Println("10 - 4 =", difference)
    }
    ```

- 函数方法

  > 一个方法就是一个**包含了接受者的函数**，接受者可以是命名类型或者结构体类型的一个值或者是一个指针。所有给定类型的方法属于该类型的方法集。

  - 语法

    ```go
    func (variable_name variable_data_type) function_name() [return_type]{
       /* 函数体*/
    }
    ```

##### 切片类型

- 切片是对数组的抽象，即“动态数组”，长度是不固定的，可以追加元素，在追加时可能使切片的容量增大
- 切片是可索引的，并且可以由 len() 方法获取长度
- 切片提供了计算容量的方法 cap() 可以测量切片最长可以达到多少
- Go 数组的长度不可改变

###### 定义切片

1. 声明一个未指定大小的数组来定义切片

   ```go
   // 一个切片在未初始化之前默认为 nil，长度为 0
   
   var slice1 []type
   ```

2. make()函数来创建切片

   - 指定数组长度

   ```go
   var slice1 []type = make([]type, len)
   
   
   也可以简写为
   
   
   slice1 := make([]type, len)
   ```

   - 指定长度和容量

   ```go
   slice1 := make([]type, length, capacity)
   ```

3. 切片初始化

   ```go
   // []表示是切片类型，{1,2,3}初始化值依次是1,2,3.其cap=len=3
   
   slice1 := []int{1, 2, 3}
   ```

4. append() 和 copy() 函数

   ```go
   /* 允许追加空切片 */
   numbers = append(numbers, 0)
   
   /* 拷贝 numbers 的内容到 numbers1 */
   copy(numbers1,numbers)
   ```

##### 接口类型

> 接口（interface）是 Go 语言中的一种类型，用于定义行为的集合，它通过描述类型必须实现的方法，规定了类型的行为契约。
>
> 它把所有的具有共性的方法定义在一起，任何其他类型只要实现了这些方法就是实现了这个接口。
>
> 接口可以让我们将不同的类型绑定到一组公共的方法上，从而实现多态和灵活的设计。

###### 接口的特点

1. 隐式实现：
   - Go 中没有关键字显式声明某个类型实现了某个接口。
   - 只要一个类型实现了接口要求的所有方法，该类型就自动被认为实现了该接口。
2. 接口类型变量
   - 接口变量可以存储实现该接口的任意值。
   - 接口变量实际上包含了两个部分：
     - **动态类型**：存储实际的值类型。
     - **动态值**：存储具体的值。
3. 零值接口
   - 接口的零值是 `nil`。
   - 一个未初始化的接口变量其值为 `nil`，且不包含任何动态类型或值。
4. 空接口
   - 定义为 `interface{}`，可以表示任何类型。

###### 接口常见用法

1. **多态**：不同类型实现同一接口，实现多态行为。
2. **解耦**：通过接口定义依赖关系，降低模块之间的耦合。
3. **泛化**：使用空接口 `interface{}` 表示任意类型。

###### 接口定义和实现

```go
/* 定义接口 */
type interface_name interface {
   method_name1 [return_type]
   method_name2 [return_type]
   method_name3 [return_type]
   ...
   method_namen [return_type]
}

/* 定义结构体 */
type struct_name struct {
   /* variables */
}

/* 实现接口方法 */
func (struct_name_variable struct_name) method_name1() [return_type] {
   /* 方法实现 */
}
...
func (struct_name_variable struct_name) method_namen() [return_type] {
   /* 方法实现*/
}
```

- 实例

  ```go
  package main
  
  import (
          "fmt"
          "math"
  )
  
  // 定义接口
  type Shape interface {
          Area() float64
          Perimeter() float64
  }
  
  // 定义一个结构体
  type Circle struct {
          Radius float64
  }
  
  // Circle 实现 Shape 接口
  func (c Circle) Area() float64 {
          return math.Pi * c.Radius * c.Radius
  }
  
  func (c Circle) Perimeter() float64 {
          return 2 * math.Pi * c.Radius
  }
  
  func main() {
          c := Circle{Radius: 5}
          var s Shape = c // 接口变量可以存储实现了接口的类型
          fmt.Println("Area:", s.Area())
          fmt.Println("Perimeter:", s.Perimeter())
  }
  ```

###### 空接口

> 空接口 `interface{}` 是 Go 的特殊接口，表示所有类型的超集。
>
> - 任意类型都实现了空接口。
> - 常用于需要存储任意类型数据的场景，如泛型容器、通用参数等。

```go
package main

import "fmt"

func printValue(val interface{}) {
        fmt.Printf("Value: %v, Type: %T\n", val, val)
}

func main() {
        printValue(42)         // int
        printValue("hello")    // string
        printValue(3.14)       // float64
        printValue([]int{1, 2}) // slice
}
```

###### 类型断言

> 类型断言用于从接口类型中提取其底层值。

```go
value := iface.(Type)
/*
iface 是接口变量。
Type 是要断言的具体类型。
如果类型不匹配，会触发 panic。
/*
```

```go
package main

import "fmt"

func main() {
        var i interface{} = "hello"
        str := i.(string) // 类型断言
        fmt.Println(str)  // 输出：hello
}
```

###### 带检查的类型断言

> 为了避免 panic，可以使用带检查的类型断言：value, ok := iface.(Type)
>
> - `ok` 是一个布尔值，表示断言是否成功。
> - 如果断言失败，`value` 为零值，`ok` 为 `false`。

```go
package main

import "fmt"

func main() {
        var i interface{} = 42
        if str, ok := i.(string); ok {
                fmt.Println("String:", str)
        } else {
                fmt.Println("Not a string")
        }
}
```

###### 类型检查

> type switch 是 Go 中的语法结构，用于根据接口变量的具体类型执行不同的逻辑。

```go
package main

import "fmt"

func printType(val interface{}) {
        switch v := val.(type) {
        case int:
                fmt.Println("Integer:", v)
        case string:
                fmt.Println("String:", v)
        case float64:
                fmt.Println("Float:", v)
        default:
                fmt.Println("Unknown type")
        }
}

func main() {
        printType(42)
        printType("hello")
        printType(3.14)
        printType([]int{1, 2, 3})
}
```

###### 接口组合

> 接口可以通过嵌套组合，实现更复杂的行为描述。

```go
package main

import "fmt"

type Reader interface {
        Read() string
}

type Writer interface {
        Write(data string)
}

type ReadWriter interface {
        Reader
        Writer
}

type File struct{}

func (f File) Read() string {
        return "Reading data"
}

func (f File) Write(data string) {
        fmt.Println("Writing data:", data)
}

func main() {
        var rw ReadWriter = File{}
        fmt.Println(rw.Read())
        rw.Write("Hello, Go!")
}
```

###### 动态值和动态类型

> 接口变量实际上包含了两部分：
>
> 1. **动态类型**：接口变量存储的具体类型。
> 2. **动态值**：具体类型的值。

```go
package main

import "fmt"

func main() {
        var i interface{} = 42
        fmt.Printf("Dynamic type: %T, Dynamic value: %v\n", i, i)
}

// Dynamic type: int, Dynamic value: 42
```

###### 接口的零值

> 接口的零值是 nil。
>
> 当接口变量的动态类型和动态值都为 nil 时，接口变量为 nil。

```go
package main

import "fmt"

func main() {
        var i interface{}
        fmt.Println(i == nil) // 输出：true
}
```

##### map类型

> 语法：map[KeyType]ValueType

1. 使用声明

   ```go
   var test1 map[string]string
   //在使用map前，需要先make，make的作用就是给map分配数据空间
   test1 = make(map[string]string, 10) 
   test1["one"] = "php"
   ```

2. make()函数来创建map

   ```go
   test2 := make(map[string]string)
   ```

3. map初始化

   ```go
   test3 := map[string]string{
           "one" : "php",
           "two" : "golang",
           "three" : "java",
       }
   ```

4. 嵌套

   ```go
   language := make(map[string]map[string]string)
   language["php"] = make(map[string]string, 1)
   language["php"]["id"] = "1"
   language["php"]["desc"] = "php是世界上最美的语言"
   ```

##### 面向对象

```go
package main

import "fmt"
import "math"

type Point struct{ X, Y float64 }

// 这是给struct Point类型定义一个方法
func (p Point) Distance(q Point) float64 {
	return math.Hypot(q.X-p.X, q.Y-p.Y)
}

func (p Point) Add(another Point) Point {
	return Point{p.X + another.X, p.Y + another.Y}
}

func (p Point) Sub(another Point) Point {
	return Point{p.X - another.X, p.Y - another.Y}
}

func (p Point) Print() {
	fmt.Printf("{%f, %f}\n", p.X, p.Y)
}

// 定义一个Point切片类型 Path
type Path []Point

// 方法的接收器 是Path类型数据, 方法的选择器是TranslateBy(Point, bool)
func (path Path) TranslateBy(another Point, add bool) {
	var op func(p, q Point) Point //定义一个 op变量 类型是方法表达式 能够接收Add,和 Sub方法
	if add == true {
		op = Point.Add //给op变量赋值为Add方法
	} else {
		op = Point.Sub //给op变量赋值为Sub方法
	}

	for i := range path {
		//调用 path[i].Add(another) 或者 path[i].Sub(another)
		path[i] = op(path[i], another)
		path[i].Print()
	}
}

func main() {

	points := Path{
		{10, 10},
		{11, 11},
	}

	anotherPoint := Point{5, 5}

	points.TranslateBy(anotherPoint, false)

	fmt.Println("------------------")

	points.TranslateBy(anotherPoint, true)
}
/*
{5.000000, 5.000000}
{6.000000, 6.000000}
------------------
{10.000000, 10.000000}
{11.000000, 11.000000}
/*
```

##### goroutine

```go
package main

import (
	"fmt"
	"time"
)

func newTask() {
	i := 0
	for {
		i++
		fmt.Printf("new goroutine: i = %d\n", i)
		time.Sleep(1 * time.Second) //延时1s
	}
}

func main() {
	//创建一个 goroutine，启动另外一个任务
	go newTask()
	i := 0
	//main goroutine 循环打印
	for {
		i++
		fmt.Printf("main goroutine: i = %d\n", i)
		time.Sleep(1 * time.Second) //延时1s
	}
}
```

##### channel类型

```go
package main
 
import (
    "fmt"
)
 
func main() {
    c := make(chan int)
 
    go func() {
        defer fmt.Println("子go程结束")
 
        fmt.Println("子go程正在运行……")
 
        c <- 666 //666发送到c
    }()
 
    num := <-c //从c中接收数据，并赋值给num
 
    fmt.Println("num = ", num)
    fmt.Println("main go程结束")
}
```

###### 无缓冲的channel

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	c := make(chan int, 0) //创建无缓冲的通道 c

	//内置函数 len 返回未被读取的缓冲元素数量，cap 返回缓冲区大小
	fmt.Printf("len(c)=%d, cap(c)=%d\n", len(c), cap(c))

	go func() {
		defer fmt.Println("子go程结束")

		for i := 0; i < 3; i++ {
			c <- i
			fmt.Printf("子go程正在运行[%d]: len(c)=%d, cap(c)=%d\n", i, len(c), cap(c))
		}
	}()

	time.Sleep(2 * time.Second) //延时2s

	for i := 0; i < 3; i++ {
		num := <-c //从c中接收数据，并赋值给num
		fmt.Println("num = ", num)
	}

	fmt.Println("main进程结束")
}
```

###### 有缓冲的channel

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	c := make(chan int, 3) //创建无缓冲的通道 c

	//内置函数 len 返回未被读取的缓冲元素数量，cap 返回缓冲区大小
	fmt.Printf("len(c)=%d, cap(c)=%d\n", len(c), cap(c))

	go func() {
		defer fmt.Println("子go程结束")

		for i := 0; i < 3; i++ {
			c <- i
			fmt.Printf("子go程正在运行[%d]: len(c)=%d, cap(c)=%d\n", i, len(c), cap(c))
		}
	}()

	time.Sleep(2 * time.Second) //延时2s

	for i := 0; i < 3; i++ {
		num := <-c //从c中接收数据，并赋值给num
		fmt.Println("num = ", num)
	}

	fmt.Println("main进程结束")
}
```

###### 关闭channel

```go
package main
 
import (
    "fmt"
)
 
func main() {
    c := make(chan int)
 
    go func() {
        for i := 0; i < 5; i++ {
            c <- i
        }
        close(c)
    }()
 
    for {
        //ok为true说明channel没有关闭，为false说明管道已经关闭
        if data, ok := <-c; ok {
            fmt.Println(data)
        } else {
            break
        }
    }
 
    fmt.Println("Finished")
}
```

###### channel的方向性

- 默认情况下，通道channel是双向的，也就是，既可以往里面发送数据也可以同里面接收数据。

```go
var ch1 chan int       // ch1是一个正常的channel，是双向的
var ch2 chan<- float64 // ch2是单向channel，只用于写float64数据
var ch3 <-chan int     // ch3是单向channel，只用于读int数据
```

- 可以将 channel 隐式转换为单向队列，只收或只发，不能将单向 channel 转换为普通 channel：

  ```go
  c := make(chan int, 3)
  var send chan<- int = c // send-only
  var recv <-chan int = c // receive-only
  send <- 1
  //<-send //invalid operation: <-send (receive from send-only type chan<- int)
  <-recv
  //recv <- 2 //invalid operation: recv <- 2 (send to receive-only type <-chan int)
  
  //不能将单向 channel 转换为普通 channel
  d1 := (chan int)(send) //cannot convert send (type chan<- int) to type chan int
  d2 := (chan int)(recv) //cannot convert recv (type <-chan int) to type chan int
  ```

  ```go
  //   chan<- //只写
  func counter(out chan<- int) {
      defer close(out)
      for i := 0; i < 5; i++ {
          out <- i //如果对方不读 会阻塞
      }
  }
   
  //   <-chan //只读
  func printer(in <-chan int) {
      for num := range in {
          fmt.Println(num)
      }
  }
   
  func main() {
      c := make(chan int) //   chan   //读写
   
      go counter(c) //生产者
      printer(c)    //消费者
   
      fmt.Println("done")
  }
  ```

##### select

- 通过select可以监听channel上的数据流动

```go
select {
case <- chan1:
    // 如果chan1成功读到数据，则进行该case处理语句
case chan2 <- 1:
    // 如果成功向chan2写入数据，则进行该case处理语句
default:
    // 如果上面都没有成功，则进入default处理流程
}
```

```go
package main

import (
	"fmt"
)

func fibonacci(c, quit chan int) {
	x, y := 1, 1
	for {
		select {
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}

func main() {
	c := make(chan int)
	quit := make(chan int)

	go func() {
		for i := 0; i < 6; i++ {
			fmt.Println(<-c)
		}
		quit <- 0
	}()

	fibonacci(c, quit)
}
```

##### 依赖管理

1. 模块初始化：go mod init <module-name>

2. 安装依赖：**`go get package@version`**：安装指定版本（如`go get github.com/gin-gonic/gin@v1.8.0`）

   - **依赖存储位置**：全局缓存（`GOPATH/pkg/mod`），无需虚拟环境。
   - **版本控制**：依赖版本通过语义化版本（如`v1.9.1`）或Git提交哈希指定。

3. 升级依赖：

   ```go
   go get -u github.com/gin-gonic/gin  # 升级到最新次要/补丁版本
   go get github.com/gin-gonic/gin@v1.9.0  # 指定版本
   ```

4. 文件说明

   - **`go.mod`**：声明依赖及版本。
   - **`go.sum`**：记录依赖的哈希校验值，确保代码完整性一致性。

5. **`go mod tidy`**：清理未使用的依赖，添加缺失的依赖。

6. **`go mod download`**：下载模块到本地缓存。

7. **`go list -m all`**：查看所有依赖版本。

##### 参数获取

###### 1. 获取querystring参数

> `querystring`指的是URL中`?`后面携带的参数
>
> c.DefaultQuery()
>
> c.Query()

```go
func main() {
	//Default返回一个默认的路由引擎
	r := gin.Default()
	r.GET("/user/search", func(c *gin.Context) {
		username := c.DefaultQuery("username", "小王子")
		//username := c.Query("username")
		address := c.Query("address")
		//输出json结果给调用方
		c.JSON(http.StatusOK, gin.H{
			"message":  "ok",
			"username": username,
			"address":  address,
		})
	})
	r.Run()
}
```

###### 2. 获取form参数

> 当前端请求的数据通过form表单提交时
>
> c.DefaultPostForm()
>
> c.PostForm()

```go
func main() {
	//Default返回一个默认的路由引擎
	r := gin.Default()
	r.POST("/user/search", func(c *gin.Context) {
		// DefaultPostForm取不到值时会返回指定的默认值
		//username := c.DefaultPostForm("username", "小王子")
		username := c.PostForm("username")
		address := c.PostForm("address")
		//输出json结果给调用方
		c.JSON(http.StatusOK, gin.H{
			"message":  "ok",
			"username": username,
			"address":  address,
		})
	})
	r.Run(":8080")
}
```

###### 3. 获取JSON参数

> 当前端请求的数据通过JSON提交时

- 手动解析原始请求体：c.GetRawData()

  ```go
  r.POST("/json", func(c *gin.Context) {
  	// 注意：下面为了举例子方便，暂时忽略了错误处理
  	b, _ := c.GetRawData()  // 从c.Request.Body读取请求数据
  	// 定义map或结构体
  	var m map[string]interface{}
  	// 反序列化
  	_ = json.Unmarshal(b, &m)
  
  	c.JSON(http.StatusOK, m)
  })
  
  func HandleRawJSON(c *gin.Context) {
      // 读取请求体
      rawData, err := c.GetRawData()
      if err != nil {
          c.JSON(400, gin.H{"error": "读取数据失败"})
          return
      }
      
      // 解析为 map 或自定义结构体
      var jsonData map[string]interface{}
      if err := json.Unmarshal(rawData, &jsonData); err != nil {
          c.JSON(400, gin.H{"error": "JSON 解析失败"})
          return
      }
      
      // 处理数据
      c.JSON(200, gin.H{"data": jsonData})
  }
  ```

- 使用 `ShouldBindJSON` 或 `BindJSON` 绑定到结构体

  > 直接将 JSON 数据解析到预定义的结构体中，并自动验证数据类型。

  ```go
  type UserRequest struct {
      Name  string `json:"name" binding:"required"`  // 必填字段
      Email string `json:"email" binding:"required,email"` // 必填且需符合邮箱格式
      Age   int    `json:"age"`  // 可选字段
  }
  
  func CreateUser(c *gin.Context) {
      var req UserRequest
      // 使用 ShouldBindJSON（推荐）
      if err := c.ShouldBindJSON(&req); err != nil {
          c.JSON(400, gin.H{"error": err.Error()})
          return
      }
      // 处理业务逻辑
      c.JSON(200, gin.H{"data": req})
  }
  ```

- 使用 ShouldBindBodyWith 多次绑定

  > 适用于需要 **多次解析同一请求体到不同结构体** 的场景。

  ```go
  func MultiBind(c *gin.Context) {
      var user UserRequest
      var logData LogRequest
      
      // 第一次绑定到 UserRequest
      if err := c.ShouldBindBodyWith(&user, binding.JSON); err != nil {
          c.JSON(400, gin.H{"error": "用户数据错误"})
          return
      }
      
      // 第二次绑定到 LogRequest
      if err := c.ShouldBindBodyWith(&logData, binding.JSON); err != nil {
          c.JSON(400, gin.H{"error": "日志数据错误"})
          return
      }
  }
  ```

- 直接操作 gin.Context 的请求体（不推荐）

  > 仅用于特殊场景（如中间件预处理），需注意请求体只能读取一次。

  ```go
  func ReadBodyDirectly(c *gin.Context) {
      // 读取请求体
      body := c.Request.Body
      defer body.Close()
      
      data, err := io.ReadAll(body)
      if err != nil {
          c.JSON(500, gin.H{"error": "读取 Body 失败"})
          return
      }
      
      // 直接使用 data
      c.String(200, string(data))
  }
  ```

###### 4. 获取path参数

> 请求的参数通过URL路径传递
>
> c.Param()

```go
func main() {
	//Default返回一个默认的路由引擎
	r := gin.Default()
	r.GET("/user/search/:username/:address", func(c *gin.Context) {
		username := c.Param("username")
		address := c.Param("address")
		//输出json结果给调用方
		c.JSON(http.StatusOK, gin.H{
			"message":  "ok",
			"username": username,
			"address":  address,
		})
	})

	r.Run(":8080")
}
```

###### 5. 参数绑定

> 基于请求的`Content-Type`识别请求数据类型并利用反射机制自动提取请求中`QueryString`、`form表单`、`JSON`、`XML`等参数到结构体中
>
> c.ShouldBind(&login)

```go
// Binding from JSON
type Login struct {
	User     string `form:"user" json:"user" binding:"required"`
	Password string `form:"password" json:"password" binding:"required"`
}

func main() {
	router := gin.Default()

	// 绑定JSON的示例 ({"user": "q1mi", "password": "123456"})
	router.POST("/loginJSON", func(c *gin.Context) {
		var login Login

		if err := c.ShouldBind(&login); err == nil {
			fmt.Printf("login info:%#v\n", login)
			c.JSON(http.StatusOK, gin.H{
				"user":     login.User,
				"password": login.Password,
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		}
	})

	// 绑定form表单示例 (user=q1mi&password=123456)
	router.POST("/loginForm", func(c *gin.Context) {
		var login Login
		// ShouldBind()会根据请求的Content-Type自行选择绑定器
		if err := c.ShouldBind(&login); err == nil {
			c.JSON(http.StatusOK, gin.H{
				"user":     login.User,
				"password": login.Password,
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		}
	})

	// 绑定QueryString示例 (/loginQuery?user=q1mi&password=123456)
	router.GET("/loginForm", func(c *gin.Context) {
		var login Login
		// ShouldBind()会根据请求的Content-Type自行选择绑定器
		if err := c.ShouldBind(&login); err == nil {
			c.JSON(http.StatusOK, gin.H{
				"user":     login.User,
				"password": login.Password,
			})
		} else {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		}
	})

	// Listen and serve on 0.0.0.0:8080
	router.Run(":8080")
}
```

##### 文件上传

###### 单文件上传

```go
func main() {
	router := gin.Default()
	// 处理multipart forms提交文件时默认的内存限制是32 MiB
	// 可以通过下面的方式修改
	// router.MaxMultipartMemory = 8 << 20  // 8 MiB
	router.POST("/upload", func(c *gin.Context) {
		// 单个文件
		file, err := c.FormFile("f1")
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"message": err.Error(),
			})
			return
		}

		log.Println(file.Filename)
		dst := fmt.Sprintf("C:/tmp/%s", file.Filename)
		// 上传文件到指定的目录
		c.SaveUploadedFile(file, dst)
		c.JSON(http.StatusOK, gin.H{
			"message": fmt.Sprintf("'%s' uploaded!", file.Filename),
		})
	})
	router.Run()
}
```

###### 多文件上传

```go
func main() {
	router := gin.Default()
	// 处理multipart forms提交文件时默认的内存限制是32 MiB
	// 可以通过下面的方式修改
	// router.MaxMultipartMemory = 8 << 20  // 8 MiB
	router.POST("/upload", func(c *gin.Context) {
		// Multipart form
		form, _ := c.MultipartForm()
		files := form.File["file"]

		for index, file := range files {
			log.Println(file.Filename)
			dst := fmt.Sprintf("C:/tmp/%s_%d", file.Filename, index)
			// 上传文件到指定的目录
			c.SaveUploadedFile(file, dst)
		}
		c.JSON(http.StatusOK, gin.H{
			"message": fmt.Sprintf("%d files uploaded!", len(files)),
		})
	})
	router.Run()
}
```

##### 重定向

###### HTTP重定向

```go
r.GET("/test", func(c *gin.Context) {
	c.Redirect(http.StatusMovedPermanently, "http://www.sogo.com/")
})
```

###### 路由重定向

```go
r.GET("/test", func(c *gin.Context) {
    // 指定重定向的URL
    c.Request.URL.Path = "/test2"
    r.HandleContext(c)
})
r.GET("/test2", func(c *gin.Context) {
    c.JSON(http.StatusOK, gin.H{"hello": "world"})
})
```

##### Gin路由

###### 1. 普通路由

- RESTful API

```go
r.GET("/index", func(c *gin.Context) {...})
r.POST("/login", func(c *gin.Context) {...})
r.PUT("/login", func(c *gin.Context) {...})
r.DELETE("/login", func(c *gin.Context) {...})
```

- 匹配所有请求方法的`Any`方法

```go
r.Any("/test", func(c *gin.Context) {...})
```

- 为没有配置处理函数的路由添加处理程序，默认情况下它返回404代码

```go
r.NoRoute(func(c *gin.Context) {
		c.HTML(http.StatusNotFound, "views/404.html", nil)
	})
```

###### 2. 路由组

> 将拥有共同URL前缀的路由划分为一个路由组。习惯性一对`{}`包裹同组的路由，这只是为了看着清晰

```go
func main() {
	r := gin.Default()
	userGroup := r.Group("/user")
	{
		userGroup.GET("/index", func(c *gin.Context) {...})
		userGroup.GET("/login", func(c *gin.Context) {...})
		userGroup.POST("/login", func(c *gin.Context) {...})

	}
	shopGroup := r.Group("/shop")
	{
		shopGroup.GET("/index", func(c *gin.Context) {...})
		shopGroup.GET("/cart", func(c *gin.Context) {...})
		shopGroup.POST("/checkout", func(c *gin.Context) {...})
	}
	r.Run()
}
```

- 路由组嵌套

```go
shopGroup := r.Group("/shop")
	{
		shopGroup.GET("/index", func(c *gin.Context) {...})
		shopGroup.GET("/cart", func(c *gin.Context) {...})
		shopGroup.POST("/checkout", func(c *gin.Context) {...})
		// 嵌套路由组
		xx := shopGroup.Group("xx")
		xx.GET("/oo", func(c *gin.Context) {...})
	}
```

##### Gin中间件

> Gin框架允许开发者在处理请求的过程中，加入用户自己的钩子（Hook）函数。这个钩子函数就叫中间件，中间件适合处理一些公共的业务逻辑，比如登录认证、权限校验、数据分页、记录日志、耗时统计等。

###### 定义中间件

> Gin中的中间件必须是一个`gin.HandlerFunc`类型。

- 记录接口耗时的中间件

  ```go
  // StatCost 是一个统计耗时请求耗时的中间件
  func StatCost() gin.HandlerFunc {
  	return func(c *gin.Context) {
  		start := time.Now()
  		c.Set("name", "小王子") // 可以通过c.Set在请求上下文中设置值，后续的处理函数能够取到该值
  		// 调用该请求的剩余处理程序
  		c.Next()
  		// 不调用该请求的剩余处理程序
  		// c.Abort()
  		// 计算耗时
  		cost := time.Since(start)
  		log.Println(cost)
  	}
  }
  ```

- 跨域中间件cors

  ```go
  package main
  
  import (
    "time"
  
    "github.com/gin-contrib/cors"
    "github.com/gin-gonic/gin"
  )
  
  func main() {
    router := gin.Default()
    // CORS for https://foo.com and https://github.com origins, allowing:
    // - PUT and PATCH methods
    // - Origin header
    // - Credentials share
    // - Preflight requests cached for 12 hours
    router.Use(cors.New(cors.Config{
      AllowOrigins:     []string{"https://foo.com"},  // 允许跨域发来请求的网站
      AllowMethods:     []string{"GET", "POST", "PUT", "DELETE",  "OPTIONS"},  // 允许的请求方法
      AllowHeaders:     []string{"Origin", "Authorization", "Content-Type"},
      ExposeHeaders:    []string{"Content-Length"},
      AllowCredentials: true,
      AllowOriginFunc: func(origin string) bool {  // 自定义过滤源站的方法
        return origin == "https://github.com"
      },
      MaxAge: 12 * time.Hour,
    }))
    router.Run()
  }
  ```

- 使用默认配置，允许所有的跨域请求

  ```go
  func main() {
    router := gin.Default()
    // same as
    // config := cors.DefaultConfig()
    // config.AllowAllOrigins = true
    // router.Use(cors.New(config))
    router.Use(cors.Default())
    router.Run()
  }
  ```

###### 注册中间件

> 可以为每个路由添加任意数量的中间件

- 为全局路由注册

  ```go
  func main() {
  	// 新建一个没有任何默认中间件的路由
  	r := gin.New()
  	// 注册一个全局中间件
  	r.Use(StatCost())
  	
  	r.GET("/test", func(c *gin.Context) {
  		name := c.MustGet("name").(string) // 从上下文取值
  		log.Println(name)
  		c.JSON(http.StatusOK, gin.H{
  			"message": "Hello world!",
  		})
  	})
  	r.Run()
  }
  ```

- 为某个路由单独注册

  ```go
  // 给/test2路由单独注册中间件（可注册多个）
  r.GET("/test2", StatCost(), func(c *gin.Context) {
      name := c.MustGet("name").(string) // 从上下文取值
      log.Println(name)
      c.JSON(http.StatusOK, gin.H{
          "message": "Hello world!",
      })
  })
  ```

- 为路由组注册中间件

  ```go
  // 写法1：
  shopGroup := r.Group("/shop", StatCost())
  {
      shopGroup.GET("/index", func(c *gin.Context) {...})
      ...
  }
  
  // 写法2：
  shopGroup := r.Group("/shop")
  shopGroup.Use(StatCost())
  {
      shopGroup.GET("/index", func(c *gin.Context) {...})
      ...
  }
  ```

##### 运行多个服务

> 可以在多个端口启动服务

```go
package main

import (
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/sync/errgroup"
)

var (
	g errgroup.Group
)

func router01() http.Handler {
	e := gin.New()
	e.Use(gin.Recovery())
	e.GET("/", func(c *gin.Context) {
		c.JSON(
			http.StatusOK,
			gin.H{
				"code":  http.StatusOK,
				"error": "Welcome server 01",
			},
		)
	})

	return e
}

func router02() http.Handler {
	e := gin.New()
	e.Use(gin.Recovery())
	e.GET("/", func(c *gin.Context) {
		c.JSON(
			http.StatusOK,
			gin.H{
				"code":  http.StatusOK,
				"error": "Welcome server 02",
			},
		)
	})

	return e
}

func main() {
	server01 := &http.Server{
		Addr:         ":8080",
		Handler:      router01(),
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	server02 := &http.Server{
		Addr:         ":8081",
		Handler:      router02(),
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}
   // 借助errgroup.Group或者自行开启两个goroutine分别启动两个服务
	g.Go(func() error {
		return server01.ListenAndServe()
	})

	g.Go(func() error {
		return server02.ListenAndServe()
	})

	if err := g.Wait(); err != nil {
		log.Fatal(err)
	}
}
```

##### gin.Context(上下文对象)

> `c *gin.Context` 是 Gin 的核心组件之一，代表当前 HTTP 请求的上下文（Context）
>
> 作用：它贯穿整个请求生命周期，提供了**访问请求数据**、**生成响应**、**管理中间件**等功能。
>
> 生命周期：每个请求都会创建一个新的 `*gin.Context`，请求结束后销毁。







##### jwt模块

```go
import "github.com/golang-jwt/jwt"

// JTW 密钥
var jwtSecret = []byte("boy_next_door")

// 签名一个 JTW
func SignJWT(user types.User) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"name": user.Name,
		"id":   user.Id,
		"exp":  time.Now().Add(time.Hour * 24 * 30).Unix(),
	})
	tokenString, err := token.SignedString([]byte(jwtSecret))
	return tokenString, err
}

// 用户表
type User struct {
	Id       int    `json:"id"`
	Name     string `json:"name"`
	Password string `json:"password"`
}
```

##### 项目部署

###### Dockerfile编写

```dockerfile
FROM golang:alpine AS builder

# 为我们的镜像设置必要的环境变量
ENV GO111MODULE=on \
    GOPROXY=https://goproxy.cn,direct \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# 移动到工作目录：/build
WORKDIR /build

# 将代码复制到容器中
COPY . .

# 下载依赖信息
RUN go mod download

# 将代码复制到容器中
COPY . .

# 将我们的代码编译成二进制可执行文件 bubble
RUN go build -o bubble .

# 接下来创建一个小镜像
FROM debian:stretch-slim

# 从builder镜像中把静态文件拷贝到当前目录
COPY ./templates /templates
COPY ./static /static

# 从builder镜像中把配置文件拷贝到当前目录
COPY ./conf /conf

# 从builder镜像中把/dist/app 拷贝到当前目录
COPY --from=builder /build/bubble /

# 需要运行的命令
ENTRYPOINT ["/bubble", "conf/config.ini"]
```



