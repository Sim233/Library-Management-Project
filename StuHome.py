import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sip
import qdarkstyle
from bookStorageViewer import BookStorageViewer
from borrowBookDialog import borrowBookDialog
from returnBookDialog import returnBookDialog
from BorrowStatusViewer import BorrowStatusViewer
from bookCateCount import bookCateCountViewer
from BookDetail import BookDetail, BookDetailSearch


class StudentHome(QWidget):
    def __init__(self, studentId):
        super().__init__()
        self.StudentId = studentId
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        # 总布局
        self.layout = QHBoxLayout(self)
        # 按钮布局
        self.buttonLayout = QVBoxLayout()
        # 按钮
        self.borrowBookButton = QPushButton("借书")
        self.returnBookButton = QPushButton("还书")
        self.myBookStatus = QPushButton("借阅状态")
        self.bookDetailButton = QPushButton("书籍详情")
        self.allBookButton = QPushButton("所有书籍")
        self.bookCateCountButton = QPushButton("书籍统计")

        self.buttonLayout.addWidget(self.borrowBookButton)
        self.buttonLayout.addWidget(self.returnBookButton)
        self.buttonLayout.addWidget(self.myBookStatus)
        self.buttonLayout.addWidget(self.bookCateCountButton)
        self.buttonLayout.addWidget(self.allBookButton)
        self.buttonLayout.addWidget(self.bookDetailButton)

        self.borrowBookButton.setFixedWidth(100)
        self.borrowBookButton.setFixedHeight(42)
        self.returnBookButton.setFixedWidth(100)
        self.returnBookButton.setFixedHeight(42)
        self.myBookStatus.setFixedWidth(100)
        self.myBookStatus.setFixedHeight(42)
        self.bookDetailButton.setFixedWidth(100)
        self.bookDetailButton.setFixedHeight(42)
        self.allBookButton.setFixedWidth(100)
        self.allBookButton.setFixedHeight(42)
        self.bookCateCountButton.setFixedWidth(100)
        self.bookCateCountButton.setFixedHeight(42)
        font = QFont()
        font.setPixelSize(16)
        self.borrowBookButton.setFont(font)
        self.returnBookButton.setFont(font)
        self.myBookStatus.setFont(font)
        self.bookDetailButton.setFont(font)
        self.allBookButton.setFont(font)
        self.bookCateCountButton.setFont(font)

        self.storageView = BookStorageViewer()
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.bookCateCountView = bookCateCountViewer()
        self.allBookButton.setEnabled(False)

        self.layout.addLayout(self.buttonLayout)
        self.layout.addWidget(self.storageView)
        self.borrowBookButton.clicked.connect(self.borrowBookButtonClicked)
        self.returnBookButton.clicked.connect(self.returnBookButtonClicked)
        self.bookCateCountButton.clicked.connect(self.bookCateCountButtonClicked)
        self.myBookStatus.clicked.connect(self.myBookStatusClicked)
        self.bookDetailButton.clicked.connect(self.bookDetailButtonClicked)
        self.allBookButton.clicked.connect(self.allBookButtonClicked)

    def borrowBookButtonClicked(self):
        borrowDialog = borrowBookDialog(self.StudentId, self)
        borrowDialog.borrow_book_success_signal.connect(self.borrowStatusView.borrowedQuery)
        borrowDialog.borrow_book_success_signal.connect(self.storageView.searchButtonClicked)
        borrowDialog.show()
        borrowDialog.exec_()
        return

    def returnBookButtonClicked(self):
        returnDialog = returnBookDialog(self.StudentId, self)
        returnDialog.return_book_success_signal.connect(self.borrowStatusView.borrowedQuery)
        returnDialog.return_book_success_signal.connect(self.storageView.searchButtonClicked)
        returnDialog.show()
        returnDialog.exec_()
        return

    def bookDetailButtonClicked(self):
        bookDetailDialog = BookDetailSearch(self.StudentId)
        bookDetailDialog.show()
        bookDetailDialog.exec_()
        return

    def myBookStatusClicked(self):
        self.layout.removeWidget(self.storageView)
        sip.delete(self.storageView)
        self.layout.removeWidget(self.bookCateCountView)
        sip.delete(self.bookCateCountView)
        self.storageView = BookStorageViewer()
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.bookCateCountView = bookCateCountViewer()
        self.layout.addWidget(self.borrowStatusView)
        self.allBookButton.setEnabled(True)
        self.myBookStatus.setEnabled(False)
        self.bookCateCountButton.setEnabled(True)
        return

    def allBookButtonClicked(self):
        self.layout.removeWidget(self.borrowStatusView)
        sip.delete(self.borrowStatusView)
        self.layout.removeWidget(self.bookCateCountView)
        sip.delete(self.bookCateCountView)
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.storageView = BookStorageViewer()
        self.bookCateCountView = bookCateCountViewer()
        self.layout.addWidget(self.storageView)
        self.allBookButton.setEnabled(False)
        self.myBookStatus.setEnabled(True)
        self.bookCateCountButton.setEnabled(True)
        return

    def bookCateCountButtonClicked(self):
        self.layout.removeWidget(self.storageView)
        sip.delete(self.storageView)
        self.layout.removeWidget(self.borrowStatusView)
        sip.delete(self.borrowStatusView)
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.storageView = BookStorageViewer()
        self.bookCateCountView = bookCateCountViewer()
        self.layout.addWidget(self.bookCateCountView)
        self.bookCateCountButton.setEnabled(False)
        self.myBookStatus.setEnabled(True)
        self.allBookButton.setEnabled(True)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = StudentHome("12345678")
    mainWindow.show()
    sys.exit(app.exec_())
