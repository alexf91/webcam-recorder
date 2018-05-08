#!/usr/bin/env python

from setuptools import setup

setup(name='webcam-recorder',
    version='0.1',
    description='Simple program to preview and record a webcam stream.',
    author='Alexander Fasching',
    author_email='fasching.a91@gmail.com',
    maintainer='Alexander Fasching',
    maintainer_email='fasching.a91@gmail.com',
    url='https://github.com/alexf91/webcam-recorder',
    license='MIT',
    packages=['webrec'],
    entry_points={
        'console_scripts': ['webrec = webrec.__main__:main']
    },
    package_data={
        'webrec': ['resources/*.ui']
    },
    install_requires=[
        'pyqt5',
    ],
)
