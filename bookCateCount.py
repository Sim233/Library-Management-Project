import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import matplotlib.pyplot as plt
import sip

class bookCateCountViewer(QWidget):
    def __init__(self):
        super(bookCateCountViewer, self).__init__()
        self.resize(700, 500)
        self.setWindowTitle("欢迎使用图书馆管理系统")

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./library.db')
        db.open()
        query = QSqlQuery()
        sql = "select bookCategory, count(bookName) from book group by bookCategory order by count(bookName) desc"
        query.exec_(sql)
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']
        label_list = []
        count_list = []
        while query.next():
            label_list.append(query.value(0))
            count_list.append(query.value(1))
        explod = [0 for item in label_list]
        explod[0] += 0.1
        explode = tuple(explod)
        fig1, ax1 = plt.subplots()
        ax1.pie(count_list, explode=explode, labels=label_list, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        plt.savefig('./CateCount.jpg')

        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.CateCountLabel = QLabel("馆藏各类书籍的种数")
        font = QFont()
        font.setPixelSize(24)
        self.CateCountLabel.setFont(font)
        self.CateCountLabel.setAlignment(Qt.AlignCenter)
        self.layout.addRow('', self.CateCountLabel)

        self.PicLabel = QLabel()
        self.PicLabel.setPixmap(QPixmap('./CateCount.jpg'))
        self.PicLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.PicLabel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = bookCateCountViewer()
    mainWindow.show()
    sys.exit(app.exec_())
