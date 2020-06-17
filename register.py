import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib


class SignupWidget(QWidget):
    student_signup_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 生成初始化窗口
        self.resize(900, 600)
        self.setWindowTitle('欢迎登录图书馆管理系统')

        self.signupLabel = QLabel('注册')
        self.signupLabel.setAlignment(Qt.AlignCenter)
        self.signupLabel.setFixedHeight(100)
        # 设置标题居中

        font = QFont()
        font.setPixelSize(36)
        self.signupLabel.setFont(font)
        # 设置标题字号

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.signupLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        # 设置窗口布局，为垂直的绝对布局

        self.formlayout = QFormLayout()
        # 将布局设置为表单形式

        # 开始设定注册内容
        # 用户姓名
        # 用户ID
        # 用户密码
        # 用户身份（学生/老师）
        self.UserIDLabel = QLabel('学    号：')
        self.UserIDLineEdit = QLineEdit()
        self.UserIDLineEdit.setFixedHeight(32)
        self.UserIDLineEdit.setFixedWidth(180)
        self.UserIDLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.UserIDLabel, self.UserIDLineEdit)

        self.UserNameLabel = QLabel('姓    名：')
        self.UserNameLineEdit = QLineEdit()
        self.UserNameLineEdit.setFixedHeight(32)
        self.UserNameLineEdit.setFixedWidth(180)
        self.UserNameLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.UserNameLabel, self.UserNameLineEdit)

        self.UserpasswordLabel = QLabel('密    码：')
        self.UserpasswordLineEdit = QLineEdit()
        self.UserpasswordLineEdit.setFixedHeight(32)
        self.UserpasswordLineEdit.setFixedWidth(180)
        self.UserpasswordLineEdit.setMaxLength(8)
        passwordFont = QFont()
        passwordFont.setPixelSize(10)
        self.UserpasswordLineEdit.setFont(passwordFont)
        self.UserpasswordLineEdit.setEchoMode(QLineEdit.Password)
        self.formlayout.addRow(self.UserpasswordLabel, self.UserpasswordLineEdit)

        self.UserIdentityLabel = QLabel('教师/学生：')
        self.UserIdentityLineEdit = QLineEdit()
        self.UserIdentityLineEdit.setFixedHeight(32)
        self.UserIdentityLineEdit.setFixedWidth(180)
        self.UserIdentityLineEdit.setMaxLength(2)
        self.formlayout.addRow(self.UserIdentityLabel, self.UserIdentityLineEdit)

        self.UserGraduatedLabel = QLabel('是否已毕业：')
        self.UserGraduatedBox = QComboBox()
        self.UserGraduatedBox.addItems(["否", "是"])
        self.formlayout.addRow(self.UserGraduatedLabel, self.UserGraduatedBox)

        # 设置注册按钮
        self.signUpbutton = QPushButton('注册')
        self.signUpbutton.setFixedHeight(30)
        self.signUpbutton.setFixedWidth(120)
        self.formlayout.addRow('', self.signUpbutton)

        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(self.Hlayout)
        self.layout.addWidget(widget, Qt.AlignHCenter)

        #事件响应
        self.signUpbutton.clicked.connect(self.SignUp)
        self.UserNameLineEdit.returnPressed.connect(self.SignUp)
        self.UserIDLineEdit.returnPressed.connect(self.SignUp)
        self.UserpasswordLineEdit.returnPressed.connect(self.SignUp)
        self.UserIdentityLineEdit.returnPressed.connect(self.SignUp)

    def SignUp(self):
        user_id = self.UserIDLineEdit.text()
        user_name = self.UserNameLineEdit.text()
        user_password = self.UserpasswordLineEdit.text()
        user_identity = self.UserIdentityLineEdit.text()
        user_grad_t = self.UserGraduatedBox.currentText()
        if user_identity == '学生':
            user_admin = 0
        elif user_identity == '教师':
            user_admin = 1
        else:
            print(QMessageBox.warning(self,"警告信息", '只能键入“教师”或“学生”，请重新输入！', QMessageBox.Ok))
            return
        if user_grad_t == '是':
            user_grad = 1
        elif user_grad_t == '否':
            user_grad = 0
        else:
            print(QMessageBox.warning(self, "警告信息", '只能键入“是”或“否”，请重新输入！', QMessageBox.Ok))
            return
        # 检查关键信息是否非空
        if (user_id == '' or user_name == '' or user_password == ''):
            print(QMessageBox.warning(self, "警告信息", '关键信息不能为空，请重新输入', QMessageBox.Ok))
            return
        else:
            # 关键信息有效时，连接数据库
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName('./library.db')
            db.open()
            query = QSqlQuery()
            sql = "SELECT * from user where userID = '%s'" % user_id
            query.exec_(sql)
            if (query.next()):
                print(QMessageBox.warning(self, "警告", '该用户ID已注册！', QMessageBox.Ok))
                return
            else:
                sql = "INSERT INTO user values('%s', '%s', '%s', '%d', 0, %d)" %\
                      (user_id, user_name, user_password, user_admin, user_grad)
                db.exec_(sql)
                db.commit()
                print(QMessageBox.information(self, "提醒", '您已注册成功！', QMessageBox.Ok))
                self.student_signup_signal.emit(user_id)
            db.close()
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = SignupWidget()
    mainWindow.show()
    sys.exit(app.exec_())
