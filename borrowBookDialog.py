import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *


class borrowBookDialog(QDialog):
    borrow_book_success_signal = pyqtSignal()

    def __init__(self, StudentId, parent=None):
        super(borrowBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("借阅书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["哲学", "物理学", "政治", "法律", "军事", "经济", "文化", "教育", "体育", "语言文字", "艺术", "历史"
            , "地理", "天文学", "生物学", "医学卫生", "农业"]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.borrowLabel = QLabel('借阅书籍')
        self.layout.addRow('', self.borrowLabel)

        # 表单结构
        # 借阅人学号
        # 借阅书籍书号


        self.userLable = QLabel('借阅人学号')
        self.uerEdit = QLabel(self.studentId)
        self.layout.addRow(self.userLable, self.uerEdit)

        self.bookIdLabel = QLabel('索书号')
        self.bookIdEdit = QLineEdit()
        self.bookIdEdit.setMaxLength(8)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)

        # 统一设定只读属性
        # 书名
        # 作者
        # 分类
        self.bookNameLabel = QLabel("书    名:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")

        self.bookNameEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)

        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)

        self.bookNameEdit.setReadOnly(True)
        self.bookNameEdit.setStyleSheet("background-color:#363636")
        self.authNameEdit.setReadOnly(True)
        self.authNameEdit.setStyleSheet("background-color:#363636")
        self.categoryComboBox.setStyleSheet("background-color:#363636")



        self.borrowBookButton = QPushButton('确认借阅')
        self.borrowBookButton.setFixedWidth(140)
        self.borrowBookButton.setFixedHeight(32)
        self.layout.addRow('', self.borrowBookButton)


        self.borrowLabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.borrowBookButton.clicked.connect(self.borrowButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.bookIdEdit.returnPressed.connect(self.borrowButtonClicked)

    def borrowButtonClicked(self):
        # 更新book表中numavai，user表中numborrowed， borrow表中插入借书记录
        bookId = self.bookIdEdit.text()
        # 字符串拼接的方式来实现借书操作的Id号
        sID = self.studentId
        borrowId = sID + bookId
        # 如果索书号为空
        if (bookId == ""):
            print(QMessageBox.warning(self, "警告", "索书号不能为空，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库进行操作
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()

        #根据索书号进行查询：
        sql = "SELECT * from book where bookID='%s' " % (bookId)
        query.exec_(sql)
        if (not query.next()):
            print(QMessageBox.warning(self, "警告", "你所要借的书不存在，请查看输入", QMessageBox.Ok))
            return
        elif query.value(5) == 0 :
            print(QMessageBox.information(self, "警告", "这本书已经被借完，请之后再来", QMessageBox.Ok))
            return

        # 设置借书上限：若一个读者已经借了6本书，则不能再次借书
        sql = "SELECT * from User where studentID='%s' " % (bookId)
        query.exec_(sql)
        if( query.next()):
            booknum = query.value(4)
            if booknum == 6:
                print(QMessageBox.warning(self,'提示', '您已达到借书上限！', QMessageBox.Ok))
                return
        sql = "SELECT * from borrow where identiID='%s' " % borrowId
        query.exec_(sql)
        if(query.next()):
            print(QMessageBox.warning(self, '提示', '您已经借阅了此书，归还前不能重复借阅', QMessageBox.Ok))
            return

        # 开始更新操作：
        # 更新User表：
        sql = "UPDATE User SET numborrowed = numborrowed + 1 where studentID='%s'" % self.studentId
        query.exec_(sql)
        db.commit()

        # 更新Book表：
        sql = "UPDATE book SET numavai = numavai - 1 where bookID='%s'" %bookId
        query.exec_(sql)
        db.commit()

        # 向borrow表中插入一条记录：
        # 设置借书时间为当前时间，还书时间为3月后
        now = QDate.currentDate()
        date = now.toString(Qt.ISODate)
        future = now.addMonths(3)
        futuredate = future.toString(Qt.ISODate)

        sql = "Insert into borrow Values('%s', '%s', '%s', '%s', '%s' )" %(self.studentId, bookId, borrowId, date, futuredate)
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "借阅成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.borrow_book_success_signal.emit()
        self.close()
        return

    def bookIdEditChanged(self):
        bookId = self.bookIdEdit.text()
        if bookId =='':
            self.bookNameEdit.clear()
            self.authNameEdit.clear()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * from book where bookID='%s'" %bookId
        query.exec_(sql)
        if query.next():
            self.bookNameEdit.setText(query.value(0))
            self.authNameEdit.setText(query.value(2))
            self.categoryComboBox.setCurrentText(query.value(3))
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = borrowBookDialog("12345678")
    mainMindow.show()
    sys.exit(app.exec_())


















