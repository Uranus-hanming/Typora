[toc]

##### 项目目录结构

```
- conf	环境变量配置文件
	- config.ini
- controller	核心业务逻辑层
- dao	数据库引擎配置文件
	- mysql.go	mysql数据库配置
- models	数据库表配置，其中每个go文件包含一张表，以及和该表相关的增删改查操作
- routers	路由配置
	- routers.go
- setting	项目配置
	- setting.go
- static	前端静态文件
	- css
	- fonts
	- js
- templates  模板
	- favicon.ico
	- index.html
main.go		项目主入口
go.mod		项目依赖管理
	- go.sum
READER.md	项目说明文件

项目部署：
Dockerfile
docker-compose.yml
```

##### 项目依赖包

```
gin框架：
	"github.com/gin-gonic/gin"
mysql数据库：
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
主要的内置包：
	"fmt"
	"os"
```

##### 日志管理配置

- main.go

  ```go
  package main
  
  import (
  	"blogx_server/core"
  	"blogx_server/flags"
  	"blogx_server/global"
  )
  
  func main() {
  	flags.Parse()
  	global.Config = core.ReadConf()
  	core.InitLogrus()
      // 四种模式：
      logrus.Warnf("xxx")
      logrus.Debug("yyy")
      logrus.Error("zzz")
      logrus.Infof("1123")
  }
  ```

- core/init_logrus.go

  ```go
  // core/init_logrus.go
  package core
  
  import (
  	// "blogx_server/global"
  	"bytes"
  	"fmt"
  	"github.com/sirupsen/logrus"
  	"os"
  	"path"
  	"time"
  )
  
  // 颜色
  const (
  	red    = 31
  	yellow = 33
  	blue   = 36
  	gray   = 37
  )
  
  type LogFormatter struct{}
  
  // Format 实现Formatter(entry *logrus.Entry) ([]byte, error)接口
  func (t *LogFormatter) Format(entry *logrus.Entry) ([]byte, error) {
  	//根据不同的level去展示颜色
  	var levelColor int
  	switch entry.Level {
  	case logrus.DebugLevel, logrus.TraceLevel:
  		levelColor = gray
  	case logrus.WarnLevel:
  		levelColor = yellow
  	case logrus.ErrorLevel, logrus.FatalLevel, logrus.PanicLevel:
  		levelColor = red
  	default:
  		levelColor = blue
  	}
  	var b *bytes.Buffer
  	if entry.Buffer != nil {
  		b = entry.Buffer
  	} else {
  		b = &bytes.Buffer{}
  	}
  	//自定义日期格式
  	timestamp := entry.Time.Format("2006-01-02 15:04:05")
  	if entry.HasCaller() {
  		//自定义文件路径
  		funcVal := entry.Caller.Function
  		fileVal := fmt.Sprintf("%s:%d", path.Base(entry.Caller.File), entry.Caller.Line)
  		//自定义输出格式
  		fmt.Fprintf(b, "[%s] \x1b[%dm[%s]\x1b[0m %s %s %s\n", timestamp, levelColor, entry.Level, fileVal, funcVal, entry.Message)
  	} else {
  		fmt.Fprintf(b, "[%s] \x1b[%dm[%s]\x1b[0m %s\n", timestamp, levelColor, entry.Level, entry.Message)
  	}
  	return b.Bytes(), nil
  }
  
  type FileDateHook struct {
  	file     *os.File
  	logPath  string
  	fileDate string //判断日期切换目录
  	appName  string
  }
  
  func (hook FileDateHook) Levels() []logrus.Level {
  	return logrus.AllLevels
  }
  func (hook FileDateHook) Fire(entry *logrus.Entry) error {
  	timer := entry.Time.Format("2006-01-02")
  	line, _ := entry.String()
  	if hook.fileDate == timer {
  		hook.file.Write([]byte(line))
  		return nil
  	}
  	// 时间不等
  	hook.file.Close()
  	os.MkdirAll(fmt.Sprintf("%s/%s", hook.logPath, timer), os.ModePerm)
  	filename := fmt.Sprintf("%s/%s/%s.log", hook.logPath, timer, hook.appName)
  
  	hook.file, _ = os.OpenFile(filename, os.O_WRONLY|os.O_APPEND|os.O_CREATE, 0600)
  	hook.fileDate = timer
  	hook.file.Write([]byte(line))
  	return nil
  }
  func InitFile(logPath, appName string) {
  	fileDate := time.Now().Format("2006-01-02")
  	//创建目录
  	err := os.MkdirAll(fmt.Sprintf("%s/%s", logPath, fileDate), os.ModePerm)
  	if err != nil {
  		logrus.Error(err)
  		return
  	}
  
  	filename := fmt.Sprintf("%s/%s/%s.log", logPath, fileDate, appName)
  	file, err := os.OpenFile(filename, os.O_WRONLY|os.O_APPEND|os.O_CREATE, 0600)
  	if err != nil {
  		logrus.Error(err)
  		return
  	}
  	fileHook := FileDateHook{file, logPath, fileDate, appName}
  	logrus.AddHook(&fileHook)
  }
  
  func InitLogrus() {
  	logrus.SetOutput(os.Stdout)          //设置输出类型
  	logrus.SetReportCaller(true)         //开启返回函数名和行号
  	logrus.SetFormatter(&LogFormatter{}) //设置自己定义的Formatter
  	logrus.SetLevel(logrus.DebugLevel)   //设置最低的Level
  	// l := global.Config.Log
  	// InitFile(l.Dir, l.App)
      InitFile("logs", "blogx_server")
  }
  ```

##### 数据库配置

###### mysql连接配置

- main.go

  ```go
  package main
  
  import (
  	"blogx_server/core"
  	"blogx_server/global"
  )
  
  func main() {
  	global.DB = core.InitDB()
  }
  ```
  
- conf/conf_db.go

  ```go
  package conf
  
  import "fmt"
  
  type DB struct {
  	User     string `yaml:"user"`
  	Password string `yaml:"password"`
  	Host     string `yaml:"host"`
  	Port     int    `yaml:"port"`
  	DB       string `yaml:"db"`
  	Debug    bool   `yaml:"debug"`  // 打印全部的日志
  	Source   string `yaml:"source"` // 数据库的源 mysql pgsql
  }
  
  func (d DB) DSN() string {
  	return fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
  		d.User, d.Password, d.Host, d.Port, d.DB)
  }
  ```

- global/enter.go

  ```go
  package global
  
  import (
  	// "blogx_server/conf"
  	"gorm.io/gorm"
  )
  
  var (
  	// Config *conf.Config
  	DB     *gorm.DB
      DB1     *gorm.DB
  )
  ```
  
- core/init_db.go

  ```go
  package core
  
  import (
  	"blogx_server/global"
  	"github.com/sirupsen/logrus"
  	"gorm.io/driver/mysql"
  	"gorm.io/gorm"
      "gorm.io/plugin/dbresolver"  // 配置数据库读写分离中间件
  	"time"
  )
  
  func InitDB() (db *gorm.DB) {
  
  	dc := global.Config.DB  // 主库为写库，读取settings.yaml配置文件
      dc1 := global.Config.DB1 // 从库为读库
  
  	db, err := gorm.Open(mysql.Open(dc.DSN()), &gorm.Config{
  		DisableForeignKeyConstraintWhenMigrating: true, // 不生成外键约束
  	})
  	if err != nil {
  		logrus.Fatalf("数据库连接失败 %s", err)
  	}
  	sqlDB, err := db.DB()
  	sqlDB.SetMaxIdleConns(10)
  	sqlDB.SetMaxOpenConns(100)
  	sqlDB.SetConnMaxLifetime(time.Hour)
  	logrus.Infof("数据库连接成功！")
      
      if !dc1.Empty() {
  		// 读写库不为空，就注册读写分离的配置
  		err = db.Use(dbresolver.Register(dbresolver.Config{
  			Sources:  []gorm.Dialector{mysql.Open(dc.DSN())}, // 写
  			Replicas: []gorm.Dialector{mysql.Open(dc1.DSN())},  // 读
  			Policy:   dbresolver.RandomPolicy{},
  		}))
  		if err != nil {
  			logrus.Fatalf("读写配置错误 %s", err)
  		}
  	}
      
  	return
  }
  ```

###### 从库连接池配置

```go
package main

import (
	"fmt"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/plugin/dbresolver"
)

func main() {
	// 主库配置
	masterDSN := "root:123456@tcp(127.0.0.1:3306)/blogx?charset=utf8mb4&parseTime=True&loc=Local"

	// 从库配置
	replicas := []string{
		"root:123456@tcp(127.0.0.1:3306)/blogx?charset=utf8mb4&parseTime=True&loc=Local",
		"root:123456@tcp(127.0.0.1:3306)/blogx?charset=utf8mb4&parseTime=True&loc=Local",
	}
	// 主库连接（写操作）
	masterDB, err := gorm.Open(mysql.Open(masterDSN), &gorm.Config{})
	if err != nil {
		fmt.Println(err)
	}
	// 从库连接池（读操作）
	replicaDBs := make([]gorm.Dialector, len(replicas))
	for i, replica := range replicas {
		replicaDBs[i] = mysql.Open(replica)
	}

	// 配置读写分离策略
	masterDB.Use(dbresolver.Register(dbresolver.Config{
		Sources:  []gorm.Dialector{mysql.Open(masterDSN)}, // 写操作主库
		Replicas: replicaDBs,                              // 读操作从库
		Policy:   dbresolver.RandomPolicy{},               // 随机选择从库
	}))

}
```

###### 模型定义

> 模型是使用**普通结构体**定义的。 这些结构体可以包含具有基本**Go类型**、**指针**或这些类型的**别名**，甚至是**自定义类型**（只需要实现 `database/sql` 包中的[Scanner](https://pkg.go.dev/database/sql/?tab=doc#Scanner)和[Valuer](https://pkg.go.dev/database/sql/driver#Valuer)接口）。
>
> 通过 **serializer 标签**支持序列化也很重要。 此功能增强了数据存储和检索的灵活性，特别是对于需要自定义序列化逻辑的字段。

```go
type User struct {
	ID           uint           // GORM 使用一个名为ID 的字段作为每个模型的默认主键。
	Name         string         // A regular string field
	Email        *string        // 指向 *string 和 *time.Time 类型的指针表示可空字段。
	Age          uint8          // 具体数字类型如 uint、string和 uint8 直接使用。
	Birthday     *time.Time     // A pointer to time.Time, can be null
	MemberNumber sql.NullString // 来自 database/sql 包的 sql.NullString 和 sql.NullTime 用于具有更多控制的可空字段。
	ActivatedAt  sql.NullTime   // Uses sql.NullTime for nullable time fields
	CreatedAt    time.Time      // CreatedAt 和 UpdatedAt 是特殊字段，当记录被创建或更新时，GORM 会自动向内填充当前时间。
	UpdatedAt    time.Time      // Automatically managed by GORM for update time
	ignored      string         // fields that aren't exported are ignored
}

// 创建/更新时间追踪（纳秒、毫秒、秒、Time）
type User struct {
  CreatedAt time.Time // 在创建时，如果该字段值为零值，则使用当前时间填充
  UpdatedAt int       // 在创建时该字段值为零值或者在更新时，使用当前时间戳秒数填充
  Updated   int64 `gorm:"autoUpdateTime:nano"` // 使用时间戳纳秒数填充更新时间
  Updated   int64 `gorm:"autoUpdateTime:milli"` // 使用时间戳毫秒数填充更新时间
  Created   int64 `gorm:"autoCreateTime"`      // 使用时间戳秒数填充创建时间
}

// 关联表UserModel，使用关联标签foreignKey
type UserConfModel struct {
	UserID             uint       `gorm:"unique" json:"userID"`
	UserModel          UserModel  `gorm:"foreignKey:UserID" json:"-"`
	LikeTags           []string   `gorm:"type:longtext;serializer:json" json:"likeTags"`
}
```

1. **约定**

   1. **主键**：GORM 使用一个名为`ID` 的字段作为每个模型的默认主键。
   2. **表名**：默认情况下，GORM 将结构体名称转换为 `snake_case` 并为表名加上复数形式。 例如，一个 `User` 结构体在数据库中的表名变为 `users` 。
   3. **列名**：GORM 自动将结构体字段名称转换为 `snake_case` 作为数据库中的列名。
   4. **时间戳字段**：GORM使用字段 `CreatedAt` 和 `UpdatedAt` 来自动跟踪记录的创建和更新时间。

2. **字段级权限控制**

   > 可导出的字段在使用 GORM 进行 CRUD 时拥有全部的权限，此外，GORM 允许您用标签控制字段级别的权限。这样您就可以让一个字段的权限是只读、只写、只创建、只更新或者被忽略
   >
   > 使用 GORM Migrator 创建表时，不会创建被忽略的字段

   ```go
   type User struct {
     Name string `gorm:"<-:create"` // 允许读和创建
     Name string `gorm:"<-:update"` // 允许读和更新
     Name string `gorm:"<-"`        // 允许读和写（创建和更新）
     Name string `gorm:"<-:false"`  // 允许读，禁止写
     Name string `gorm:"->"`        // 只读（除非有自定义配置，否则禁止写）
     Name string `gorm:"->;<-:create"` // 允许读和写
     Name string `gorm:"->:false;<-:create"` // 仅创建（禁止从 db 读）
     Name string `gorm:"-"`  // 通过 struct 读写会忽略该字段
     Name string `gorm:"-:all"`        // 通过 struct 读写、迁移会忽略该字段
     Name string `gorm:"-:migration"`  // 通过 struct 迁移会忽略该字段
   }
   ```

3. **嵌入结构体**

   - 对于匿名字段，GORM 会将其字段包含在父结构体中
   - 对于正常的结构体字段，可以通过标签 `embedded` 将其嵌入
   - 可以使用标签 `embeddedPrefix` 来为 db 中的字段名添加前缀

   ```go
   type Author struct {
     Name  string
     Email string
   }
   
   type Blog struct {
     ID      int
     Author  Author `gorm:"embedded;embeddedPrefix:author_"`
     Upvotes int32
   }
   
   // 等效于
   type Blog struct {
     ID          int64
     AuthorName string
     AuthorEmail string
     Upvotes     int32
   }
   ```

4. **字段标签**

   | 标签名                 | 说明                                                         |
   | :--------------------- | :----------------------------------------------------------- |
   | column                 | 指定 db 列名                                                 |
   | type                   | 列数据类型，推荐使用兼容性好的通用类型，例如：所有数据库都支持 bool、int、uint、float、string、time、bytes 、longtext并且可以和其他标签一起使用，例如：`not null`、`size`, `autoIncrement`… 像 `varbinary(8)` 这样指定数据库数据类型也是支持的。在使用指定数据库数据类型时，它需要是完整的数据库数据类型，如：`MEDIUMINT UNSIGNED not NULL AUTO_INCREMENT` |
   | serializer             | 指定将数据序列化或反序列化到数据库中的序列化器, 例如: `serializer:json/gob/unixtime` |
   | size                   | 定义列数据类型的大小或长度，例如 `size: 256`                 |
   | primaryKey             | 将列定义为主键                                               |
   | unique                 | 将列定义为唯一键                                             |
   | default                | 定义列的默认值                                               |
   | precision              | 指定列的精度                                                 |
   | scale                  | 指定列大小                                                   |
   | not null               | 指定列为 NOT NULL                                            |
   | autoIncrement          | 指定列为自动增长                                             |
   | autoIncrementIncrement | 自动步长，控制连续记录之间的间隔                             |
   | embedded               | 嵌套字段                                                     |
   | embeddedPrefix         | 嵌入字段的列名前缀                                           |
   | autoCreateTime         | 创建时追踪当前时间，对于 `int` 字段，它会追踪时间戳秒数，您可以使用 `nano`/`milli` 来追踪纳秒、毫秒时间戳，例如：`autoCreateTime:nano` |
   | autoUpdateTime         | 创建/更新时追踪当前时间，对于 `int` 字段，它会追踪时间戳秒数，您可以使用 `nano`/`milli` 来追踪纳秒、毫秒时间戳，例如：`autoUpdateTime:milli` |
   | index                  | 根据参数创建索引，多个字段使用相同的名称则创建复合索引，查看 [索引](https://gorm.io/zh_CN/docs/indexes.html) 获取详情 |
   | uniqueIndex            | 与 `index` 相同，但创建的是唯一索引                          |
   | check                  | 创建检查约束，例如 `check:age > 13`，查看 [约束](https://gorm.io/zh_CN/docs/constraints.html) 获取详情 |
   | <-                     | 设置字段写入的权限， `<-:create` 只创建、`<-:update` 只更新、`<-:false` 无写入权限、`<-` 创建和更新权限 |
   | ->                     | 设置字段读的权限，`->:false` 无读权限                        |
   | -                      | 忽略该字段，`-` 表示无读写，`-:migration` 表示无迁移权限，`-:all` 表示无读写迁移权限 |
   | comment                | 迁移时为字段添加注释                                         |

###### 关联标签

> GORM中的关联标签通常用于指定如何处理模型之间的关联。 这些标签定义了一些关系细节，比如外键，引用和约束。

| 标签               | 描述                                                         |
| :----------------- | :----------------------------------------------------------- |
| `foreignKey`       | Specifies the column name of the current model used as a foreign key in the join table. |
| `references`       | Indicates the column name in the reference table that the foreign key of the join table maps to. |
| `polymorphic`      | Defines the polymorphic type, typically the model name.      |
| `polymorphicValue` | Sets the polymorphic value, usually the table name, if not specified otherwise. |
| `many2many`        | Names the join table used in a many-to-many relationship.    |
| `joinForeignKey`   | Identifies the foreign key column in the join table that maps back to the current model’s table. |
| `joinReferences`   | Points to the foreign key column in the join table that links to the reference model’s table. |
| `constraint`       | Specifies relational constraints like `OnUpdate`, `OnDelete` for the association. |



###### 结构体标签

> 它们通过键值对的形式为字段提供元数据（metadata），供不同工具或框架解析和使用

1. 基本语法

   ```go
   type StructName struct {
       FieldName FieldType `gorm:"key1:value1;key2:value2;value3" json:"value1,value2"`
   }
   ```

2. 标签`gorm:"key:value"`

   > 这是 **GORM 框架**（Go 的 ORM 库）的标签，用于定义数据库表的字段约束和映射规则
   >
   > **数据库层面**：通过 `gorm` 标签控制字段的存储方式（长度、约束等）

   | **标签**        | **作用**                                 | **示例**                   |
   | :-------------- | :--------------------------------------- | :------------------------- |
   | `size`          | 指定数据库字段的长度，适用于strig        | `gorm:"size:64"`           |
   | `column`        | 指定数据库列名                           | `gorm:"column:user_name"`  |
   | `primaryKey`    | 标记为主键                               | `gorm:"primaryKey"`        |
   | `autoIncrement` | 自增字段（如 MySQL 的 `AUTO_INCREMENT`） | `gorm:"autoIncrement"`     |
   | `not null`      | 非空约束                                 | `gorm:"not null"`          |
   | `unique`        | 唯一约束                                 | `gorm:"unique"`            |
   | `index`         | 创建索引                                 | `gorm:"index"`             |
   | `default`       | 设置默认值                               | `gorm:"default:'guest'"`   |
   | `type`          | 强制指定数据库字段类型                   | `gorm:"type:varchar(100)"` |

3. 标签 `json:"name"`

   > 这是 **JSON 序列化/反序列化**（如 `encoding/json` 包）的标签，用于控制字段在 JSON 中的行为
   >
   > **API 层面**：通过 `json` 标签控制字段的输入输出格式

   | **标签**    | **作用**                                                     | **示例**                    |
   | :---------- | :----------------------------------------------------------- | :-------------------------- |
   | `name`      | 指定该字段在 JSON 中的键名为 `"name"`（默认使用结构体字段名） | `json:"username"`           |
   | `-`         | 表示该字段不参与 JSON 序列化（如敏感字段 `Password`）        | `json:"-"`                  |
   | `omitempty` | 空值时忽略该字段                                             | `json:"nickname,omitempty"` |
   | `string`    | 强制数值类型序列化为字符串                                   | `json:"age,string"`         |



###### 数据库迁移

```go
package flags

import (
    "time"
    "gorm.io/gorm"
	"blogx_server/global"
	"github.com/sirupsen/logrus"
)

var DB  *gorm.DB

type Model struct {
	ID        uint `gorm:"primaryKey"`
	CreatedAt time.Time
	UpdatedAt time.Time
}

type UserModel struct {
	Model
	Username       string `gorm:"size:32" json:"username"`
	Nickname       string `gorm:"size:32" json:"nickname"`
	Avatar         string `gorm:"size:256" json:"avatar"`
	Abstract       string `gorm:"size:256" json:"abstract"`
	RegisterSource int8   `json:"registerSource"` // 注册来源
	CodeAge        int    `json:"codeAge"`        // 码龄
	Password       string `gorm:"size:64" json:"-"`
	Email          string `gorm:"size:256" json:"email"`
	OpenID         string `gorm:"size:64" json:"openID"` // 第三方登陆的唯一id
}

func FlagDB() {
	err := DB.AutoMigrate(
		&UserModel{},
	)
	if err != nil {
		logrus.Errorf("数据迁移失败 %s", err)
		return
	}
	logrus.Infof("数据库迁移成功！")
}
```



###### 表增删改查操作

###### 数据过滤操作



##### 路由配置

- main.go

  ```go
  // 注册路由
  r := routers.SetupRouter()
  if err := r.Run(fmt.Sprintf(":%d", setting.Conf.Port)); err != nil {
      fmt.Println("server startup failed, err:%v\n", err)
  }
  ```

- routers.go

  ```go
  package routers
  
  import (
  	"bubble/controller"
  	"github.com/gin-gonic/gin"
  )
  
  func SetupRouter() *gin.Engine {
      // 创建路由引擎
  	r := gin.Default()
  	// 告诉gin框架模板文件引用的静态文件去哪里找
  	r.Static("/static", "static")
  	// 告诉gin框架去哪里找模板文件
  	r.LoadHTMLGlob("templates/*")
      // 返回index.html
  	r.GET("/", controller.IndexHandler)
  
  	// 配置路由组
  	v1Group := r.Group("v1")
  	{
  		// 添加
  		v1Group.POST("/todo", controller.Create)
  		// 查看
  		v1Group.GET("/todo", controller.Get)
  		// 修改
  		v1Group.PUT("/todo/:id", controller.Update)
  		// 删除
  		v1Group.DELETE("/todo/:id", controller.Delete)
  	}
  	return r
  }
  ```

##### 用户模块开发

###### 注册

###### 登录

##### 中间件开发

###### 认证

###### 权限

###### 限流

###### 分页

