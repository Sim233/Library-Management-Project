import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import sip
from addBookDialog import addBookDialog
from dropBookDialog import dropBookDialog
from bookStorageViewer import BookStorageViewer
from UserManage import UserManage, OverdueUserManage
from bookCateCount import bookCateCountViewer
from BookDetail import BookDetail, BookDetailSearch


class AdminHome(QWidget):
    def __init__(self, AdminId):
        super().__init__()
        self.StudentId = AdminId
        self.setUpUI()

    def setUpUI(self):
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.layout = QHBoxLayout()
        self.buttonlayout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setPixelSize(16)
        self.userManageButton = QPushButton("用户管理")
        self.addBookButton = QPushButton("添加书籍")
        self.dropBookButton = QPushButton("淘汰书籍")
        self.bookDetailButton = QPushButton("书籍详情")
        self.overdueUserButton = QPushButton("逾期用户")
        self.allBookButton = QPushButton("所有书籍")
        self.bookCateCountButton = QPushButton("书籍统计")

        self.userManageButton.setFont(font)
        self.addBookButton.setFont(font)
        self.dropBookButton.setFont(font)
        self.bookDetailButton.setFont(font)
        self.overdueUserButton.setFont(font)
        self.bookCateCountButton.setFont(font)
        self.allBookButton.setFont(font)
        self.userManageButton.setFixedWidth(100)
        self.userManageButton.setFixedHeight(42)
        self.addBookButton.setFixedWidth(100)
        self.addBookButton.setFixedHeight(42)
        self.dropBookButton.setFixedWidth(100)
        self.dropBookButton.setFixedHeight(42)
        self.bookDetailButton.setFixedWidth(100)
        self.bookDetailButton.setFixedHeight(42)
        self.overdueUserButton.setFixedWidth(100)
        self.overdueUserButton.setFixedHeight(42)
        self.bookCateCountButton.setFixedWidth(100)
        self.bookCateCountButton.setFixedHeight(42)
        self.allBookButton.setFixedWidth(100)
        self.allBookButton.setFixedHeight(42)
        self.buttonlayout.addWidget(self.addBookButton)
        self.buttonlayout.addWidget(self.dropBookButton)
        self.buttonlayout.addWidget(self.bookDetailButton)
        self.buttonlayout.addWidget(self.bookCateCountButton)
        self.buttonlayout.addWidget(self.allBookButton)
        self.buttonlayout.addWidget(self.userManageButton)
        self.buttonlayout.addWidget(self.overdueUserButton)
        self.layout.addLayout(self.buttonlayout)
        self.storageView = BookStorageViewer()
        self.bookCateCountView = bookCateCountViewer()
        self.layout.addWidget(self.storageView)
        self.allBookButton.setEnabled(False)

        self.addBookButton.clicked.connect(self.addBookButtonClicked)
        self.dropBookButton.clicked.connect(self.dropBookButtonClicked)
        self.bookDetailButton.clicked.connect(self.bookDetailButtonClicked)
        self.bookCateCountButton.clicked.connect(self.bookCateCountButtonClicked)
        self.allBookButton.clicked.connect(self.allBookButtonClicked)
        self.userManageButton.clicked.connect(self.userManage)
        self.overdueUserButton.clicked.connect(self.overdueUserManage)

    def addBookButtonClicked(self):
        addDialog = addBookDialog(self)
        addDialog.add_book_success_signal.connect(self.storageView.searchButtonClicked)
        addDialog.show()
        addDialog.exec_()

    def dropBookButtonClicked(self):
        dropDialog = dropBookDialog(self)
        dropDialog.drop_book_success_signal.connect(self.storageView.searchButtonClicked)
        dropDialog.show()
        dropDialog.exec_()

    def bookDetailButtonClicked(self):
        bookDetailDialog = BookDetailSearch(self.StudentId)
        bookDetailDialog.show()
        bookDetailDialog.exec_()
        return

    def bookCateCountButtonClicked(self):
        self.layout.removeWidget(self.storageView)
        sip.delete(self.storageView)
        self.storageView = BookStorageViewer()
        self.bookCateCountView = bookCateCountViewer()
        self.layout.addWidget(self.bookCateCountView)
        self.bookCateCountButton.setEnabled(False)
        self.allBookButton.setEnabled(True)
        return

    def allBookButtonClicked(self):
        self.layout.removeWidget(self.bookCateCountView)
        sip.delete(self.bookCateCountView)
        self.bookCateCountView = bookCateCountViewer()
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)
        self.allBookButton.setEnabled(False)
        self.bookCateCountButton.setEnabled(True)
        return

    def userManage(self):
        UserDelete = UserManage(self)
        UserDelete.show()
        UserDelete.exec_()

    def overdueUserManage(self):
        overdueUserDialog = OverdueUserManage(self)
        overdueUserDialog.show()
        overdueUserDialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = AdminHome()
    mainWindow.show()
    sys.exit(app.exec_())
