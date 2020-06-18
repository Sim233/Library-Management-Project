import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *

class returnBookDialog(QDialog):
    return_book_success_signal = pyqtSignal()

    def __init__(self, StudentId, parent=None):
        super(returnBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("归还书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类
        BookCategory = ["哲学", "数学", "物理学", "化学", "政治", "社会学", "法律", "军事", "经济学", "教育", "体育", "文学",
                        "艺术", "历史", "地理", "天文学", "生物学", "医学卫生", "农业", "计算机", "工程技术", "心理学"]

        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.returnLabel = QLabel('归还书籍')
        self.layout.addRow('', self.returnLabel)

        # 表单结构
        # 归还人学号
        # 归还书籍书号
        self.userLable = QLabel('借阅人学号')
        self.uerEdit = QLabel(self.studentId)
        self.layout.addRow(self.userLable, self.uerEdit)

        self.bookIdLabel = QLabel('索书号')
        self.bookIdEdit = QLineEdit()
        self.bookIdEdit.setMaxLength(10)
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

        self.returnBookButton = QPushButton('确认归还')
        self.returnBookButton.setFixedWidth(140)
        self.returnBookButton.setFixedHeight(32)
        self.layout.addRow('', self.returnBookButton)

        self.returnLabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.returnBookButton.clicked.connect(self.returnButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.bookIdEdit.returnPressed.connect(self.returnButtonClicked)

    def returnButtonClicked(self):
        bookId = self.bookIdEdit.text()
        returnId = self.studentId + bookId
        # 索书号为空时设置提示
        if bookId == '':
            print(QMessageBox.warning(self, '警告', '索书号不能为空，请查看输入', QMessageBox.Ok))
            return

        # 打开数据库进行操作
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()

        # 根据索书号进行查询：
        sql = "SELECT * from book where bookID='%s'" % bookId
        query.exec_(sql)
        if not query.next():
            print(QMessageBox.warning(self, "警告", "你所要借的书不存在，请查看输入", QMessageBox.Ok))
            return

        # 检查是否借书
        sql = "SELECT * from borrow where identiID = '%s'" % returnId
        query.exec_(sql)
        if not query.next():
            print(QMessageBox.warning(self, '提示', '您并未借阅这本书，请检查输入', QMessageBox.Ok))
            return

        # 更新操作
        # 更新user
        sql = "UPDATE user SET numborrowed = numborrowed - 1 where userID = '%s'" % self.studentId
        query.exec_(sql)
        db.commit()

        # 更新book
        sql = "UPDATE book SET numavai = numavai + 1 where bookID = '%s'" % bookId
        query.exec_(sql)
        db.commit()

        # 在borrow表中删除借书目录
        sql = "DELETE from borrow where identiID = '%s'" % returnId
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "归还成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.return_book_success_signal.emit()
        self.close()
        return  # todo: 提示写书评

    def bookIdEditChanged(self):
        bookId = self.bookIdEdit.text()
        if bookId == '':
            self.bookNameEdit.clear()
            self.authNameEdit.clear()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * from book where bookID='%s'" % bookId
        query.exec_(sql)
        if query.next():
            self.bookNameEdit.setText(query.value(1))
            self.authNameEdit.setText(query.value(2))
            self.categoryComboBox.setCurrentText(query.value(3))
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = returnBookDialog("12345678")
    mainWindow.show()
    sys.exit(app.exec_())
