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

##### redis配置

- redis连接初始化

  ```go
  import (
  	"blogx_server/global"
  	"github.com/go-redis/redis"
  	"github.com/sirupsen/logrus"
  )
  
  type Redis struct {
  	Addr     string `yaml:"addr"`
  	Password string `yaml:"password"`
  	DB       int    `yaml:"db"`
  }
  
  func InitRedis() *redis.Client {
  	r := global.Config.Redis
  	redisDB := redis.NewClient(&redis.Options{
  		Addr:     r.Addr,     // 不写默认就是这个
  		Password: r.Password, // 密码
  		DB:       r.DB,       // 默认是0
  	})
  	_, err := redisDB.Ping().Result()
  	if err != nil {
  		logrus.Fatalf("redis连接失败 %s", err)
  	}
  	logrus.Info("redis连接成功")
  	return redisDB
  }
  ```

- redis的使用

  ```go
  // 添加数据
  _, err = global.Redis.Set(key, value.String(), time.Duration(second)*time.Second).Result()
  	if err != nil {
  		logrus.Errorf("redis添加黑名单失败 %s", err)
  		return
  	}
  
  // 获取数据
  value, err := global.Redis.Get(key).Result()
  if err != nil {
      return
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

###### 数据库迁移(DB.AutoMigrate(&Model))

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
        ...
	)
	if err != nil {
		logrus.Errorf("数据迁移失败 %s", err)
		return
	}
	logrus.Infof("数据库迁移成功！")
}
```

###### 列表查询(query.Offset(offset).Limit(limit).Find(&list).Error)

- enter.go

  ```go
  type BannerApi struct {
  }
  
  type BannerListRequest struct {
  	common.PageInfo
  	Show bool `form:"show"`
  }
  
  func (BannerApi) BannerListView(c *gin.Context) {
  	var cr BannerListRequest
  	c.ShouldBindQuery(&cr)
  
  	list, count, _ := common.ListQuery(models.BannerModel{
  		Show: cr.Show,
  	}, common.Options{
  		PageInfo: cr.PageInfo,
  	})
  
  	res.OkWithList(list, count, c)
  }
  ```

- list.query.go

  ```go
  // common/list_query.go
  package common
  
  import (
  	"blogx_server/global"
  	"fmt"
  	"gorm.io/gorm"
  )
  
  type PageInfo struct {
  	Limit int    `form:"limit"`
  	Page  int    `form:"page"`
  	Key   string `form:"key"`
  	Order string `form:"order"` // 前端可以覆盖
  }
  
  func (p PageInfo) GetPage() int {
  	if p.Page > 20 || p.Page <= 0 {
  		return 1
  	}
  	return p.Page
  }
  
  func (p PageInfo) GetLimit() int {
  	if p.Limit <= 0 || p.Limit > 100 {
  		return 10
  	}
  	return p.Limit
  }
  func (p PageInfo) GetOffset() int {
  	return (p.GetPage() - 1) * p.GetLimit()
  }
  
  type Options struct {
  	PageInfo     PageInfo
  	Likes        []string
  	Preloads     []string
  	Where        *gorm.DB
  	Debug        bool
  	DefaultOrder string
  }
  
  func ListQuery[T any](model T, option Options) (list []T, count int, err error) {
  
  	// 自己的基础查询
  	query := global.DB.Model(model).Where(model)
  
  	// 日志
  	if option.Debug {
  		query = query.Debug()
  	}
  
  	// 模糊匹配
  	if len(option.Likes) > 0 && option.PageInfo.Key != "" {
  		likes := global.DB.Where("")
  		for _, column := range option.Likes {
  			likes.Or(
  				fmt.Sprintf("%s like ?", column),
  				fmt.Sprintf("%%%s%%", option.PageInfo.Key))
  		}
  		query = query.Where(likes)
  	}
  
  	// 高级查询
  	if option.Where != nil {
  		query = query.Where(option.Where)
  	}
  
  	// 预加载
  	for _, preload := range option.Preloads {
  		query = query.Preload(preload)
  	}
  
  	// 查总数
  	var _c int64
  	query.Count(&_c)
  	count = int(_c)
  
  	// 分页
  	limit := option.PageInfo.GetLimit()
  	offset := option.PageInfo.GetOffset()
  
  	// 排序
  	if option.PageInfo.Order != "" {
  		// 在外层配置了
  		query = query.Order(option.PageInfo.Order)
  	} else {
  		if option.DefaultOrder != "" {
  			query = query.Order(option.DefaultOrder)
  		}
  	}
  
  	err = query.Offset(offset).Limit(limit).Find(&list).Error
  	return
  }
  
  ```

###### 单例查询(DB.Take(&model, id).Error)

```go
var log models.LogModel
err = DB.Take(&log, id).Error
```

###### 创建操作(DB.Create(&model{key: value, ...}).Error)

- 语法

  ```go
  err = global.DB.Create(&model{
      key1: value1,
      key2: value2,
      ...
  }).Error
  if err != nil {
  		// 处理错误逻辑
  		return
  	}
  ```

- 案例

  ```go
  func (BannerApi) BannerCreateView(c *gin.Context) {
  	var cr BannerCreateRequest
  	err := c.ShouldBindJSON(&cr)
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  	err = global.DB.Create(&models.BannerModel{
  		Cover: cr.Cover,
  		Href:  cr.Href,
  		Show:  cr.Show,
  	}).Error
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  	res.OkWithMsg("添加banner成功", c)
  }
  ```

###### 更新操作(DB.Model(&model).Updates().Error)

```go
type IDRequest struct {
	ID uint `json:"id" form:"id" uri:"id"`
}

type BannerCreateRequest struct {
	Cover string `json:"cover" binding:"required"`
	Href  string `json:"href"`
	Show  bool   `json:"show"`
}

type Model struct {
	ID        uint      `gorm:"primaryKey" json:"id"`
	CreatedAt time.Time `json:"createdAt"`
	UpdatedAt time.Time `json:"updatedAt"`
}

type BannerModel struct {
	Model
	Show  bool   `json:"show"`  // 是否展示
	Cover string `json:"cover"` // 图片链接
	Href  string `json:"href"`  // 跳转链接
}

func (BannerApi) BannerUpdateView(c *gin.Context) {
	var id models.IDRequest
	err := c.ShouldBindUri(&id)
	if err != nil {
		res.FailWithError(err, c)
		return
	}
	var cr BannerCreateRequest
	err = c.ShouldBindJSON(&cr)
	if err != nil {
		res.FailWithError(err, c)
		return
	}

	var model models.BannerModel
	err = global.DB.Take(&model, id.ID).Error
	if err != nil {
		res.FailWithMsg("不存在的banner", c)
		return
	}

	err = global.DB.Model(&model).Updates(map[string]any{
		"cover": cr.Cover,
		"href":  cr.Href,
		"show":  cr.Show,
	}).Error
	if err != nil {
		res.FailWithError(err, c)
		return
	}
	res.OkWithMsg("banner更新成功", c)
}
```

###### 删除操作(DB.Delete(&logList))

```go
// 支持删除多条
type RemoveRequest struct {
	IDList []uint `json:"IDList"`
}

func (LogApi) LogRemoveView(c *gin.Context) {
	var cr models.RemoveRequest
	err := c.ShouldBindJSON(&cr)
	if err != nil {
		res.FailWithError(err, c)
		return
	}

	var logList []models.LogModel
	global.DB.Find(&logList, "id in ?", cr.IDList)

	if len(logList) > 0 {
		global.DB.Delete(&logList)
	}
```

###### 过滤分页排序

- common/list_query.go

  ```go
  package common
  
  import (
  	"blogx_server/global"
  	"fmt"
  	"gorm.io/gorm"
  )
  
  type PageInfo struct {
  	Limit int    `form:"limit"`  // 分页，每页的条目
  	Page  int    `form:"page"`  // 查询第几页
  	Key   string `form:"key"`  // 关键字查询，模糊查询
  	Order string `form:"order"` // 排序，前端可以覆盖
  }
  
  func (p PageInfo) GetPage() int {
  	if p.Page > 20 || p.Page <= 0 {
  		return 1
  	}
  	return p.Page
  }
  
  func (p PageInfo) GetLimit() int {
  	if p.Limit <= 0 || p.Limit > 100 {
  		return 10
  	}
  	return p.Limit
  }
  func (p PageInfo) GetOffset() int {
  	return (p.GetPage() - 1) * p.GetLimit()
  }
  
  type Options struct {
  	PageInfo     PageInfo
  	Likes        []string
  	Preloads     []string
  	Where        *gorm.DB
  	Debug        bool
  	DefaultOrder string
  }
  
  func ListQuery[T any](model T, option Options) (list []T, count int, err error) {
  
  	// 自己的基础查询
  	query := global.DB.Model(model).Where(model)
  
  	// 日志
  	if option.Debug {
  		query = query.Debug()
  	}
  
  	// 模糊匹配
  	if len(option.Likes) > 0 && option.PageInfo.Key != "" {
  		likes := global.DB.Where("")
  		for _, column := range option.Likes {
  			likes.Or(
  				fmt.Sprintf("%s like ?", column),
  				fmt.Sprintf("%%%s%%", option.PageInfo.Key))
  		}
  		query = query.Where(likes)
  	}
  
  	// 高级查询
  	if option.Where != nil {
  		query = query.Where(option.Where)
  	}
  
  	// 预加载
  	for _, preload := range option.Preloads {
  		query = query.Preload(preload)
  	}
  
  	// 查总数
  	var _c int64
  	query.Count(&_c)
  	count = int(_c)
  
  	// 分页
  	limit := option.PageInfo.GetLimit()
  	offset := option.PageInfo.GetOffset()
  
  	// 排序
  	if option.PageInfo.Order != "" {
  		// 在外层配置了
  		query = query.Order(option.PageInfo.Order)
  	} else {
  		if option.DefaultOrder != "" {
  			query = query.Order(option.DefaultOrder)
  		}
  	}
  
  	err = query.Offset(offset).Limit(limit).Find(&list).Error
  	return
  }
  ```

- api/log_api/enter.go

  ```go
  package log_api
  
  import (
  	"blogx_server/common"
  	"blogx_server/common/res"
  	"blogx_server/models"
  	"blogx_server/models/enum"
  	"github.com/gin-gonic/gin"
  )
  
  type LogApi struct {
  }
  
  // 这里自定义配置的字段属性，表示允许接收前端传来的表单信息
  type LogListRequest struct {
  	common.PageInfo
  	LogType     enum.LogType      `form:"logType"` // 日志类型 1 2 3
  	Level       enum.LogLevelType `form:"level"`
  	UserID      uint              `form:"userID"`
  	IP          string            `form:"ip"`
  	LoginStatus bool              `form:"loginStatus"`
  	ServiceName string            `form:"serviceName"`
  }
  
  type LogListResponse struct {
  	models.LogModel
  	UserNickname string `json:"userNickname"`
  	UserAvatar   string `json:"userAvatar"`
  }
  
  func (LogApi) LogListView(c *gin.Context) {
  	// 分页 查询（精确查询，模糊匹配）
  	var cr LogListRequest
  	err := c.ShouldBindQuery(&cr)
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  
  	list, count, err := common.ListQuery(models.LogModel{
  		LogType:     cr.LogType,
  		Level:       cr.Level,
  		UserID:      cr.UserID,
  		IP:          cr.IP,
  		LoginStatus: cr.LoginStatus,
  		ServiceName: cr.ServiceName,
  	}, common.Options{
  		PageInfo:     cr.PageInfo,
  		Likes:        []string{"title", "service_name"},  // 配置可以模糊搜索的字段信息
  		Preloads:     []string{"UserModel"},
  		Debug:        true,
  		DefaultOrder: "created_at desc",  // 配置根据哪个字段进行排序，是否倒序，且前端可以传表单信息进行覆盖
  	})
  
  	var _list = make([]LogListResponse, 0)
  	for _, logModel := range list {
  		_list = append(_list, LogListResponse{
  			LogModel:     logModel,
  			UserNickname: logModel.UserModel.Nickname,
  			UserAvatar:   logModel.UserModel.Avatar,
  		})
  	}
  
  	res.OkWithList(_list, int(count), c)
  	return
  
  }
  ```

##### GORM钩子函数

> 在 GORM（Go 的 ORM 框架）中，**数据库钩子（Hooks）** 是一组预定义的方法，允许你在模型的生命周期（如创建、更新、删除）的特定阶段插入自定义逻辑。
>
> 这些钩子方法会在执行数据库操作（如 `Get`、`Create`、`Update`、`Delete` 等）时自动触发。

###### GORM支持的钩子函数

| **钩子方法**       | **触发时机**                                                 |
| :----------------- | :----------------------------------------------------------- |
| **`BeforeSave`**   | 在执行 `Save` 或任何包含 `Save` 的操作（如 `Create`、`Update`）**之前**触发 |
| **`AfterSave`**    | 在执行 `Save` 或相关操作**之后**触发                         |
| **`BeforeCreate`** | 在执行 `Create` 操作**之前**触发                             |
| **`AfterCreate`**  | 在执行 `Create` 操作**之后**触发                             |
| **`BeforeUpdate`** | 在执行 `Update` 操作**之前**触发                             |
| **`AfterUpdate`**  | 在执行 `Update` 操作**之后**触发                             |
| **`BeforeDelete`** | 在执行 `Delete` 操作**之前**触发                             |
| **`AfterDelete`**  | 在执行 `Delete` 操作**之后**触发                             |
| **`AfterFind`**    | 在执行查询操作（如 `First`、`Find`）**之后**触发             |
| **`BeforeQuery`**  | 在执行任何查询操作（如 `Find`、`First`）**之前**触发         |
| **`AfterQuery`**   | 在执行任何查询操作**之后**触发                               |

###### 钩子函数的应用

1. 密码加密

   ```go
   type User struct {
       ID       uint
       Username string
       Password string
   }
   
   // BeforeCreate 钩子：创建用户前加密密码
   func (u *User) BeforeCreate(tx *gorm.DB) error {
       hashedPassword, err := bcrypt.GenerateFromPassword([]byte(u.Password), bcrypt.DefaultCost)
       if err != nil {
           return err
       }
       u.Password = string(hashedPassword)
       return nil
   }
   
   // 创建用户时自动触发加密
   user := User{Username: "alice", Password: "123456"}
   db.Create(&user)
   ```

2. 错误处理

   ```go
   // 在钩子中返回 error 会 终止后续操作 并回滚事务
   
   func (u *User) BeforeDelete(tx *gorm.DB) error {
       if u.Username == "admin" {
           return errors.New("禁止删除管理员用户")
       }
       return nil
   }
   
   // 尝试删除管理员会失败
   db.Delete(&User{Username: "admin"}) // 错误：禁止删除管理员用户
   ```

3. 自动维护时间戳

   ```go
   type Post struct {
       ID        uint
       Title     string
       CreatedAt time.Time
       UpdatedAt time.Time
   }
   
   // BeforeCreate 钩子：设置创建时间
   func (p *Post) BeforeCreate(tx *gorm.DB) error {
       p.CreatedAt = time.Now()
       return nil
   }
   
   // BeforeUpdate 钩子：设置更新时间
   func (p *Post) BeforeUpdate(tx *gorm.DB) error {
       p.UpdatedAt = time.Now()
       return nil
   }
   ```

4. 级联删除关联资源

   ```go
   type Article struct {
       ID      uint
       Content string
       Images  []Image `gorm:"foreignKey:ArticleID"`
   }
   
   // BeforeDelete 钩子：删除文章前删除关联图片
   func (a *Article) BeforeDelete(tx *gorm.DB) error {
       // 删除所有关联的图片记录
       if err := tx.Where("article_id = ?", a.ID).Delete(&Image{}).Error; err != nil {
           return err
       }
       // 删除本地文件（假设 Image 模型有 Path 字段）
       var images []Image
       tx.Model(&a).Association("Images").Find(&images)
       for _, img := range images {
           os.Remove(img.Path)
       }
       return nil
   }
   ```

5. 数据校验

   ```go
   type Product struct {
       ID    uint
       Price float64
   }
   
   // BeforeSave 钩子：校验价格必须为正数
   func (p *Product) BeforeSave(tx *gorm.DB) error {
       if p.Price <= 0 {
           return errors.New("价格必须大于 0")
       }
       return nil
   }
   ```

###### 高级用法

1. 跳过钩子

   ```go
   // 跳过所有钩子
   db.Session(&gorm.Session{SkipHooks: true}).Create(&user)
   ```

2. 事务中的钩子

   ```go
   // 钩子默认在事务内执行。若钩子返回错误，整个操作会回滚：
   
   func (u *User) BeforeCreate(tx *gorm.DB) error {
       // 在事务中执行操作
       if err := tx.Create(&Profile{UserID: u.ID}).Error; err != nil {
           return err
       }
       return nil
   }
   ```

###### 钩子函数的实现机制

> 钩子函数的自动调用是通过 **反射（Reflection）** 和 **接口方法匹配** 机制实现的。
>
> GORM 内部维护了一个钩子方法列表，覆盖了所有支持的钩子类型（如 `BeforeCreate`、`AfterUpdate` 等）。当执行数据库操作（如 `Create`、`Update`）时，GORM 会按顺序触发对应阶段的钩子。

- 方法签名的强制匹配

  ```go
  // GORM 要求钩子方法的签名必须严格符合以下格式：
  func (model *YourModel) HookName(tx *gorm.DB) error{
      // 业务逻辑
      return nil  // 若返回非 `nil` 错误，GORM 会终止操作并回滚
  }
  ```

  - **方法名**：如 `BeforeCreate`、`AfterUpdate`，必须与钩子名称完全一致。

    > 约定优于配置：GORM 通过 **方法名的约定**（如 `BeforeCreate`）自动关联钩子，开发者无需手动注册钩子或修改框架代码。

  - **参数**：必须接受一个 `*gorm.DB` 参数（表示当前数据库事务）。

    > 钩子方法在数据库事务中执行，若钩子返回错误，GORM 会自动回滚整个操作

  - **返回值**：必须返回 `error` 类型（若返回非 `nil` 错误，GORM 会终止操作并回滚）。

- GORM源码中的钩子调用

  ```go
  // 伪代码：GORM 的钩子处理器
  func CallMethod(db *gorm.DB, hookName string) error {
      // 通过反射获取模型实例：利用 Go 的反射机制，GORM 能在运行时动态检查并调用模型的方法，实现高度灵活性
      modelValue := reflect.ValueOf(db.Statement.Model)
      method := modelValue.MethodByName(hookName)
      
      if method.IsValid() {
          // 调用钩子方法
          result := method.Call([]reflect.Value{reflect.ValueOf(db)})
          if len(result) > 0 && !result[0].IsNil() {
              return result[0].Interface().(error)
          }
      }
      return nil
  }
  
  // 在 Create 操作中触发钩子
  func CreateCallback(db *gorm.DB) {
      // 触发 BeforeCreate：GORM 通过 方法名的约定自动关联钩子，开发者无需手动注册钩子或修改框架代码
      if err := CallMethod(db, "BeforeCreate"); err != nil {
          db.AddError(err)
          return
      }
      
      // 执行 INSERT 操作
      executeSQL(db)
      
      // 触发 AfterCreate
      CallMethod(db, "AfterCreate")
  }
  ```





##### 路由配置

- main.go

  ```go
  package main
  
  func main() {
  	// 启动web程序
  	router.Run()
  }
  ```

- conf/conf_system.go

  ```go
  package conf
  
  import "fmt"
  
  type System struct {
  	IP   string `yaml:"ip"`
  	Port int    `yaml:"port"`
  }
  
  func (s System) Addr() string {
  	return fmt.Sprintf("%s:%d", s.IP, s.Port)
  }
  ```

- api/enter.go

  ```go
  package api
  
  import "blogx_server/api/site_api"
  
  type Api struct {
  	SiteApi site_api.SiteApi
  }
  
  var App = Api{}
  ```

- api/site_api/enter.go

  ```go
  package site_api
  
  import (
  	"fmt"
  	"github.com/gin-gonic/gin"
  )
  
  type SiteApi struct {
  }
  
  func (SiteApi) SiteInfoView(c *gin.Context) {
  	fmt.Println("1")
  	c.JSON(200, gin.H{"code": 0, "msg": "站点信息"})
  	return
  }
  ```

- router/site_router.go

  ```go
  package router
  
  import (
  	"blogx_server/api"
  	"github.com/gin-gonic/gin"
  )
  
  func SiteRouter(r *gin.RouterGroup) {
  	app := api.App.SiteApi
  	r.GET("site", app.SiteInfoView)
  }
  ```

- router/enter.go

  ```go
  package router
  
  import (
  	"blogx_server/global"
  	"github.com/gin-gonic/gin"
  )
  
  func Run() {
  	r := gin.Default()
  
  	nr := r.Group("/api")
  
  	SiteRouter(nr)
  
  	addr := global.Config.System.Addr()
  	r.Run(addr)
  }
  ```

###### 路由响应

| **场景**     | **方法**                |
| :----------- | :---------------------- |
| API 数据交互 | `c.JSON()` / `c.XML()`  |
| 网页渲染     | `c.HTML()`              |
| 文件传输     | `c.File()` / `c.Data()` |
| 流式处理     | `c.Stream()`            |
| 重定向       | `c.Redirect()`          |
| 静态资源托管 | `router.Static()`       |

###### 静态路由配置

- **静态资源托管**：将本地目录中的文件（如 HTML、CSS、JS、图片）映射到 Web 服务器的指定路由路径。
- **简化访问**：用户可通过 URL 直接访问静态文件，无需编写额外路由逻辑。

```go
package main

import "github.com/gin-gonic/gin"

func main() {
    r := gin.Default()

    // 将 "./public" 目录下的文件映射到 "/static" 路径
    r.Static("/static", "./public")

    r.Run(":8080")
}
```



##### 用户模块开发

###### 注册

###### 登录

##### 中间件开发

```go
package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
    nr := r.Group("/api")
    nr.Use(middleware ...HandlerFunc)  // 路由组中使用中间件
    // 单个路由中使用中间件
    r.PUT("site", middleware.AdminMiddleware, app.SiteUpdateView)
}
```

- 中间件执行流程控制
  - 默认顺序：Gin 的中间件按照注册顺序依次执行。
- **`c.Next()` 的作用**：
  - 在调用 `c.Next()` 时，Gin 会暂停当前中间件的执行。
    - **执行后续中间件和路由处理函数**。
    - 当后续所有操作完成后，返回到当前中间件继续执行 `c.Next()` 之后的代码。

- **`c.Abort()`**：终止后续中间件和路由的执行，直接返回响应。



###### 认证





###### 权限

- 管理员权限校验

  ```go
  type RoleType int8
  
  const (
  	AdminRole   RoleType = 1
  	UserRole    RoleType = 2
  	VisitorRole RoleType = 3
  )
  
  func ParseTokenByGin(c *gin.Context) (*MyClaims, error) {
  	token := c.GetHeader("token")
  	if token == "" {
  		token = c.Query("token")
  	}
  
  	return ParseToken(token)
  }
  
  func AdminMiddleware(c *gin.Context) {
  	claims, err := jwts.ParseTokenByGin(c)
  	if err != nil {
  		res.FailWithError(err, c)
  		c.Abort()
  		return
  	}
  	if claims.Role != enum.AdminRole {
  		res.FailWithMsg("权限错误", c)
  		c.Abort()
  		return
  	}
  	blcType, ok := redis_jwt.HasTokenBlackByGin(c)
  	if ok {
  		res.FailWithMsg(blcType.Msg(), c)
  		c.Abort()
  		return
  	}
  	c.Set("claims", claims)
  }
  ```



###### 限流

##### 文件管理

###### 文件上传

- 核心

  ```go
  func ImageUploadView(c *gin.Context) {
  	fileHeader, err := c.FormFile("file")
      filePath := fmt.Sprintf("uploads/%s/%s.%s", UploadDir, hash, suffix)
      c.SaveUploadedFile(fileHeader, filePath)
  }
  ```

- 案例

  ```go
  // api/image_api/image_upload.go
  package image_api
  
  import (
  	"blogx_server/common/res"
  	"blogx_server/global"
  	"blogx_server/models"
  	"blogx_server/utils"
  	"fmt"
  	"github.com/gin-gonic/gin"
  	"github.com/pkg/errors"
  	"github.com/sirupsen/logrus"
  	"io"
  	"strings"
  )
  
  func (ImageApi) ImageUploadView(c *gin.Context) {
  	fileHeader, err := c.FormFile("file")
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  	// 文件大小判断
  	s := global.Config.Upload.Size
  	if fileHeader.Size > s*1024*1024 {
  		res.FailWithMsg(fmt.Sprintf("文件大小大于%dMB", s), c)
  		return
  	}
  	// 后缀判断
  	filename := fileHeader.Filename
  	suffix, err := imageSuffixJudge(filename)
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  	// 文件hash
  	file, err := fileHeader.Open()
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  	byteData, _ := io.ReadAll(file)
  	hash := utils.Md5(byteData)
  	// 判断这个hash有没有
  	var model models.ImageModel
  	err = global.DB.Take(&model, "hash = ?", hash).Error
  	if err == nil {
  		// 找到了
  		logrus.Infof("上传图片重复 %s <==> %s  %s", filename, model.Filename, hash)
  		res.Ok(model.WebPath(), "上传成功", c)
  		return
  	}
  
  	// 文件名称一样，但是文件内容不一样
  
  	filePath := fmt.Sprintf("uploads/%s/%s.%s", global.Config.Upload.UploadDir, hash, suffix)
  	// 入库
  	model = models.ImageModel{
  		Filename: filename,
  		Path:     filePath,
  		Size:     fileHeader.Size,
  		Hash:     hash,
  	}
  	err = global.DB.Create(&model).Error
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  
  	c.SaveUploadedFile(fileHeader, filePath)
  	res.Ok(model.WebPath(), "图片上传成功", c)
  
  }
  
  func imageSuffixJudge(filename string) (suffix string, err error) {
  	_list := strings.Split(filename, ".")
  	if len(_list) == 1 {
  		err = errors.New("错误的文件名")
  		return
  	}
  	// xxx.jpg   xxx  xxx.jpg.exe
  	suffix = _list[len(_list)-1]
  	if !utils.InList(suffix, global.Config.Upload.WhiteList) {
  		err = errors.New("文件非法")
  		return
  	}
  	return
  }
  ```

###### 文件获取





###### 文件删除

- 主函数

  ```go
  func (ImageApi) ImageRemoveView(c *gin.Context) {
  	var cr models.RemoveRequest
  	err := c.ShouldBindJSON(&cr)
  	if err != nil {
  		res.FailWithError(err, c)
  		return
  	}
  	log := log_service.GetLog(c)
  	log.ShowRequest()
  	log.ShowResponse()
  
  	var list []models.ImageModel
  	global.DB.Find(&list, "id in ?", cr.IDList)
  
  	var successCount, errCount int64
  	if len(list) > 0 {
  		successCount = global.DB.Delete(&list).RowsAffected
  	}
  	errCount = int64(len(list)) - successCount
  
  	msg := fmt.Sprintf("操作成功，成功%d 失败%d", successCount, errCount)
  
  	res.OkWithMsg(msg, c)
  }
  ```

- 数据库钩子（Hook）函数

  ```go
  type ImageModel struct {
  	Model
  	Filename string `gorm:"size:64" json:"filename"`
  	Path     string `gorm:"size:256" json:"path"`
  	Size     int64  `json:"size"`
  	Hash     string `gorm:"size:32" json:"hash"`
  }
  
  // 删除前自动触发该钩子函数
  func (l ImageModel) BeforeDelete(tx *gorm.DB) error {
  	err := os.Remove(l.Path)
  	if err != nil {
  		logrus.Warnf("删除文件失败 %s", err)
  	}
  	return nil
  }
  ```























