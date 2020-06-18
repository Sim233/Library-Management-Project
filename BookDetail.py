import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *


class BookDetail(QDialog):
    def __init__(self, StudentId, bookId):
        super(BookDetail, self).__init__()
        self.StudentId = StudentId
        self.bookId = bookId
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("书籍详情")
        self.setUpUI()

    def setUpUI(self):
        self.resize(600, 700)
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.DialogLabel = QLabel('书籍详情')
        font1 = QFont()
        font1.setPixelSize(24)
        self.DialogLabel.setFont(font1)
        self.DialogLabel.setFixedHeight(40)
        self.layout.addRow(self.DialogLabel)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * from book where bookID='%s' " % self.bookId
        query.exec_(sql)
        if not query.next():
            print(QMessageBox.warning(self, "警告", "您查询的书不存在，请查看输入", QMessageBox.Ok))
            self.close()
            return

        font2 = QFont()
        font2.setPixelSize(20)
        self.bookIDLabel = QLabel('书籍编号')
        self.bookIDLine = QLabel(query.value(0))
        self.bookIDLabel.setFont(font2)
        self.bookIDLine.setFont(font2)
        self.bookIDLabel.setFixedHeight(32)
        self.layout.addRow(self.bookIDLabel, self.bookIDLine)

        self.bookNameLabel = QLabel('书籍名称')
        self.bookNameLine = QLabel(query.value(1))
        self.bookNameLabel.setFont(font2)
        self.bookNameLine.setFont(font2)
        self.bookNameLabel.setFixedHeight(32)
        self.layout.addRow(self.bookNameLabel, self.bookNameLine)
        self.bookAurLabel = QLabel('书籍作者')
        self.bookAurLine = QLabel(query.value(2))
        self.bookAurLabel.setFont(font2)
        self.bookAurLine.setFont(font2)
        self.bookAurLabel.setFixedHeight(32)
        self.layout.addRow(self.bookAurLabel, self.bookAurLine)
        self.bookCateLabel = QLabel('书籍类别')
        self.bookCateLine = QLabel(query.value(3))
        self.bookCateLabel.setFont(font2)
        self.bookCateLine.setFont(font2)
        self.bookCateLabel.setFixedHeight(32)
        self.layout.addRow(self.bookCateLabel, self.bookCateLine)
        self.bookStoreLabel = QLabel('馆藏本数')
        self.bookStoreLine = QLabel(str(query.value(4)))
        self.bookStoreLabel.setFont(font2)
        self.bookStoreLine.setFont(font2)
        self.bookStoreLabel.setFixedHeight(32)
        self.layout.addRow(self.bookStoreLabel, self.bookStoreLine)
        self.bookAvaiLabel = QLabel('在架本数')
        self.bookAvaiLine = QLabel(str(query.value(5)))
        self.bookAvaiLabel.setFont(font2)
        self.bookAvaiLine.setFont(font2)
        self.bookAvaiLabel.setFixedHeight(32)
        self.layout.addRow(self.bookAvaiLabel, self.bookAvaiLine)

        font3 = QFont()
        font3.setPixelSize(18)
        self.CommentTitle = QLabel('添加评论...')
        self.CommentTitle.setFont(font1)
        self.bookIDLabel.setFixedHeight(40)
        self.layout.addRow(self.CommentTitle)
        self.CommentEdit = QTextEdit()
        self.CommentEdit.setFont(font3)
        self.CommentEdit.setFixedHeight(125)
        self.layout.addRow(self.CommentEdit)

        self.CommentButton = QPushButton('提交评论')
        self.CommentButton.setFixedWidth(140)
        self.CommentButton.setFixedHeight(32)
        self.layout.addRow(self.CommentButton)
        self.CommentButton.clicked.connect(self.CommentButtonClicked)
        # todo: function clicked and insert and reload

        self.CommentTitle = QLabel('书籍评论')
        self.CommentTitle.setFont(font1)
        self.bookIDLabel.setFixedHeight(40)
        self.layout.addRow(self.CommentTitle)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()
        sql = "select user.userName, comment.comContent from user inner join comment on user.userID = comment.userID " \
              "where comment.bookID ='%s'" % self.bookId
        query.exec_(sql)
        self.CommentNameLabel = []
        self.CommentLabel = []
        self.CommentCount = 0
        while query.next():
            self.CommentNameLabel.append(QLabel(query.value(0)))
            self.CommentNameLabel[self.CommentCount].setFixedHeight(64)
            self.CommentNameLabel[self.CommentCount].setFont(font3)
            self.CommentLabel.append(QLabel(query.value(1)))
            self.CommentLabel[self.CommentCount].setFont(font3)
            self.CommentLabel[self.CommentCount].setWordWrap(True)
            self.layout.addRow(self.CommentNameLabel[self.CommentCount], self.CommentLabel[self.CommentCount])
            self.CommentCount += 1

    def CommentButtonClicked(self):
        comment = self.CommentEdit.toPlainText()
        commentID = self.StudentId + self.bookId
        # 禁止空评论
        if comment == "":
            print(QMessageBox.warning(self, "警告", "输入评论为空，请检查输入", QMessageBox.Ok))
            return
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()

        # 检查是否已经评论
        sql = "SELECT * from comment where commentID='%s'" % commentID
        query.exec_(sql)
        if query.next():
            print(QMessageBox.warning(self, "警告", "您已对此书作出过评论", QMessageBox.Ok))
            return
        sql = "INSERT INTO comment values ('%s', '%s', '%s', '%s')" % (self.bookId, self.StudentId, commentID, comment)
        query.exec_(sql)
        db.commit()
        self.CommentEdit.clear()
        BookDetail(self.StudentId, self.bookId)
        self.close()


class BookDetailSearch(QDialog):
    def __init__(self, StudentId):
        super(BookDetailSearch, self).__init__()
        self.StudentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("查询书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["哲学", "数学", "物理学", "化学", "政治", "社会学", "法律", "军事", "经济学", "教育", "体育", "文学",
                        "艺术", "历史", "地理", "天文学", "生物学", "医学卫生", "农业", "计算机", "工程技术", "心理学"]

        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.SearchLabel = QLabel('查询书籍')
        self.layout.addRow('', self.SearchLabel)

        # 表单结构
        # 借阅人学号
        # 借阅书籍书号
        self.userLable = QLabel('查询人学号')
        self.uerEdit = QLabel(self.StudentId)
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

        self.SearchBookButton = QPushButton('查看详情')
        self.SearchBookButton.setFixedWidth(140)
        self.SearchBookButton.setFixedHeight(32)
        self.layout.addRow('', self.SearchBookButton)

        self.SearchLabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.SearchBookButton.clicked.connect(self.SearchButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.bookIdEdit.returnPressed.connect(self.SearchButtonClicked)

    def SearchButtonClicked(self):
        bookId = self.bookIdEdit.text()
        if bookId == "":
            print(QMessageBox.warning(self, "警告", "索书号不能为空，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * from book where bookID='%s' " % bookId
        query.exec_(sql)
        if not query.next():
            print(QMessageBox.warning(self, "警告", "您查询的书不存在，请查看输入", QMessageBox.Ok))
            return
        self.close()
        BookDetailDialog = BookDetail(self.StudentId, bookId)
        BookDetailDialog.show()
        BookDetailDialog.exec_()
        return

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
    mainWindow = BookDetailSearch('43211234')
    mainWindow.show()
    sys.exit(app.exec_())
