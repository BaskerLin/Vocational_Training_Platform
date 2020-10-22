# coding=utf8
import sys
import os

from GDB import GMySQLConnector
import mysql
import pymysql

import dayu_widgets
from dayu_widgets.dock_widget import MDockWidget
from dayu_widgets import MTextEdit, MLineEdit, MPushButton, MLabel, MDivider, MCarousel, MTreeView
from dayu_widgets.qt import *


class MainWindow(QWidget):
    ICON_PATH = os.path.join(os.getcwd(), r"img\LOGO1.png")
    LOGO_PATH = os.path.join(os.getcwd(), r"img\LOGO2.png")

    def __init__(self):
        super(MainWindow, self).__init__()

        # 初始化控件
        self.icon_logo = None
        self.main_lay = None

        # 上部layout
        self.lay1 = None
        self.pix_logo = None
        self.label_logo = None
        self.label_search = None
        self.lineEdit_search = None
        self.btn_signIn = None
        self.btn_register = None
        self.divider_h = None

        # 下部layout
        self.lay2 = None
        self.lay2_1 = None
        self.lay2_2 = None

        self.carousel = None

        self.construct_ui()
        self.resize_default()

    def construct_ui(self):
        self.setWindowTitle(u"职业培训平台")
        self.icon_logo = QIcon(QIcon(self.ICON_PATH))
        self.setWindowIcon(self.icon_logo)

        # 总体layout
        self.main_lay = QVBoxLayout()

        # Lay1_1
        self.lay1 = QHBoxLayout()

        self.label_logo = MLabel()
        self.label_logo.setPixmap(self.LOGO_PATH)
        self.label_logo.setScaledContents(True)
        self.label_logo.setMinimumSize(354, 100)
        self.label_logo.setMaximumSize(354, 100)

        self.label_search = MLabel(u"搜索")
        self.lineEdit_search = MLineEdit()

        self.btn_signIn = MPushButton(u"  登录  ")
        self.btn_register = MPushButton(u"  注册  ")

        self.lay1.addWidget(self.label_logo)
        self.lay1.addWidget(self.label_search)
        self.lay1.addWidget(self.lineEdit_search)
        self.lay1.addStretch()
        self.lay1.addWidget(self.btn_signIn)
        self.lay1.addWidget(self.btn_register)

        # lay2_1
        self.lay2 = QHBoxLayout()
        self.lay2_1 = QVBoxLayout()
        self.lay2_2 = QVBoxLayout()

        # self.lay2_1.addStretch()

        self.carousel = MCarousel([MPixmap(r'D:\LinHuiHuang\Vocational_Training_Platform\img\1.PNG'),
                                   MPixmap(r'D:\LinHuiHuang\Vocational_Training_Platform\img\2.PNG'),
                                   MPixmap(r'D:\LinHuiHuang\Vocational_Training_Platform\img\3.PNG'),
                                   MPixmap(r'D:\LinHuiHuang\Vocational_Training_Platform\img\4.PNG')],
                                  width=1202,
                                  height=362,
                         autoplay=True)
        self.lay2_2.addWidget(self.carousel)
        self.lay2_2.addStretch()

        self.lay2.addLayout(self.lay2_1)
        self.lay2.addLayout(self.lay2_2)


        # 添加layout至main_lay
        self.main_lay.addLayout(self.lay1)

        self.divider_h = MDivider()
        self.main_lay.addWidget(self.divider_h)

        self.main_lay.addLayout(self.lay2)
        # self.main_lay.addStretch()
        self.setLayout(self.main_lay)

    def resize_default(self):
        self.setGeometry((1920 - 800) / 2, (1080 - 600) / 2, 800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    dayu_widgets.dayu_theme.apply(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

    # conn = GMySQLConnector()
    # conn.set_config({
    #             'user': "root",
    #             'password': "root",
    #             'host': "localhost",
    #             'database': "world",
    #         })
    # print conn.auto_query("SELECT * FROM country")[3]['Region']