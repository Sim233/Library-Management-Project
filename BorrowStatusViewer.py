import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *


class BorrowStatusViewer(QWidget):
    def __init__(self, studentId):
        super(BorrowStatusViewer, self).__init__()
        self.resize(700, 500)
        self.studentId = studentId
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./library.db')
        self.db.open()
        # 分为两块，上方是已借未归还书，下方是已归还书
        self.layout = QVBoxLayout(self)
        # Label设置
        self.borrowedLabel = QLabel("未归还:")
        self.returnedLabel = QLabel("已归还:")
        self.borrowedLabel.setFixedHeight(32)
        self.borrowedLabel.setFixedWidth(60)


        # Table和Model
        self.borrowedTableView = QTableView()
        self.borrowedTableView.horizontalHeader().setStretchLastSection(True)
        self.borrowedTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.borrowedTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.borrowedQueryModel = QSqlQueryModel()
        self.borrowedTableView.setModel(self.borrowedQueryModel)
        self.borrowedQuery()
        self.borrowedQueryModel.setHeaderData(0, Qt.Horizontal, "书名")
        self.borrowedQueryModel.setHeaderData(1, Qt.Horizontal, "书号")
        self.borrowedQueryModel.setHeaderData(2, Qt.Horizontal, "作者")
        self.borrowedQueryModel.setHeaderData(3, Qt.Horizontal, "分类")
        self.borrowedQueryModel.setHeaderData(4, Qt.Horizontal, "借出时间")
        self.borrowedQueryModel.setHeaderData(5, Qt.Horizontal, "应还时间")


        self.layout.addWidget(self.borrowedLabel)
        self.layout.addWidget(self.borrowedTableView)
        return

    def borrowedQuery(self):
        sql = "SELECT Book.bookName,Book.bookId,book.bookaur,book.bookcate,borrow.borrowtime,borrow.returntime FROM Book,borrow WHERE Book.BookId=borrow.bookID AND borrow.student_ID='%s'" % self.studentId
        self.borrowedQueryModel.setQuery(sql)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BorrowStatusViewer("12345678")
    mainMindow.show()
    sys.exit(app.exec_())