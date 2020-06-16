# 数据库技术及应用大作业——图书馆管理系统

需要Python及PyQt5, sip库运行本项目，数据库类型为SQLite3。

### 数据库结构

数据库名为library，以db形式存储，**使用数据库SQLite3**

分为三个表，分别为user，book，borrow。

user用来存储用户信息。其中的列按顺序为：

studentID 8位 用来存储用户的学号。主键

stuname 用户姓名

stupassword 登录密码

IsAdmin int 类型，0则为学生，1为管理员

numborrowed 借书本数。设置最多借六本书



book用来存储书籍信息，其中列按顺序为：

bookname 书名

bookID 书籍编号，为8位字符 主键

bookaur 书籍作者

bookcate 书籍分类。可选类别为：

```
["哲学", "物理学", "政治", "法律", "军事", "经济", "文化", "教育", "体育", "语言文字", "艺术", "历史", "地理", "天文学", "生物学", "医学卫生", "农业"]
```

numstore 总库存量

numavai 现有可借的书籍量



borrow用来存储借书记录，列按顺序为：

student_ID 借书的用户ID

bookID 借阅的书籍编号

identiID 借阅记录编号，为studentID+bookID ，主键

borrowtime 为date类型，借书时间

returntime 归还时间，默认为借书时间三月后



### 程序结构

MainWindow 数据库系统主页面，可连接到注册和登录页面

register 注册页面，创建新的用户

Login 登入页面，登录后会根据用户类型跳转到AdminHome或StuHome

AdminHome 管理员主页，可执行的操作按钮为添加书籍、删除书籍、查看用户学号和姓名

StuHome 学生主页，可执行的操作为书籍查找，借阅书籍，归还书籍

bookstorageViewer 查看与查询书籍功能实现

UserManage 查看已录入的学生学号和姓名

addbookDialog 实现加入书籍的会话

dropbookDialog 实现删除书籍的会话

borrowBookDialog 实现借阅书籍的会话

returnBookDialog 实现归还书籍的会话

borrowstatusViewer 查看已借阅的书籍