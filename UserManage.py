import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip

class UserManage(QDialog):
    def __init__(self,parent=None):
        super(UserManage, self).__init__(parent)
        self.resize(280, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("管理用户")
        # 用户数
        self.userCount = 0
        self.setUpUI()

    def setUpUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./library.db')
        self.db.open()
        self.query = QSqlQuery()
        self.getResult()

        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['学号', '姓名'])
        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.widget = QWidget()
        self.widget.setFixedHeight(48)
        font = QFont()
        font.setPixelSize(15)
        self.layout.addWidget(self.widget, Qt.AlignCenter)
        # 设置信号
        self.tableWidget.itemClicked.connect(self.getStudentInfo)

    def getResult(self):
        sql = "SELECT StudentId,stuName FROM User WHERE IsAdmin=0"
        self.query.exec_(sql)
        self.userCount = 0;
        while (self.query.next()):
            self.userCount += 1;
        sql = "SELECT StudentId,stuName FROM User WHERE IsAdmin=0"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.userCount):
            if (self.query.next()):
                StudentIdItem = QTableWidgetItem(self.query.value(0))
                StudentNameItem = QTableWidgetItem(self.query.value(1))
                StudentIdItem.setFont(font)
                StudentNameItem.setFont(font)
                StudentIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                StudentNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, StudentIdItem)
                self.tableWidget.setItem(i, 1, StudentNameItem)
        return

    def getStudentInfo(self, item):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.getResult()
        i = 0
        while (self.query.next() and i != row):
            i = i + 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = UserManage()
    mainMindow.show()
    sys.exit(app.exec_())