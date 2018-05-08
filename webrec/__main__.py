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

import sys
import argparse
import os

import numpy as np
from PyQt5 import QtWidgets, QtMultimedia

from .mainwindow import MainWindow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', action='store_true',
            help='list available camera devices')
    parser.add_argument('--device', '-d', type=int, default=0,
            help='index of the camera device')
    parser.add_argument('--fullscreen', '-f', action='store_true',
            help='show window in full screen')
    parser.add_argument('--output', '-o', type=str, default=os.path.expanduser('~'),
            help='directory where output files are stored')
    args = parser.parse_args()

    cameras = QtMultimedia.QCameraInfo.availableCameras()
    if args.list:
        for i, info in enumerate(cameras):
            print('{}: {}'.format(i, info.description()))
        return 0

    if args.device < 0 or args.device >= len(cameras):
        print('Invalid camera index or no devices found', file=sys.stderr)
        return 1

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(camera_info=cameras[args.device], output_path=args.output)
    if args.fullscreen:
        w.showFullScreen()
    else:
        w.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main() or 0)
