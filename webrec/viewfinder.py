#
# Copyright (c) 2018 Alexander Fasching
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function, division

import os
import pkgutil
import datetime as dt

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets, uic

class ButtonSignalSender(QtCore.QObject):
    clicked = QtCore.pyqtSignal()

class ButtonItem(QtWidgets.QGraphicsPixmapItem):
    """Item for the GraphicsView that emits a signal when clicked."""

    def __init__(self, imagedata, parent=None):
        img  = QtGui.QImage.fromData(imagedata)
        pxmap = QtGui.QPixmap.fromImage(img)
        super(ButtonItem, self).__init__(pxmap, parent=parent)
        self.signalSource = ButtonSignalSender()

        self.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.xscale = 1.0
        self.yscale = 1.0

    def setSize(self, width, height):
        """Set the size (in pixels) of the object.
        This changes the transformation matrix of the underlying pixmap item.
        """
        self.xscale = width / self.pixmap().width()
        self.yscale = height / self.pixmap().height()
        trans = QtGui.QTransform()
        trans.scale(self.xscale, self.yscale)
        self.setTransform(trans)

    def width(self):
        return self.pixmap().width() * self.xscale

    def height(self):
        return self.pixmap().height() * self.yscale

    def mousePressEvent(self, event):
        self.signalSource.clicked.emit()


class Viewfinder(QtWidgets.QGraphicsView):
    """Previews the camera image and provides controls for recording."""

    recordStarted = QtCore.pyqtSignal(str)
    recordStopped = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Viewfinder, self).__init__(parent=parent)

        self.camera = None
        self.recordDir = os.path.expanduser('~')

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QtCore.Qt.black)
        self.setScene(self.scene)

        # Camera preview
        self.preview = QtMultimediaWidgets.QGraphicsVideoItem()
        self.scene.addItem(self.preview)

        # Record and stop button. The record button is initially added to the scene.
        self.stopItem = ButtonItem(pkgutil.get_data('webrec', 'resources/stop_icon.png'))
        self.stopItem.signalSource.clicked.connect(self.stopClicked)
        self.recordItem = ButtonItem(pkgutil.get_data('webrec', 'resources/record_icon.png'))
        self.recordItem.signalSource.clicked.connect(self.recordClicked)
        self.scene.addItem(self.recordItem)

        self.resize(self.width(), self.height())

    @QtCore.pyqtSlot(QtMultimedia.QCamera)
    def setCamera(self, camera):
        """Set the camera that is previewed."""
        self.camera = camera
        self.camera.setViewfinder(self.preview)
        self.camera.start()

    @QtCore.pyqtSlot(str)
    def setRecordDirectory(self, dirpath):
        """Set the directory that is used to record files."""
        self.recordDir = dirpath

    @QtCore.pyqtSlot(int, int)
    def resize(self, width, height):
        """Set the size of the viewfinder."""
        self.scene.setSceneRect(0, 0, width, height)
        self.preview.setSize(QtCore.QSizeF(width, height))

        sidelength = height * 0.2

        for item in (self.recordItem, self.stopItem):
            item.setSize(sidelength, sidelength)
            item.setPos((width - item.width()) // 2, (height - item.height()) * 0.8)

    @QtCore.pyqtSlot()
    def recordClicked(self):
        self.scene.removeItem(self.recordItem)
        self.scene.addItem(self.stopItem)
        fname = dt.datetime.now().strftime('%Y%m%dT%H%M%S')
        self.recordStarted.emit(os.path.join(self.recordDir, fname))

    @QtCore.pyqtSlot()
    def stopClicked(self):
        self.scene.removeItem(self.stopItem)
        self.scene.addItem(self.recordItem)
        self.recordStopped.emit()
