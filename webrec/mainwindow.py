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
import datetime as dt
import pkgutil
from io import StringIO

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets, uic

from .recorder import Recorder

class MainWindow(QtWidgets.QMainWindow):
    """Main window of the recorder."""

    def __init__(self, camera_info, output_path, parent=None):
        super(MainWindow, self).__init__(parent)

        # Setup main window
        uifile = StringIO(pkgutil.get_data('webrec', 'resources/mainwindow.ui').decode('utf-8'))
        uic.loadUi(uifile, self)
        self.output_path = output_path

        # Display the camera image on viewfinder
        camera = QtMultimedia.QCamera(camera_info)
        camera.setCaptureMode(QtMultimedia.QCamera.CaptureVideo)
        self.viewfinder.setCamera(camera)
        self.viewfinder.setRecordDirectory(output_path)

        # Initialize the recorder and connect the signals
        self.recorder = Recorder(parent=self)
        self.recorder.setCamera(camera)

        # Connect the signals
        self.viewfinder.recordStarted.connect(self.recorder.startRecording)
        self.viewfinder.recordStopped.connect(self.recorder.stopRecording)

    def resizeEvent(self, event):
        """Window was resized."""
        self.viewfinder.resize(event.size().width(), event.size().height())
