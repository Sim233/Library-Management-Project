# 数据库技术及应用大作业——图书馆管理系统

需要Python及PyQt5, sip库运行本项目，数据库类型为SQLite3。

### 数据库结构

数据库名为library，以db形式存储，**使用数据库SQLite3**

分为三个表，分别为user，book，borrow。

user用来存储用户信息。其中的列按顺序为：

userID 用来存储用户的学号 （**主键**）

userName 用户姓名

uPassword 登录密码

IsAdmin int 类型，0则为学生，1为管理员

numborrowed 借书本数。设置最多借六本书

uGraduated int类型，在校为0，毕业为1，毕业生无借书权限，但可以还书



book用来存储书籍信息，其中列按顺序为：

bookID 书籍编号，为8位字符 （**主键**）

bookName 书名

bookAur 书籍作者

bookCategory 书籍分类，其可选类别为：

```
["哲学", "数学", "物理学", "化学", "政治", "社会学", "法律", "军事", "经济学", "教育", "体育", "文学", "艺术", "历史", "地理", "天文学", "生物学", "医学卫生", "农业", "计算机", "工程技术", "心理学"]
```

numstore 总库存量 int

numavai 现有可借的书籍量 int 初始化为与numstore相同数值



borrow用来存储借书记录，列按顺序为：

userID 借书的用户ID（**外键**）

bookID 借阅的书籍编号 （**外键**）

identiID 借阅记录编号，为studentID+bookID （**主键**）

borrowtime 为date类型，借书时间

returntime 归还时间，默认为借书时间三月后



### 程序结构

`MainWindow.py` 数据库系统主页面，可连接到注册和登录页面

`register.py` 注册页面，创建新的用户

`Login.py` 登入页面，登录后会根据用户类型跳转到AdminHome或StuHome

`AdminHome.py` 管理员主页，可执行的操作按钮为添加书籍、删除书籍、查看用户学号和姓名

`StuHome.py` 学生主页，可执行的操作为书籍查找，借阅书籍，归还书籍

`bookStorageViewer.py` 查看与查询书籍功能实现

`UserManage.py` 查看已录入的学生学号和姓名

`addBookDialog.py` 实现加入书籍的会话

`dropBookDialog.py` 实现删除书籍的会话

`borrowBookDialog.py` 实现借阅书籍的会话

`returnBookDialog.py` 实现归还书籍的会话

`borrowStatusViewer.py` 查看已借阅的书籍