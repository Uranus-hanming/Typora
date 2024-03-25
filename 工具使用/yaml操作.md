[toc]

> 简单表达清单、散列表，标量等数据形态。它使用空白符号缩进和大量依赖外观的特色，特别适合用来表达或编辑数据结构、各种配置文件、倾印调试内容、文件大纲

### 基本语法

- 大小写敏感
- 使用缩进表示层级关系
- 缩进不允许使用tab，只允许空格
- 缩进的空格数不重要，只要相同层级的元素左对齐即可
- '#'表示注释

### 数据类型

- 对象：键值对的集合，又称为映射（mapping）/ 哈希（hashes） / 字典（dictionary）
- 数组：一组按次序排列的值，又称为序列（sequence） / 列表（list）
- 纯量（scalars）：单个的、不可再分的值

##### YAML 对象

- 对象键值对使用冒号结构表示 **key: value**，冒号后面要加一个空格。

- 也可以使用 **key:{key1: value1, key2: value2, ...}**。

- 还可以使用缩进表示层级关系；

##### YAML 数组：以 **-** 开头的行表示构成一个数组

##### 复合结构：数组和对象可以构成复合结构

```shell
languages:
  - Ruby
  - Perl
  - Python 
websites:
  YAML: yaml.org 
  Ruby: ruby-lang.org 
  Python: python.org 
  Perl: use.perl.org
```

```shell
# 轉換為json:
{ 
  languages: [ 'Ruby', 'Perl', 'Python'],
  websites: {
    YAML: 'yaml.org',
    Ruby: 'ruby-lang.org',
    Python: 'python.org',
    Perl: 'use.perl.org' 
  } 
}
```

##### 纯量：纯量是最基本的，不可再分的值

- 字符串
- 布尔值
- 整数
- 浮点数
- Null
- 时间
- 日期