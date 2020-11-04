# coding=utf8
import sys
import os

import dayu_widgets
from dayu_widgets.dock_widget import MDockWidget
from dayu_widgets import MTextEdit, MLineEdit, MPushButton, MLabel, MDivider, MCarousel, MTreeView, MToolButtonGroup, \
    dayu_theme, MToolButton, MMessage
from dayu_widgets.qt import *
import functools
from PySide import QtCore

from ConnectDataBase import mydb


class RegisterWindow(QWidget):
    DEFAULT_HEAD_PATH = os.path.join(os.path.abspath('..'), r"img\defaulthead.jpg")
    ICON_PATH = os.path.join(os.path.abspath('..'), r"img\LOGO1.png")
    notenough_signal = QtCore.Signal()

    def __init__(self):
        super(RegisterWindow, self).__init__()
        # 初始化控件
        self.icon_logo = None
        self.main_lay = None

        self.btn_head = None
        self.label_userName = None
        self.lineEdit_userName = None
        self.label_password = None
        self.lineEdit_password = None
        self.label_realName = None
        self.lineEdit_realName = None
        self.label_IDNum = None
        self.lineEdit_IDNum = None
        self.label_occupation = None
        self.lineEdit_occupation = None
        self.label_education = None
        self.lineEdit_education = None
        self.btn_confirm = None

        # 初始化变量
        self.username = ""
        self.userID = ""
        self.realname = ""
        self.job = ""
        self.password = ""
        self.education = ""

        self.construct_ui()
        self.resize_default()
        self.set_func_connect()

    def construct_ui(self):
        self.setWindowTitle(u"注册")
        self.icon_logo = QIcon(QIcon(self.ICON_PATH))
        self.setWindowIcon(self.icon_logo)

        # Layout
        self.main_lay = QVBoxLayout()

        icon = QIcon(self.DEFAULT_HEAD_PATH)
        self.btn_head = QPushButton()
        self.btn_head.setIcon(icon)
        self.btn_head.setStyleSheet("border:None")
        self.btn_head.setMinimumSize(100, 100)
        self.btn_head.setMaximumSize(100, 100)
        self.btn_head.setIconSize(QSize(100, 100))
        self.set_widget_layout(self.btn_head)

        self.label_userName = MLabel(u"用户名:")
        self.label_userName.setMinimumWidth(90)
        self.lineEdit_userName = MLineEdit()
        self.set_widget_layout(self.label_userName, self.lineEdit_userName)

        self.label_password = MLabel(u"密码:")
        self.label_password.setMinimumWidth(90)
        self.lineEdit_password = MLineEdit()
        self.set_widget_layout(self.label_password, self.lineEdit_password)

        self.label_realName = MLabel(u"真实姓名:")
        self.label_realName.setMinimumWidth(90)
        self.lineEdit_realName = MLineEdit()
        self.set_widget_layout(self.label_realName, self.lineEdit_realName)

        self.label_IDNum = MLabel(u"身份证号码:")
        self.label_IDNum.setMinimumWidth(90)
        self.lineEdit_IDNum = MLineEdit()
        self.set_widget_layout(self.label_IDNum, self.lineEdit_IDNum)

        self.label_education = MLabel(u"学历:")
        self.label_education.setMinimumWidth(90)
        self.lineEdit_education = MLineEdit()
        self.set_widget_layout(self.label_education, self.lineEdit_education)

        self.label_occupation = MLabel(u"职业:")
        self.label_occupation.setMinimumWidth(90)
        self.lineEdit_occupation = MLineEdit()
        self.set_widget_layout(self.label_occupation, self.lineEdit_occupation)

        self.btn_confirm = MPushButton(u"确认注册:")
        self.set_widget_layout(self.btn_confirm)

        self.setLayout(self.main_lay)

    def set_widget_layout(self, widget1, widget2=None):
        tem_lay = QHBoxLayout()
        # tem_lay.addStretch()
        tem_lay.addWidget(widget1)
        if widget2 is not None:
            tem_lay.addWidget(widget2)
        # tem_lay.addStretch()
        self.main_lay.addLayout(tem_lay)

    def resize_default(self):
        self.setGeometry((1920 - 800) / 2, (1080 - 600) / 2, 300, 350)

    def set_func_connect(self):
        self.btn_confirm.clicked.connect(self.get_input_message)
        self.notenough_signal.connect(functools.partial(self.slot_show_message,
                                                        MMessage.warning,
                                                        {'text': u'请输入完整信息！'}))

    def get_input_message(self):

        self.username = self.lineEdit_userName.text()
        self.userID = self.lineEdit_IDNum.text()
        self.realname = self.lineEdit_realName.text()
        self.job = self.lineEdit_occupation.text()
        self.password = self.lineEdit_password.text()
        self.education = self.lineEdit_education.text()

        if (self.username == "") or \
                (self.userID == "") or \
                (self.realname == "") or \
                (self.job == "") or \
                (self.password == "") or \
                (self.education == ""):
            self.notenough_signal.emit()
        else:
            self.close()

    def slot_show_message(self, func, config):
        func(parent=self, **config)

