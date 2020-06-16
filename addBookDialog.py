import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *

class addBookDialog(QDialog):
    # 一个对话类，实现对于书籍信息的输入
    add_book_success_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(addBookDialog, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        # 在运行这个弹窗时，禁止父窗口的响应
        self.setWindowTitle("添加书籍")

    def setUpUI(self):
        self.resize(1000, 800)
        # 设置窗口为垂直布局
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # 设置标题样式
        self.DialogLabel = QLabel('书籍添加')

        font = QFont()
        font.setPixelSize(20)
        self.DialogLabel.setFont(font)

        self.layout.addRow('', self.DialogLabel)

        # 表单式布局

        # 开始设定输入内容
        # 书籍名称
        # 书籍编号(8位)
        # 书籍分类（哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类）
        # 书籍录入本数

        bookCategory =["哲学", "物理学","政治", "法律", "军事", "经济", "文化", "教育", "体育", "语言文字", "艺术", "历史"
            , "地理", "天文学", "生物学", "医学卫生", "农业"]

        self.bookNameLabel = QLabel('书籍名称')
        self.bookNameLineEdit = QLineEdit()
        self.bookNameLineEdit.setMaxLength(20)
        self.bookNameLineEdit.setFixedHeight(32)
        self.bookNameLineEdit.setFixedWidth(180)
        self.layout.addRow(self.bookNameLabel, self.bookNameLineEdit)

        self.bookIDLabel = QLabel('书籍编号')
        self.bookIDLineEdit = QLineEdit()
        self.bookIDLineEdit.setMaxLength(8)
        self.layout.addRow(self.bookIDLabel, self.bookIDLineEdit)

        self.bookaurLabel = QLabel('书籍作者')
        self.bookaurLineEdit = QLineEdit()
        self.bookaurLineEdit.setMaxLength(10)
        self.layout.addRow(self.bookaurLabel, self.bookaurLineEdit)

        self.bookCateLabel = QLabel('书籍分类')
        self.bookBox = QComboBox()
        self.bookBox.addItems(bookCategory)
        self.layout.addRow(self.bookCateLabel, self.bookBox)
        # 将书籍种类设置为下拉菜单选择形式

        self.bookNumLabel = QLabel('新增本数')
        self.bookNumLineEdit = QLineEdit()
        self.bookNumLineEdit.setMaxLength(3)
        self.bookNumLineEdit.setValidator(QIntValidator())
        self.layout.addRow(self.bookNumLabel, self.bookNumLineEdit)


        # 设置按钮
        self.addBookButton = QPushButton('添加')
        self.addBookButton.setFixedHeight(32)
        self.addBookButton.setFixedWidth(140)
        self.layout.addRow('', self.addBookButton)

        # 设置间距
        #self.DialogLabel.setMargin(8)
        #self.layout.setVerticalSpacing(10)

        # 设置动作
        self.addBookButton.clicked.connect(self.addBookButtonClicked)

    def addBookButtonClicked(self):
        bookName = self.bookNameLineEdit.text()
        bookID = self.bookIDLineEdit.text()
        bookCate = self.bookBox.currentText()
        bookNum = self.bookNumLineEdit.text()
        bookaur = self.bookaurLineEdit.text()
        if(bookName == '' or bookID == '' or bookCate == '' or bookNum == '' or bookaur == ''):
            print(QMessageBox.warning(self, '警告', '字段不能为空', QMessageBox.Ok))
        else:
            bookNum = int(bookNum)
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./library.db')
            if(db.open()):
                print('成功')
            else:
                print('失败')
            query = QSqlQuery()
            sql = "SELECT * FROM book WHERE bookID='%s'" % (bookID)
            query.exec_(sql)
            if (query.next()):
                sql = "UPDATE book SET numstore=numstore+%d,numavai=numavai+%d WHERE bookID='%s'" % (bookNum, bookNum, bookID)
                print('旧书')
            else:
                sql = "Insert into book Values ('%s', '%s', '%s','%s', '%d', '%d')"%(
                    bookName, bookID, bookaur, bookCate, bookNum, bookNum
                )
                print('新书')
            query.exec_(sql)
            db.commit()
            print(QMessageBox.information(self, '提示', '添加书籍信息成功！', QMessageBox.Ok))
            self.add_book_success_signal.emit()
            self.close()
            self.clearEdit()
        return
    def clearEdit(self):
        self.bookNameLineEdit.clear()
        self.bookIDLineEdit.clear()
        self.bookNumLineEdit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = addBookDialog()
    mainMindow.show()
    sys.exit(app.exec_())






















