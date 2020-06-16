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
        BookCategory = ["哲学", "物理学","政治", "法律", "军事", "经济", "文化", "教育", "体育", "语言文字", "艺术", "历史"
            , "地理", "天文学", "生物学", "医学卫生", "农业"]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

