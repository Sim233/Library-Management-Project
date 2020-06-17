import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *


class dropBookDialog(QDialog):
    drop_book_success_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(dropBookDialog, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("删除书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["哲学", "数学", "物理学", "化学", "政治", "社会学", "法律", "军事", "经济学", "教育", "体育", "文学",
                        "艺术", "历史", "地理", "天文学", "生物学", "医学卫生", "农业", "计算机", "工程技术", "心理学"]

        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.dropLabel = QLabel('删除书籍')
        self.layout.addRow('', self.dropLabel)

        # 表单结构
        # 借阅人学号
        # 借阅书籍书号
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

        self.dropBookButton = QPushButton('确认删除')
        self.dropBookButton.setFixedWidth(140)
        self.dropBookButton.setFixedHeight(32)
        self.layout.addRow('', self.dropBookButton)

        self.dropLabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.dropBookButton.clicked.connect(self.dropButtonClicked)
        self.bookIdEdit.returnPressed.connect(self.dropButtonClicked)

    def dropButtonClicked(self):
        # 更新book表中numavai，user表中numborrowed， borrow表中插入借书记录
        bookID = self.bookIdEdit.text()
        # 字符串拼接的方式来实现借书操作的Id号
        # 如果索书号为空
        if bookID == "":
            print(QMessageBox.warning(self, "警告", "索书号不能为空，请查看输入", QMessageBox.Ok))
            return
        # 打开数据库进行操作
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()

        #根据索书号进行查询：
        sql = "SELECT * from book where bookID='%s' " % bookID
        query.exec_(sql)
        if not query.next():
            print(QMessageBox.warning(self, "警告", "你所要删除的书不存在，请查看输入", QMessageBox.Ok))
            return
        elif query.value(5) != query.value(4):
            print(QMessageBox.information(self, "警告", "本书有在外未归还的书籍，请归还后再操作", QMessageBox.Ok))
            return

        # 开始删除操作：
        # 删除book表：
        sql = "DELETE from book where bookID='%s'" % bookID
        query.exec_(sql)
        db.commit()
        sql = "DELETE from comment where bookID='%s'" % bookID
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "删除书籍成功!", QMessageBox.Yes, QMessageBox.Yes))

        self.drop_book_success_signal.emit()
        self.close()
        return

    def bookIdEditChanged(self):
        bookID = self.bookIdEdit.text()
        if bookID == '':
            self.bookNameEdit.clear()
            self.authNameEdit.clear()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * from book where bookID='%s'" % bookID
        query.exec_(sql)
        if query.next():
            self.bookNameEdit.setText(query.value(1))
            self.authNameEdit.setText(query.value(2))
            self.categoryComboBox.setCurrentText(query.value(3))
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = dropBookDialog()
    mainWindow.show()
    sys.exit(app.exec_())
