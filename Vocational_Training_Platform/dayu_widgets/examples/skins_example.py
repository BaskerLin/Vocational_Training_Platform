# coding=utf8
# Copyright (c) 2019 GVF
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.divider import MDivider
from dayu_widgets.field_mixin import MFieldMixin
from dayu_widgets.push_button import MPushButton
from dayu_widgets.qt import QWidget, QVBoxLayout, \
    QApplication, Qt, QMessageBox, QStandardItemModel,\
    QStandardItem, QHBoxLayout, Signal, QAbstractItemView
from dayu_widgets.theme import MTheme
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.menu import MMenu

from functools import partial
import json
import os

PRESET_JSON = os.path.join(os.path.expanduser("~"), "theme_setting.json")
COLOR_DICT = {
    u"蓝": MTheme.blue,
    u"紫": MTheme.purple,
    u"青": MTheme.cyan,
    u"绿": MTheme.green,
    u"品红": MTheme.magenta,
    u"粉红": MTheme.pink,
    u"红": MTheme.red,
    u"橘": MTheme.orange,
    u"黄": MTheme.yellow,
    u"火": MTheme.volcano,
    u"蓝绿": MTheme.geekblue,
    u"绿黄": MTheme.lime,
    u"金": MTheme.gold
}


class Main_UI(QWidget, MFieldMixin):
    def __init__(self, parent=None):
        super(Main_UI, self).__init__(parent)
        self.resize(500, 500)
        self._init_ui()

    def _init_ui(self):

        v_layout = QVBoxLayout(self)

        self.dayu_theme = MTheme("dark")
        self.dayu_theme.apply(self)

        # skin setting
        skin_divider = MDivider(u"一个不用充钱就可以换皮肤的功能")
        # theme
        self.theme_combobox = MComboBox()
        self.theme_combobox.setFixedWidth(80)
        self.theme_combobox.set_dayu_size(20)
        theme_menu = MMenu()
        theme_menu.set_data(["dark", "light"])
        self.theme_combobox.set_menu(theme_menu)
        self.theme_combobox.sig_value_changed.connect(self.change_theme)
        # color
        self.color_combobox = MComboBox()
        self.color_combobox.setFixedWidth(80)
        self.color_combobox.set_dayu_size(20)
        color_menu = MMenu()
        color_menu.set_data(COLOR_DICT.keys())
        self.color_combobox.set_menu(color_menu)
        self.color_combobox.sig_value_changed.connect(self.change_color)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.theme_combobox)
        h_layout.addWidget(self.color_combobox)

        v_layout.addWidget(skin_divider)
        v_layout.addLayout(h_layout)

        color_divider = MDivider(u"可以尝试输入一个颜色")
        self.color_line = MLineEdit()
        v_layout.addWidget(color_divider)
        v_layout.addWidget(self.color_line)

        button1 = MPushButton(u"测试").huge()
        v_layout.addWidget(button1)
        button2 = MPushButton(u"颜色").huge()
        v_layout.addWidget(button2)
        button3 = MPushButton(u"长什么").huge()
        v_layout.addWidget(button3)
        button4 = MPushButton(u"样子").huge()
        v_layout.addWidget(button4)

        button1.clicked.connect(self.set_color)
        button2.clicked.connect(self.set_color)
        button3.clicked.connect(self.set_color)
        button4.clicked.connect(self.set_color)

        v_layout.addStretch()

    def set_color(self):
        if self.color_line.text():
            self.dayu_theme.set_primary_color(self.color_line.text())
            self.dayu_theme.apply(self)

    def change_theme(self, value):
        self.dayu_theme.set_theme(value)
        self.dayu_theme.apply(self)

    def change_color(self, value):
        self.dayu_theme.set_primary_color(COLOR_DICT[value])
        self.dayu_theme.apply(self)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Main_UI()
    win.show()
    app.exec_()