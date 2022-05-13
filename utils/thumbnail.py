
import os

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from database.env import *
from database.database import Database


class Thumbnail(QWidget):

    def __init__(self, parent, *drop, **data):
        """
        widget to load thumbnail.
        :rtype: object
        :param QWidget parent: Table widget
        :param tuple drop: is item dropped.
        """
        super(Thumbnail, self).__init__(parent)
        cache, src, self.drop = str(data['item']), str(data['source']), drop
        self.parent_dir = config['icons']
        if os.path.splitext(src)[1] in ['.obj', '.abc', '.fbx']:
            cache = "{}/obj.png".format(self.parent_dir)
        if os.path.splitext(src)[1] in ['.nk']:
            cache = "{}/nuke_1.png".format(self.parent_dir)

        widget_layout = QGridLayout()
        self.thumbnail_label = QLabel()
        self.file_label = QLabel()
        self.file_label.setAlignment(Qt.AlignHCenter)
        self.thumbnail_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.file_label.setMaximumHeight(30)
        if '$$' in src:
            clip = os.path.basename(src).split('$$')[0]
            folder = src.split('/')[-2]
            current_item = "{}\n/{}".format(folder, clip)
        else:
            current_item = os.path.basename(src)
        self.file_label.setText(current_item)
        self.file_label.setStyleSheet('QLabel{color:rgb(160, 160, 160, 160);}')
        widget_layout.addWidget(self.thumbnail_label)
        widget_layout.addWidget(self.file_label)
        self.thumbnail_label.setGeometry(0, 0, config['DIMENSION_X'], config['DIMENSION_Y'])
        self.setLayout(widget_layout)
        self.load_gif(cache)
        self.setMaximumWidth(250)
        QApplication.processEvents()

    @staticmethod
    def read_db():
        """
        load the database from data.json.
        :return dict: database.
        """
        db = Database()
        return db.read_from_json()

    def load_gif(self, cache):
        """
        load gif/image into widget.
        :param str cache: cache file to be loaded in widget.
        :return: None
        """

        if self.drop:
            pixmap = QPixmap("{}/submit_progress.png".format(self.parent_dir))
            self.thumbnail_label.setPixmap(pixmap)
            self.opacity = QGraphicsOpacityEffect()
            self.opacity.setOpacity(0.3)
            self.thumbnail_label.setGraphicsEffect(self.opacity)

        else:
            if os.path.isfile(cache + '.tmp'):
                pixmap = QPixmap("{}/submit_progress.png".format(self.parent_dir))
                self.thumbnail_label.setPixmap(pixmap)
                self.opacity = QGraphicsOpacityEffect()
                self.opacity.setOpacity(0.3)
                self.thumbnail_label.setGraphicsEffect(self.opacity)

            elif isinstance(cache, str) and cache.endswith('.gif'):
                if not os.path.isfile(cache):
                    pixmap = QPixmap("{}/error.png".format(self.parent_dir))
                    self.thumbnail_label.setPixmap(pixmap)
                else:
                    self.movie = QMovie(cache)
                    self.movie.setCacheMode(QMovie.CacheAll)
                    self.movie.start()
                    self.movie.stop()
                    self.movie.jumpToFrame(20)
                    self.thumbnail_label.setMovie(self.movie)
                    self.movie.setScaledSize(self.movie.scaledSize())

            else:
                if not os.path.isfile(cache):
                    pixmap = QPixmap("{}/error.png".format(self.parent_dir))
                else:
                    pixmap = QPixmap(cache)
                self.thumbnail_label.setPixmap(
                    pixmap.scaled(
                        self.thumbnail_label.width(),
                        self.thumbnail_label.height(),
                        Qt.KeepAspectRatio
                    )
                )

    def enterEvent(self, event):
        """
        play gif if mouse cursor enters the cell.
        """
        try:
            if not self.drop:
                self.movie.jumpToFrame(0)
                self.movie.start()
        except AttributeError:
            pass

    def leaveEvent(self, event):
        """
        stop gif if mouse cursor leaves the cell.
        """
        try:
            if not self.drop:
                self.movie.jumpToFrame(20)
                self.movie.stop()
        except AttributeError:
            pass
