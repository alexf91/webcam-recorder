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

from __future__ import print_function

import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets, uic

class Viewfinder(QtWidgets.QGraphicsView):
    """Previews the camera image and provides controls for recording."""

    recordStarted = QtCore.pyqtSignal(str)
    recordStopped = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Viewfinder, self).__init__(parent=parent)

        self.camera = None
        self.recordDir = os.path.expanduser('~')
        self.preview = QtMultimediaWidgets.QGraphicsVideoItem()

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setBackgroundBrush(QtCore.Qt.black)
        self.scene.addItem(self.preview)
        self.setScene(self.scene)

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
