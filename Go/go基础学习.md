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

##### 类型的分类

###### 1. 基本类型（Primitive Types）

- **布尔型（Boolean）**
  `bool`：值为 `true` 或 `false`。
- **数值类型（Numeric）**
  - **整数**：
    - 有符号整数：`int8`, `int16`, `int32`（`rune`）, `int64`, `int`（平台相关，32/64位）。
    - 无符号整数：`uint8`（`byte`）, `uint16`, `uint32`, `uint64`, `uint`（平台相关）。
    - 特殊类型：`uintptr`（用于存储指针的整数）。
  - **浮点数**：
    - `float32`（单精度）、`float64`（双精度）。
  - **复数**：
    - `complex64`（`float32` 实部和虚部）、`complex128`（`float64` 实部和虚部）。
- **字符串（String）**
  `string`：不可变的 UTF-8 字符序列。

###### 2. 复合类型（Composite Types）

由基本类型或其他复合类型组合而成：

- **数组（Array）**
  固定长度的元素序列：

  ```go
  var arr [5]int // 包含 5 个 int 的数组
  ```

- **切片（Slice）**
  动态长度的数组视图：

  ```go
  var s []int // 可扩展的切片
  ```

- **结构体（Struct）**
  组合多个字段的自定义类型：

  ```go
  type User struct {
      Name string
      Age  int
  }
  ```

- **映射（Map）**
  键值对的集合：

  ```go
  var m map[string]int // 键为 string，值为 int
  ```

- **指针（Pointer）**
  指向变量的内存地址：

  ```go
  var p *int // 指向 int 的指针
  ```

- **通道（Channel）**
  用于协程（goroutine）间通信：

  ```go
  var ch chan int // 传递 int 的通道
  ```

###### 3. 接口类型（Interface Types）

定义一组方法签名，用于多态：

- **普通接口**：

  ```go
  type Writer interface {
      Write([]byte) (int, error)
  }
  ```

- **空接口（`interface{}`）**：
  可接受任意类型的值：

  ```go
  var any interface{} = 42 // 存储任意类型
  ```

###### 4. 函数类型（Function Types）

表示函数签名，可作为变量或参数传递：

```go
type Adder func(a, b int) int
```

###### 5. 自定义类型（Custom Types）

通过 `type` 关键字定义的新类型：

- **基于现有类型**：

  ```go
  type Celsius float64 // 新类型，基于 float64
  ```

- **类型别名**：

  ```go
  type Alias = int // 别名，与 int 完全等价
  ```

###### 6. 错误类型（Error Type）

内置的 `error` 接口类型，用于错误处理：

```go
type error interface {
    Error() string
}
```

###### 7. 特殊类型

- **`rune`**：`int32` 的别名，表示 Unicode 码点。
- **`byte`**：`uint8` 的别名，表示原始二进制数据。
- **`nil`**：指针、通道、函数、接口、映射或切片的零值。

##### go关键字

> 程序一般由**关键字**、**常量**、**变量**、**运算符**、**类型**和**函数**组成。
>
> 程序中可能会使用到这些分隔符：括号 ()，中括号 [] 和大括号 {}。
>
> 程序中可能会使用到这些标点符号：**.**、**,**、**;**、**:** 和 **…**。

- 25个关键字或保留字

| break        | default         | func       | interface   | select     |
| ------------ | --------------- | ---------- | ----------- | ---------- |
| **case**     | **defer**       | **go**     | **map**     | **struct** |
| **chan**     | **else**        | **goto**   | **package** | **switch** |
| **const**    | **fallthrough** | **if**     | **range**   | **type**   |
| **continue** | **for**         | **import** | **return**  | **var**    |

- 36个预定义标识符

| append    | bool        | byte        | cap         | close      | complex  | complex64 | complex128 | uint16      |
| --------- | ----------- | ----------- | ----------- | ---------- | -------- | --------- | ---------- | ----------- |
| **copy**  | **false**   | **float32** | **float64** | **imag**   | **int**  | **int8**  | **int16**  | **uint32**  |
| **int32** | **int64**   | **iota**    | **len**     | **make**   | **new**  | **nil**   | **panic**  | **uint64**  |
| **print** | **println** | **real**    | **recover** | **string** | **true** | **uint**  | **uint8**  | **uintptr** |

###### type

1. 定义新类型

   > 通过 `type` 可以基于现有类型（如基本类型、结构体、函数签名等）创建新类型。

   ```go
   type 新类型名 基础类型
   ```

   - **类型安全**：新类型与基础类型是 **不同的类型**，不能直接混用。

     ```go
     var a int = 10
     var b MyInt = 20
     // a = b // 错误：类型不匹配
     ```

   - **可扩展性**：可以为新类型定义方法（Go 的**方法接收者**机制）。

     ```go
     func (m MyInt) Double() MyInt {
         return m * 2
     }
     ```

2. 定义结构体

   > `type` 常用于定义结构体类型，用于封装多个字段。

   ```go
   type 结构体名 struct {
       字段1 类型1
       字段2 类型2
       ...
   }
   ```

   - **字段组合**：支持嵌套结构体，**实现组合**而非继承。

   - **方法绑定**：可以为结构体定义方法。

     ```go
     func (p Person) Greet() string {
         return "Hello, " + p.Name
     }
     ```

3. 定义接口

   > `type` 用于定义接口类型，描述方法集合。

   ```go
   type 接口名 interface {
       方法1(参数列表) 返回值列表
       方法2(参数列表) 返回值列表
       ...
   }
   ```

   - **隐式实现**：无需显式声明实现接口，只需实现接口方法即可。
   - **多态性**：接口变量可以存储任何实现了该接口的具体类型值。

 4. 定义函数类型

    > `type` 可以定义函数类型，用于抽象函数签名。

    ```go
    type 函数类型名 func(参数列表) 返回值列表
    ```

    - **高阶函数**：函数类型可以作为参数或返回值。
    - **代码复用**：通过类型抽象实现通用逻辑。

5. 定义类型别名

   > 通过 `type` 可以为现有类型创建别名，**别名与原类型完全等价**。

   ```go
   type 别名 = 基础类型
   ```

   - **类型兼容**：别名与原类型可以互换使用。
   - **代码可读性**：通过别名增强语义。

6. 定义复杂类型

   > `type` 支持定义复杂的组合类型

   - **切片类型**：

     ```go
     type IntSlice []int
     ```

   - **映射类型**：

     ```go
     type StringMap map[string]string
     ```

   - **通道类型**：

     ```go
     type JobChan chan Job
     ```

7. 类型嵌入

   > 通过 `type` 可以实现类型嵌入（组合），用于扩展结构体或接口。

   ```go
   type Person struct {
       Name string
       Age  int
   }
   
   type Employee struct {
       Person  // 嵌入 Person 类型
       Salary float64
   }
   ```

   - **字段提升**：嵌入类型的字段和方法会被提升到外层类型。
   - **代码复用**：通过组合实现类似继承的效果。

8. 类型约束（泛型）

   ```go
   type Number interface {
       int | float64
   }
   
   func Add[T Number](a, b T) T {
       return a + b
   }
   ```

   - **类型安全**：限制泛型类型参数的范围。
   - **灵活性**：支持多种类型的通用逻辑。

###### fallthrough

> 在 Go 语言中，**`fallthrough`** 是一个特殊的控制流关键字，**仅用于 `switch` 语句**。它的作用是强制继续执行下一个 `case` 或 `default` 的代码块，而**不检查下一个 `case` 的条件**。

###### make

> **`make()`** 是一个内建函数，专门用于初始化并分配内存给 **切片（slice）**、**映射（map）** 和 **通道（channel）** 这三种引用类型的数据结构。它的作用是创建这些类型的实例，并设置它们的初始属性（如容量、长度等）

1. 创建切片（Slice）

   ```go
   // 切片是动态数组，需要指定初始长度和容量（可选）。
   
   // 语法
   make([]T, length, capacity)
   
   // 示例
   s1 := make([]int, 5)       // 长度=5，容量=5（默认等于长度）
   s2 := make([]int, 3, 10)   // 长度=3，容量=10
   ```

   - 长度（`length`）：切片当前包含的元素个数。
   - 容量（`capacity`）：底层数组可容纳的元素总数（切片可动态扩展）。

2. 创建映射（Map）

   ```go
   // 映射是键值对集合，需初始化后才能添加键值。
   
   // 语法
   make(map[K]V, initialCapacity)
   
   // 示例
   m1 := make(map[string]int)     // 初始容量未指定（由运行时决定）
   m2 := make(map[string]bool, 10) // 初始容量为10（优化性能，避免扩容）
   ```

   - `initialCapacity` 是可选参数，提示运行时预先分配内存空间（不强制限制大小）

3. 创建通道（Channel）

   ```go
   // 通道用于协程（goroutine）间通信，需指定缓冲区大小（可选）
   
   // 语法
   make(chan T, bufferSize)
   
   // 示例
   ch1 := make(chan int)      // 无缓冲通道（同步通信）
   ch2 := make(chan string, 5) // 有缓冲通道（容量为5，异步通信）
   ```

   - 无缓冲通道：发送和接收操作会阻塞，直到另一方准备好。
   - 有缓冲通道：缓冲区未满时可异步发送，未空时可异步接收。

###### new()

> **`new()`** 是一个内建函数，用于为指定类型分配内存并返回指向该内存的指针。它会将分配的内存初始化为类型的 **零值**，适用于所有数据类型（包括基本类型、结构体、数组等）

```go
ptr := new(T)
```

- **`T`**：任意类型（如 `int`、`struct`、自定义类型等）
- **返回值**：指向新分配的 `T` 类型零值的指针（`*T`）

| **特性**       | **`new()`**                            | **`make()`**                         |
| :------------- | :------------------------------------- | :----------------------------------- |
| **适用类型**   | 所有类型（如 `int`、`struct`、指针等） | 仅限 `slice`、`map`、`channel`       |
| **返回值**     | 指向类型零值的指针（`*T`）             | 初始化后的类型实例（非指针）         |
| **内存初始化** | 仅分配内存并清零                       | 分配内存并初始化数据结构（如哈希表） |

1. 基本类型

   ```go
   // 分配一个 int 类型的零值，返回指针
   numPtr := new(int)
   fmt.Println(*numPtr) // 输出: 0
   
   // 修改指针指向的值
   *numPtr = 42
   fmt.Println(*numPtr) // 输出: 42
   ```

2. 结构体

   ```go
   type Person struct {
       Name string
       Age  int
   }
   
   // 分配并初始化 Person 结构体的零值
   p := new(Person)
   fmt.Println(p) // 输出: &{"" 0}
   
   // 修改字段
   p.Name = "Alice"
   p.Age = 30
   fmt.Println(p) // 输出: &{Alice 30}
   ```

3. 数组

   ```go
   // 分配长度为 3 的 int 数组，初始化为零值
   arrPtr := new([3]int)
   fmt.Println(*arrPtr) // 输出: [0 0 0]
   
   // 修改元素
   (*arrPtr)[1] = 10
   fmt.Println(*arrPtr) // 输出: [0 10 0]
   ```

4. 适用场景

   - **需要显式指针时**
     当函数需返回一个指向新对象的指针时：

     ```go
     func NewPerson() *Person {
         return new(Person)
     }
     ```

   - **避免结构体复制**
     传递大结构体时使用指针减少内存拷贝：

     ```go
     type LargeStruct struct { /* 大量字段 */ }
     obj := new(LargeStruct)
     process(obj) // 传递指针而非值
     ```

   - **接口实现**
     当类型需要实现某个接口，且需通过指针接收者定义方法时：

     ```go
     type Writer interface { Write([]byte) }
     type MyWriter struct{}
     
     func (w *MyWriter) Write(data []byte) { /* ... */ }
     
     func main() {
         var w Writer = new(MyWriter) // 必须用指针
     }
     ```

###### range

**基本语法**

```go
for index, value := range collection {
    // 循环体
}
```

- **`index`**：当前元素的索引（数组、切片、字符串）或键（map）。
- **`value`**：当前元素的值（或 map 的值）。
- **`collection`**：被迭代的集合（数组、切片、字符串、map、通道）。

**1. 数组/切片**

- **返回索引和元素值**。

  ```go
  nums := []int{10, 20, 30}
  for i, num := range nums {
      fmt.Printf("索引: %d, 值: %d\n", i, num)
  }
  
  索引: 0, 值: 10
  索引: 1, 值: 20
  索引: 2, 值: 30
  ```

**2. 字符串**

- **返回字符的字节索引和 Unicode 码点（rune）**。

- 处理多字节字符（如 UTF-8）时，索引可能不连续。

  ```go
  s := "Go语言"
  for i, r := range s {
      fmt.Printf("字节索引: %d, Unicode码点: %U, 字符: %c\n", i, r, r)
  }
  
  字节索引: 0, Unicode码点: U+0047, 字符: G
  字节索引: 1, Unicode码点: U+006F, 字符: o
  字节索引: 2, Unicode码点: U+8BED, 字符: 语
  字节索引: 5, Unicode码点: U+8A00, 字符: 言
  ```

**3. 映射（map）**

- **返回键和值**。

- **遍历顺序随机**（Go 故意随机化 map 的遍历顺序）。

  ```go
  m := map[string]int{"a": 1, "b": 2}
  for k, v := range m {
      fmt.Printf("键: %s, 值: %d\n", k, v)
  }
  
  键: a, 值: 1
  键: b, 值: 2
  ```

**4. 通道（channel）**

- **仅返回值**，持续接收数据直到通道关闭。

  ```go
  ch := make(chan int, 3)
  ch <- 1
  ch <- 2
  close(ch) // 必须关闭通道，否则 range 会阻塞
  for v := range ch {
      fmt.Println(v)
  }
  
  1
  2
  ```

**关键特性与注意事项**

**1. 值拷贝**

- `range` 迭代时返回的是元素的 **副本**，而非原始元素的引用。

- **修改副本不影响原数据**：

  ```go
  nums := []int{1, 2, 3}
  for _, num := range nums {
      num *= 2 // 仅修改副本
  }
  fmt.Println(nums) // 输出: [1 2 3]
  ```

- **若需修改原数据，需通过索引**：

  ```go
  for i := range nums {
      nums[i] *= 2
  }
  fmt.Println(nums) // 输出: [2 4 6]
  ```

**2. 忽略返回值**

- 使用 `_` 忽略不需要的值：

  ```go
  // 仅获取索引
  for i := range nums { /* ... */ }
  
  // 仅获取值（切片/数组）
  for _, num := range nums { /* ... */ }
  
  // 仅获取键（map）
  for k := range m { /* ... */ }
  ```

**3. 性能优化**

- **切片遍历时，直接使用索引访问可能更快**（避免值拷贝）：

  ```go
  for i := 0; i < len(nums); i++ {
      // 直接访问 nums[i]
  }
  ```

- **大结构体切片建议使用索引**，减少拷贝开销。

**4. 循环变量重用**

- `range` 的循环变量在每次迭代中会被 **重用**（内存地址相同）。

- **闭包陷阱**：在异步操作（如 goroutine）中直接使用循环变量可能导致意外结果。

  ```go
  for _, num := range []int{1, 2, 3} {
      go func() {
          fmt.Println(num) // 可能输出 3, 3, 3
      }()
  }
  ```

- **修复方法**：传递参数或创建局部变量副本。

  ```go
  for _, num := range nums {
      n := num // 创建副本
      go func() {
          fmt.Println(n) // 正确输出 1, 2, 3
      }()
  }
  ```

**5. 遍历时修改集合**

- **数组/切片**：可安全修改元素值，但修改长度（如追加元素）不会影响迭代次数。

  ```go
  nums := []int{1, 2, 3}
  for i := range nums {
      nums[i] *= 2     // 安全
      nums = append(nums, i) // 不影响当前循环次数
  }
  ```

- **map**：遍历时修改键值可能导致不可预测行为，需避免。

**`range` 的底层实现**

- **数组/切片**：通过索引逐步访问，时间复杂度 O(n)。
- **字符串**：按 UTF-8 解码遍历 rune。
- **map**：随机选择一个桶开始遍历，每次迭代顺序不同。
- **通道**：持续调用 `<-ch` 直到通道关闭。

###### append



###### cap

>  获取 **切片（slice）**、**数组（array）** 或 **通道（channel）** 的 **容量**。

```go
s := make([]int, 3, 5) // 切片长度3，容量5
fmt.Println(cap(s))    // 输出: 5

ch := make(chan int, 10)
fmt.Println(cap(ch))   // 输出: 10（通道缓冲区容量）
```

###### close

>  关闭 **通道（channel）**，表示不再向通道发送数据。

- 关闭后的通道无法再发送数据（发送会 panic）。
- 接收操作可以继续读取剩余数据，直到通道为空。

```go
ch := make(chan int)
go func() {
    ch <- 1
    close(ch) // 关闭通道
}()
for v := range ch { // 循环会自动退出
    fmt.Println(v)
}
```

###### imag

> 获取 **复数（complex number）** 的虚部。

```go
c := complex(3, 4) // 3 + 4i
fmt.Println(imag(c)) // 输出: 4
```

###### iota

- 每遇到一个 `const` 关键字，`iota` 重置为 0。
- 每声明一行常量，`iota` 自动递增 1。

```go
const (
    A = iota // 0
    B        // 1
    C        // 2
)
const (
    D = iota << 1 // 0 << 1 = 0
    E             // 1 << 1 = 2
)
```

###### panic

> 触发 **运行时恐慌（panic）**，终止当前函数的执行，并逐层向上触发 `defer`

- 若未通过 `recover` 捕获，程序会崩溃并打印堆栈信息。

```go
func risky() {
    panic("发生严重错误！")
}
```

###### real

> 获取 **复数（complex number）** 的实部。

```go
c := complex(3, 4) // 3 + 4i
fmt.Println(real(c)) // 输出: 3
```

###### recover

> 捕获 **panic** 并恢复程序执行，只能在 `defer` 函数中使用。

```go
func safeCall() {
    defer func() {
        if err := recover(); err != nil {
            fmt.Println("捕获到 panic:", err)
        }
    }()
    panic("手动触发 panic")
}
```

###### uintptr

> 一种无符号整数类型，用于存储指针的位模式（内存地址）。

- 与 `unsafe` 包配合，进行底层指针操作。
- 通常用于与 C 语言交互或系统级编程。

```go
var x int = 42
ptr := uintptr(unsafe.Pointer(&x)) // 将指针转换为 uintptr
```



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

##### 类型转换

> 在 Go 语言中，**类型转换（Type Conversion）** 是将一个类型的值显式转换为另一个类型的操作。
>
> Go 是**静态类型语言**，对类型安全要求严格，因此类型转换需要显式进行（不支持隐式自动转换）。

###### 一、基本类型转换

1. 数值类型转换

   > 数值类型（如 `int`、`float`、`uint`）之间可以相互转换，但可能丢失精度或溢出。

   ```go
   var a int = 42
   var b float64 = float64(a)  // int → float64
   var c uint = uint(b)        // float64 → uint
   
   // 注意：高精度转低精度可能丢失数据
   var x float64 = 3.14
   var y int = int(x)          // y = 3（小数部分截断）
   ```

2. 字符串 ↔ 字节切片（`[]byte`）

   > 字符串可转换为字节切片（底层共享数据，但类型不同）

   ```go
   s := "hello"
   bytes := []byte(s)     // string → []byte
   s2 := string(bytes)    // []byte → string
   ```

3. 字符串 ↔ 符文切片（`[]rune`）

   > 字符串可转换为 Unicode 符文切片（每个 `rune` 对应一个 Unicode 码点）

   ```go
   s := "你好"
   runes := []rune(s)     // string → []rune
   s2 := string(runes)    // []rune → string
   ```

###### 二、自定义类型转换

1. 类型别名（Type Alias）

   > 类型别名与原类型可直接转换

   ```go
   type MyInt = int       // MyInt 是 int 的别名
   var a int = 10
   var b MyInt = a        // 无需显式转换
   ```

2. 新类型（Type Definition）

   > 新定义的类型（即使底层类型相同）需显式转换

   ```go
   type Celsius float64    // 新类型
   type Fahrenheit float64 // 新类型
   
   var c Celsius = 100.0
   var f Fahrenheit = Fahrenheit(c) // 必须显式转换
   ```

###### 三、接口类型转换

1. 接口 ↔ 具体类型

   > 使用 **类型断言（Type Assertion）** 将接口转换为具体类型

   ```go
   var i interface{} = "hello"
   s := i.(string)        // 类型断言，若失败会 panic
   s, ok := i.(string)    // 安全类型断言，ok 为检测标志
   ```

2. 类型断言（Type Assertion）

   ```go
   var val interface{} = 42
   
   // 安全断言
   if num, ok := val.(int); ok {
       fmt.Println(num * 2) // 输出 84
   } else {
       fmt.Println("不是整数")
   }
   ```

###### 四、特殊类型转换

1. 指针类型转换

   > 需使用 `unsafe` 包（一般不推荐）

   ```go
   var a int64 = 42
   var p *int64 = &a
   var p2 *int32 = (*int32)(unsafe.Pointer(p)) // 危险操作！
   ```

2. 结构体强制转换

   > 仅当两个结构体 **内存布局完全一致** 时，可通过强制指针转换实现

   ```go
   type A struct { X int }
   type B struct { X int }
   
   a := A{X: 42}
   b := *(*B)(unsafe.Pointer(&a)) // b.X = 42
   ```

###### 五、类型转换的注意事项

1. **不支持隐式转换**
   - Go 严格禁止隐式类型转换，必须显式操作。

2. **类型兼容性**
   - 只有底层类型兼容的类型才能转换，否则需通过其他方式（如序列化）。

3. **性能开销**
   - 类型转换可能涉及内存拷贝（如 `string` ↔ `[]byte`），需注意性能。

4. **数据丢失风险**
   - 数值类型转换可能导致溢出或精度丢失

###### 六、实际应用场景

1. 数值计算

   ```go
   func Calculate(a int, b float64) float64 {
       return float64(a) + b // 需统一类型
   }
   ```

2. 处理二进制数据

   ```go
   data := []byte{0x48, 0x65, 0x6C, 0x6C, 0x6F}
   text := string(data) // "Hello"
   ```

3. JSON 序列化（**json.Unmarshal()**）

   ```go
   type User struct {
       Name string `json:"name"`
       Age  int    `json:"age"`
   }
   
   jsonData := []byte(`{"name":"Alice","age":30}`)
   var user User
   json.Unmarshal(jsonData, &user) // []byte → 结构体
   ```

4. 接口解包

   ```go
   func process(val interface{}) {
       if s, ok := val.(string); ok {
           fmt.Println("字符串:", s)
       } else if i, ok := val.(int); ok {
           fmt.Println("整数:", i)
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

###### 2. 数值类型

- 整型：int
  - uint8、int8
  
    > byte是uint8的别名
  
  - uint16、int16
  
  - uint32、int32
  
    > rune是int32的别名，用来表示Unicode码点。
  
  - uint64、int64
  
- 浮点型：float32、float64、complex64、complex128

###### 3. 字符串类型

> 字符串就是一串固定长度的字符连接起来的字符序列。Go 的字符串是由单个字节连接起来的。Go 语言的字符串的字节使用 UTF-8 编码标识 Unicode 文本。

###### 4. 派生类型

1. 指针类型（Pointer）

   > 指向变量的内存地址

2. 数组类型

   > 数组是固定长度的元素序列，比如[5]int

3. 结构化类型（struct）

4. Channel 类型

   > 用于goroutine之间的通信

5. 函数类型（fun）

6. 切片类型（slice）

   > 是基于数组的动态视图，更灵活

7. 接口类型（interface）

   > 定义了一组方法签名

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

###### 结构体标签

> 通过 **键值对（Key-Value）** 的形式为字段附加元数据（Metadata），供不同的框架或工具解析和使用。

1. `json:"age"`

- **作用**：
  控制 JSON 序列化（`json.Marshal`）和反序列化（`json.Unmarshal`）时的字段名称和行为。
- **规则**：
  - `"age"`：JSON 字段名称为 `"age"`（默认使用结构体字段名的蛇形命名，如 `Age` → `age`）。
  - 忽略字段：`json:"-"`（不参与序列化）。
  - 忽略空值：`json:"age,omitempty"`（字段为零值时，JSON 中不显示该字段）。

2. `binding:"required"`

- **作用**：
  用于 **Gin 框架** 的参数绑定和验证，表示该字段为必填项。
- **规则**：
  - `"required"`：字段必须存在且非零值（如 `string` 不能为空字符串，`int` 不能为 `0`）。
  - 其他验证规则：如 `min=1`、`max=100`、`email` 等（需结合 Gin 的验证器使用）。

3. `label:"年龄"`

- **作用**：
  通常用于定义字段的友好名称（如表单显示、错误提示）。
  **注意**：`label` 标签不是 Go 标准库或 Gin 内置的标签，需要开发者自行解析（或通过第三方库实现）。

4. `gorm`（数据库 ORM）
   
   - 用于定义数据库表的字段约束（需配合 GORM 框架）
   
5. `form`（表单绑定）
   
   - 用于 Gin 框架的表单参数绑定（即URL中?后面所带的参数）
   
6. `xml`（XML 编码）
   
   - 控制 XML 序列化/反序列化的字段名称
   
7. `yaml`（YAML 编码）

   - 控制 YAML 序列化/反序列化的字段名称

   ```go
   type Config struct {
       Port int `yaml:"port" default:"8080"`
   }
   ```

8. `bson`（MongoDB 驱动）

9. `validate`（通用验证）
   
   - 通用参数验证（需配合验证库如 `go-playground/validator`）
   
10. `db`（SQL 数据库驱动）
    
    - 用于 SQL 查询的字段映射（如 `sqlx` 或 `gorm`）
    
11. `mapstructure`（配置解析）

    - 用于将 `map` 数据解码到结构体（如 Viper 配置管理）

    ```go
    type ServerConfig struct {
        Port int `mapstructure:"server_port"`
    }
    ```

###### 标签语法规则

1. **格式**：

   键值对用空格分隔，多个键值对可以共存：

   ```go
   Field Type `key1:"value1" key2:"value2"`
   ```

2. **键名约定**：

   标签的键名（如 `json`、`gorm`）由框架或工具定义，需遵循其文档规则。

3. **值格式**：

   值可以是单个字符串或多个逗号分隔的参数：

   ```go
   Field string `json:"name,omitempty" validate:"required,email"`
   ```

4. **自定义标签**：

   开发者可以通过反射（`reflect` 包）解析自定义标签：

   ```go
   field := reflect.TypeOf(obj).Field(0)
   label := field.Tag.Get("label") // 获取 label 标签的值
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
type 接口名 interface {
    方法1(参数列表) 返回值列表
    方法2(参数列表) 返回值列表
    // ...
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

##### 接口和结构体的区别

> 结构体通过实现接口的方法，满足接口的约束。
>
> 接口变量可以持有结构体实例，实现多态调用。
>
> **接口管行为，结构体管数据**

###### 一、接口（Interface）的核心

1. 接口是什么？

   - **接口是一组方法的集合**，只定义方法的签名（名称、参数、返回值），不包含具体实现。

   - **目的**：约束类型必须实现某些方法，实现多态性和解耦。

2. 接口的示例

   ```go
   package main
   
   import "fmt"
   
   // 定义一个 "说话" 接口
   type Speaker interface {
   	Speak() string // 方法签名
   }
   
   type Dog struct{}
   
   // Dog 实现 Speaker 接口
   func (d Dog) Speak() string {
   	return "汪汪！"
   }
   
   type Cat struct{}
   
   // Cat 实现 Speaker 接口
   func (c Cat) Speak() string {
   	return "喵喵！"
   }
   
   // 使用接口类型接收不同结构体
   func MakeSound(s Speaker) {
   	fmt.Println(s.Speak())
   }
   
   func main() {
   	dog := Dog{}
   	cat := Cat{}
   	MakeSound(dog) // 输出: 汪汪！
   	MakeSound(cat) // 输出: 喵喵！
   }
   ```

###### 二、结构体（Struct）的核心作用

1. 结构体是什么？

   - **结构体是数据的集合**，可以包含多个不同类型的字段。

   - **目的**：存储具体的数据，定义数据结构。

2. 结构体的示例

###### 三、接口与结构体的关键区别

| **特性**     | **接口（Interface）**          | **结构体（Struct）**              |
| :----------- | :----------------------------- | :-------------------------------- |
| **本质**     | 定义方法签名（行为规范）       | 定义数据结构（字段集合）          |
| **实现方式** | 隐式实现（无需显式声明）       | 显式定义字段和方法                |
| **实例化**   | 不能直接实例化，需赋值具体类型 | 可以直接实例化（`p := Person{}`） |
| **零值**     | `nil`（未赋值时）              | 各字段的零值（如 `""`、`0`）      |
| **多态性**   | 支持（同一接口不同实现）       | 不支持                            |
| **主要用途** | 解耦、多态、定义行为           | 存储数据、封装状态                |

###### 四、接口的实际应用场景

1. 多态处理

   不同结构体实现同一接口，统一调用：

   ```go
   type Payment interface {
       Pay(amount float64) error
   }
   
   type CreditCard struct{}
   func (c CreditCard) Pay(amount float64) error { /* 信用卡支付逻辑 */ }
   
   type Alipay struct{}
   func (a Alipay) Pay(amount float64) error { /* 支付宝支付逻辑 */ }
   
   // 统一处理支付
   func ProcessPayment(p Payment, amount float64) {
       p.Pay(amount)
   }
   ```

2. 依赖注入

   通过接口解耦模块依赖：

   ```go
   type Logger interface {
       Log(message string)
   }
   
   type Service struct {
       logger Logger // 依赖接口
   }
   
   func (s *Service) DoWork() {
       s.logger.Log("工作开始")
   }
   
   // 使用不同日志实现
   type FileLogger struct{}
   func (f FileLogger) Log(message string) { /* 写入文件 */ }
   
   type ConsoleLogger struct{}
   func (c ConsoleLogger) Log(message string) { /* 打印到控制台 */ }
   ```

五、结构体的实际应用场景

1. 定义数据模型

   ```go
   type User struct {
       ID       int
       Username string
       Email    string
   }
   ```

2. 封装方法

   ```go
   func (u *User) UpdateEmail(newEmail string) {
       u.Email = newEmail
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
>
> c.ShouldBindQuery()

```go
func main() {
	//Default返回一个默认的路由引擎
	r := gin.Default()
	r.POST("/user/search", func(c *gin.Context) {
        // 使用c.ShouldBindQuery()
        var cr BannerListRequest
		c.ShouldBindQuery(&cr)
        
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

###### 4. 获取path参数(c.Param())

> 请求的参数通过URL路径传递
>

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

###### 5. 参数绑定(c.ShouldBind(&login))

> 基于请求的`Content-Type`识别请求数据类型并利用反射机制自动提取请求中`QueryString`、`form表单`、`JSON`、`XML`等参数到结构体中
>

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

###### 6. url参数绑定(c.ShouldBindUri())

```go
r.GET("logs/:id", app.LogReadView)

type IDRequest struct {
	ID uint `json:"id" form:"id" uri:"id"`
}

func LogReadView(c *gin.Context) {
	var cr models.IDRequest
    // 绑定id
	err := c.ShouldBindUri(&cr)
	if err != nil {
		res.FailWithError(err, c)
		return
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



