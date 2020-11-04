# coding=utf8
import sys
import os

import dayu_widgets
from dayu_widgets.dock_widget import MDockWidget
from dayu_widgets import MTextEdit, MLineEdit, MPushButton, MLabel, MDivider, MCarousel, MTreeView, MToolButtonGroup, \
    dayu_theme, MToolButton
from dayu_widgets.qt import *
from PySide import QtCore


class LoginWindow(QWidget):
    DEFAULT_HEAD_PATH = os.path.join(os.path.abspath('..'), r"img\defaulthead.jpg")
    ICON_PATH = os.path.join(os.path.abspath('..'), r"img\LOGO1.png")
    login_signal = QtCore.Signal(str)

    def __init__(self):
        super(LoginWindow, self).__init__()
        # 初始化变量
        self.user_num = ""

        # 初始化控件
        self.icon_logo = None
        self.main_lay = None
        self.lay_H = None
        self.lay_H1 = None
        self.lay_H2 = None
        self.lay_H3 = None

        self.label_head = None
        self.label_account = None
        self.lineEdit_account = None
        self.label_password = None
        self.lineEdit_password = None

        self.btn_login = None
        self.btn_register = None
        self.btn_forget = None

        self.construct_ui()
        self.resize_default()
        self.set_func_connect()

    def construct_ui(self):
        self.setWindowTitle(u"登录")
        self.icon_logo = QIcon(QIcon(self.ICON_PATH))
        self.setWindowIcon(self.icon_logo)

        # Layout
        self.main_lay = QVBoxLayout()
        self.lay_H = QHBoxLayout()
        self.lay_H1 = QHBoxLayout()
        self.lay_H2 = QHBoxLayout()
        self.lay_H3 = QHBoxLayout()

        self.label_head = MLabel()
        self.label_head.setPixmap(self.DEFAULT_HEAD_PATH)
        self.label_head.setMinimumSize(100, 100)
        self.label_head.setMaximumSize(100, 100)
        self.lay_H.addStretch()
        self.lay_H.addWidget(self.label_head)
        self.lay_H.addStretch()
        self.main_lay.addLayout(self.lay_H)

        self.label_account = MLabel(u"账号")
        self.lineEdit_account = MLineEdit()
        self.lay_H1.addWidget(self.label_account)
        self.lay_H1.addWidget(self.lineEdit_account)
        self.label_password = MLabel(u"密码")
        self.lineEdit_password = MLineEdit()
        self.lay_H2.addWidget(self.label_password)
        self.lay_H2.addWidget(self.lineEdit_password)

        self.btn_login = MPushButton(u"登录")
        self.btn_register = MPushButton(u"注册")
        self.btn_forget = MPushButton(u"忘记密码")
        self.lay_H3.addWidget(self.btn_login)
        self.lay_H3.addWidget(self.btn_register)
        self.lay_H3.addWidget(self.btn_forget)

        self.main_lay.addLayout(self.lay_H1)
        self.main_lay.addLayout(self.lay_H2)
        self.main_lay.addLayout(self.lay_H3)

        self.setLayout(self.main_lay)

    def resize_default(self):
        self.setGeometry((1920 - 800) / 2, (1080 - 600) / 2, 300, 350)

    def set_func_connect(self):
        self.btn_login.clicked.connect(self.btn_login_clicked)

    def get_input_message(self):
        pass

    def btn_login_clicked(self):
        if judge_password("13670892740", "123456"):
            self.login_signal_emit()

    def login_signal_emit(self):
        self.login_signal.emit(self.user_num)
        self.close()


def judge_password(user_num, input_password):
    return True