# Stuchkut 语言
> 因 XiaohezAWA 太闲了于是使用 Python 制作的新编程语言执行器
当前版本：**0.3.0**（目前为半成品）

## 运行方式
### 环境要求：
#### 解释器版本：**Python 3.10+**
#### 外部库依赖：
暂无依赖库
### 运行脚本：
**python Main.py xxx.shk**
## 基本语法


语法分为三个大类：

### Chapters：

细分为 `Chapter.str`、`Chapter.int`、`Chapter.list` 和 `Chapter.map`，可修改、运用和展示的变量

### Tasks:

可以运行的内置函数

### symbols：

基础的关键字，已经实现了 `create`,`switch`,`ready`,`run`等

### 如何编程：

Stuchkut 在一段程序中只能操作一个 Chapter，而执行器提供了一个基础的名为 `lang` 的 Chapter.str。在默认情况下，所有需要指定操作对象 Chapter 的代码都会操作 `lang`。
首先，可以通过 `create` 关键字创建 Chapter：

```shk
create Chapter.str example
```

其中，`example` 作为新 Chapter 的名称，创建其他类型的 Chapter 亦如此。
接下来，使用 `switch` 关键字将操作对象切换至新 Chapter。

```shk
switch example
```

这样就好了。
想要一个基础的输出，需要改变 Chapter 的值，`Task.set` 可以给 Chapter 赋值。使 用 create 创建新 Task，再使用 ready 关键字将自己设为新 Task 的一个形参。

```shk
create Task.set SETTER
ready SETTER
```

其中，`SETTER` 是新 Task 的名称。一般来说，建议设为大写。再使用 `go` 将一个常 量作为 Task 的另一个形参。

```shk
go "Helloworld" str SETTER
```

使用 `go` 关键字时，需要另外输入常量的类型。再使用 `run` 关键字运行 `SETTER`  任务：

```shk
run SETTER
```
无输出，Chapter `example` 的值被改为 `"Helloworld"`。最后，输出使用的是 `Task.intro`。

```shk
create Task.intro INTROR
ready INTROR
run INTROR
```

输出：`Helloworld`。

```shk
create Task.intro INTROR
create Chapter.str shower
switch shower
create Task.set SETTER
go SETTER str "Helloworld"
run SETTER
ready INTROR
run INTROR
```

这就是一个 Helloworld 程序了。

### 方法

####基础

`intro[<Chapter.str>]`: 输出至命令行。
`set[<Chapter> <value>]`: 改变 Chapter 的值。
`create <type> <name>`: 创建新 Chapter/Task。
`switch <Chapter>`: 改变 `current_chapter`。
`ready <Task name>`: 将 `current_chapter` 当作指定 Task 的形参。
`go <value> <type> <Task name>`: 将一个值当作指定 Task 的形参。
`run <Task name>`: 运行指定 Task。
#### 数学运算

`add[<Chapter.int> <int>]`: 将当前 Chapter 的值与指定整数或另一个 Chapter 相加

`drop[<Chapter.int> <int>]`: 从当前 Chapter 的值中减去指定整数或另一个 Chapter

`mtpy[<Chapter.int> <int>]`: 将当前 Chapter 的值与指定整数或另一个 Chapter 相 乘

`dvsn[<Chapter.int> <int>]`: 将当前 Chapter 的值除以指定整数或另一个 Chapter (整数除法)

#### 对象操作

·`apnd[<Chapter.list> <value>]`: 在列表末尾添加一个元素

`dlnd[<Chapter.list>]`: 删除列表的最后一个元素

`istl[<Chapter.list> <int> <value>]`: 在指定位置插入元素

`setm[<Chapter.map> <str> <value>]`: 设置一对键值

`dlmp[<Chapter.map/list> <str/int>]`: 从映射或列表中删除指定键

`get[<Chapter.map/list> <str/int>]`: 从映射或列表中获取值，并存储到当前 Chapter

#### 数学比较
> 特别说明 此类 Task 不能直接调用只与 ifstamp 配合使用

`bigr[<Chapter.int> <int>]`: 比较当前 Chapter 的值是否大于指定值，返回布尔值

`smlr[<Chapter.int> <int>]`: 比较当前 Chapter 的值是否小于指定值，返回布尔值

`eqal[<Chapter.int> <int>]`: 比较当前 Chapter 的值是否等于指定值，返回布尔值

### stamps 控制流

> stamps 的设计刚刚加入, 尚有欠缺

`startstamp <name>`: 开始定义并执行一个代码块

`onlystamp <name>`: 只进行定义一个代码块

`endstamp`: 结束代码块定义

`backstamp <name>`: 执行指定的代码块

`ifstamp <condition_task> <stamp_name>`: 如果条件为真则执行代码块

### 附加:模拟 For 循环示例
```shk
^ i = 0

create Chapter.int i
create Task.intro INTROR
create Task.set SETR
create Task.add ADDR
create Task.smlr SMLR

^ init
switch i
go SETR int 0
run SETR

^ print
ready INTROR
run INTROR

startstamp LOOP
    clrtsk INTROR
    clrtsk ADDR
    clrtsk SMLR

    ready ADDR
    go ADDR int 1
    run ADDR

    ready INTROR
    run INTROR

    ^ 比较 i 和 10
    switch i
    ready SMLR
    go SMLR int 10
    run SMLR

    ifstamp SMLR LOOP
endstamp

backstamp LOOP
```
输出:
```output
0
1
2
3
4
5
6
7
8
9
10
11
```

**Stuchkut 的更多功能正在开发，请留意！**
