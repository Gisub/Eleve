# -*- coding: utf-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import os

from database.database import Database


class Ui_Settings(QFrame):
    def __init__(self):
        super(Ui_Settings, self).__init__()
        self.db = Database()

        self.resize(1637, 996)
        self.setObjectName("frame_settings")
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        font = QFont()
        font.setPointSize(9)

        self.group_settings_general = QGroupBox(self)
        self.group_settings_general.setObjectName("group_settings_general")
        self.group_settings_general.setFlat(True)
        self.verticalLayout_2 = QVBoxLayout(self.group_settings_general)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 30, -1, -1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(9)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, -1, -1, -1)

        self.category_label = QLabel(self.group_settings_general)
        self.category_label.setObjectName("category_label")
        self.category_label.setMaximumSize(QSize(100, 24))
        self.category_label.setFont(font)
        self.category_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.category_label, 0, 0, 1, 1)

        self.category_combobox = QComboBox(self.group_settings_general)
        self.category_combobox.setObjectName("category_combobox")
        for group in self.db.read_from_json():
            self.category_combobox.addItem(group)
        self.category_combobox.setMaximumSize(QSize(300, 25))

        self.gridLayout.addWidget(self.category_combobox, 0, 1, 1, 1)

        self.always_on_top_label = QLabel(self.group_settings_general)
        self.always_on_top_label.setObjectName("always_on_top_label")
        self.always_on_top_label.setMaximumSize(QSize(100, 24))
        self.always_on_top_label.setFont(font)
        self.always_on_top_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.always_on_top_label, 1, 0, 1, 1)

        self.always_top_chkbox = QCheckBox('', self.group_settings_general)
        self.always_top_chkbox.setFont(font)
        self.always_top_chkbox.setFocusPolicy(Qt.ClickFocus)

        self.gridLayout.addWidget(self.always_top_chkbox, 1, 1, 1, 1)

        self_dummy = QFrame(self.group_settings_general)
        self_dummy.setObjectName("frame_settings_dummy")
        self_dummy.setFrameShape(QFrame.NoFrame)
        self_dummy.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self_dummy, 6, 1, 1, 1)

        self_dummy_2 = QFrame(self.group_settings_general)
        self_dummy_2.setObjectName("frame_settings_dummy_2")
        self_dummy_2.setFrameShape(QFrame.NoFrame)
        self_dummy_2.setFrameShadow(QFrame.Plain)

        self.gridLayout.addWidget(self_dummy_2, 2, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self_footer = QFrame(self.group_settings_general)
        self_footer.setObjectName("frame_settings_footer")
        self_footer.setMaximumSize(QSize(16777215, 40))
        self_footer.setFrameShape(QFrame.NoFrame)
        self_footer.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self_footer)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 6, 0)
        self.frame_2 = QFrame(self_footer)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_3.addWidget(self.frame_2)

        self.btn_apply_settings = QPushButton(self_footer)
        self.btn_apply_settings.setObjectName("btn_apply_settings")
        self.btn_apply_settings.setMinimumSize(QSize(0, 24))
        self.btn_apply_settings.setMaximumSize(QSize(100, 24))
        self.btn_apply_settings.setFont(font)
        self.btn_apply_settings.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.btn_apply_settings)

        self.btn_reset_settings = QPushButton(self_footer)
        self.btn_reset_settings.setObjectName("btn_reset_settings")
        self.btn_reset_settings.setMinimumSize(QSize(0, 24))
        self.btn_reset_settings.setMaximumSize(QSize(100, 24))
        self.btn_reset_settings.setFont(font)
        self.btn_reset_settings.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.btn_reset_settings)

        self.verticalLayout_2.addWidget(self_footer)
        self.verticalLayout.addWidget(self.group_settings_general)

        QMetaObject.connectSlotsByName(self)
        self.setWindowTitle(QCoreApplication.translate("Settings", "Form", None))
        self.group_settings_general.setTitle(QCoreApplication.translate("Settings", "General", None))
        self.category_label.setText(QCoreApplication.translate("Settings", "Default Category", None))
        self.always_on_top_label.setText(QCoreApplication.translate("Settings", "Always on top", None))
        self.btn_apply_settings.setText(QCoreApplication.translate("Settings", "Apply", None))
        self.btn_reset_settings.setText(QCoreApplication.translate("Settings", "Reset", None))

