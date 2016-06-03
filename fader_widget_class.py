#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

class FaderWidget(QWidget):
    """this class provide fade in/out animation effect"""

    def __init__(self, pre_widget, post_widget):

        QWidget.__init__(self, post_widget)

        self.pre_widget = pre_widget
        self.post_widget = post_widget

        self.pixmap_opacity = 1.0
        self.post_pixmap = QPixmap(960, 540)
        self.pre_widget.render(self.post_pixmap)

    def fade(self, duration):

        self.duration = duration

        self.timeline = QTimeLine()
        self.timeline.setUpdateInterval(1000 / 60)
        self.timeline.setCurveShape(QTimeLine.EaseInOutCurve)
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(self.duration)
        self.timeline.start()

        self.resize(960, 540)
        self.show()

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.post_pixmap)
        painter.end()

    def animate(self, value):

        self.pixmap_opacity = 1.0 - value
        self.repaint()