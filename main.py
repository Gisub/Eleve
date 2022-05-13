# -*- coding: utf-8 -*-

import os
import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ui.ui_eleve import Ui_Eleve
from ui.ui_settings import Ui_Settings
from utils.ui_operation import UpdateUI
from database.env import *


class Eleve(Ui_Eleve, QWidget):

    def __init__(self):
        super(Eleve, self).__init__()
        self.setupUi(self)
        self.current_category = None
        self.settings_ui = Ui_Settings()
        self.ui = UpdateUI(self)

        self.set_icons()
        self.trigger_btn_signals()
        self.default_ui()

        # close if the widget is already opened.
        for widget in QApplication.allWidgets():
            if type(widget).__name__ == "Eleve":
                widget.close()

    def trigger_btn_signals(self):
        """
        trigger button signals.
        :return: None.
        """
        self.btn_search.toggled.connect(lambda: self.ui.toggle_search())
        self.btn_info_global.toggled.connect(lambda: self.ui.toggle_info())
        self.btn_favourite.toggled.connect(self.ui.update_thumbnail_items)
        self.btn_refresh.clicked.connect(self.ui.update_thumbnail_items)
        self.combo_group.currentIndexChanged.connect(self.ui.add_root_tree)
        self.combo_file_type_filter.currentIndexChanged.connect(self.ui.update_thumbnail_items)
        self.tree_category.itemChanged.connect(self.tree_item_changed)
        self.tree_category.currentItemChanged.connect(
            lambda: self.ui.load_thumbnail_widget(
                self.frame_thumb_loader.width(),
                self.frame_thumb_loader.height()
            )
        )
        self.lineEdit_search.textChanged.connect(self.ui.user_search)
        self.btn_info_global.toggled.connect(
            lambda: self.ui.metadata(info=self.btn_info_global.isChecked())
        )
        if os.environ.get('HOSTNAME') in config['ADMIN']:
            self.btn_settings.clicked.connect(lambda: self.ui.enable_settings_ui(self.settings_ui))
            self.btn_home.clicked.connect(lambda: self.ui.enable_content_ui(self.settings_ui))
            self.btn_add_group.clicked.connect(lambda: self.ui.add_group(self))
            self.btn_remove_group.clicked.connect(self.ui.remove_group)
            self.btn_category_add.clicked.connect(self.ui.add_category)
            self.btn_category_remove.clicked.connect(self.ui.remove_category)

    def set_icons(self):
        """
        Set icons for buttons.
        :return: None.
        """
        self.btn_refresh.setIcon(QIcon(config['icons'] + "/refresh.png"))
        self.btn_favourite.setIcon(QIcon(config['icons'] + "/remove_fav.png"))
        self.btn_grid_view.setIcon(QIcon(config['icons'] + "/grid.png"))
        self.btn_list_view.setIcon(QIcon(config['icons'] + "/list.png"))
        self.btn_info_global.setIcon(QIcon(config['icons'] + "/info.png"))
        self.btn_search.setIcon(QIcon(config['icons'] + "/search.png"))
        self.btn_settings.setIcon(QIcon(config['icons'] + "/setting.png"))
        self.btn_home.setIcon(QIcon(config['icons'] + "/home.png"))
        if os.environ.get('HOSTNAME') in config['ADMIN']:
            self.btn_add_group.setIcon(QIcon(config['icons'] + "/plus.png"))
            self.btn_remove_group.setIcon(QIcon(config['icons'] + "/minus.png"))
            self.btn_category_add.setIcon(QIcon(config['icons'] + "/plus_cyan.png"))
            self.btn_category_remove.setIcon(QIcon(config['icons'] + "/minus_cyan.png"))

    def default_ui(self):
        """
        startup default settings.
        :return: None
        """
        if UpdateUI.load_settings()["stay_top"] == "True":
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.lineEdit_search.hide()
        self.combo_file_type_filter.hide()
        self.frame_content_right.hide()
        self.ui.load_groups_ui(UpdateUI.load_settings()["category"])
        self.ui.add_root_tree()
        self.ui.add_filter_items()
        self.tree_category.setStyleSheet("QTreeWidget:item{height: 24px;}")

    def keyPressEvent(self, event):
        """
        Rename the categories in tree widget by pressing F2.
        Open metadata popup by pressing F6
        """
        if event.key() == Qt.Key_F2:
            item = self.tree_category.currentItem()
            if not item.text(0).lower() == "root":
                if not self.ui.validate_category_rename():
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.tree_category.editItem(item, 0)
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.current_category = str(item.text(0))
                else:
                    self.label_status_progress.setText("Items loaded, cannot rename!")

        # Open metadata popup by pressing F6.
        if event.key() == Qt.Key_F6:
            self.ui.metadata(info=self.btn_info_global.isChecked())

    def tree_item_changed(self):
        """
        update renamed categories in data.json.
        """
        if self.current_category:
            self.ui.update_category_json(
                self.tree_category.currentItem(), self.current_category
            )
            self.current_category = None

    def event(self, event):
        if event.type() == QEvent.Type.Show:
            try:
                set_widget_margins(self)
            except:
                pass
        return QWidget.event(self, event)


def set_widget_margins(widget_object):
    if widget_object:
        target_widgets = set()
        target_widgets.add(widget_object.parentWidget().parentWidget())
        target_widgets.add(widget_object.parentWidget().parentWidget().parentWidget().parentWidget())

        for widget_layout in target_widgets:
            try:
                widget_layout.layout().setContentsMargins(0, 0, 0, 0)
            except Exception as error:
                print(error)


def main():
    main.e = Eleve()
    main.e.show()
