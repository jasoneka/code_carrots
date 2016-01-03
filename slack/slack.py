# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'slack.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(464, 428)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.comboChannel = QtGui.QComboBox(self.centralwidget)
        self.comboChannel.setGeometry(QtCore.QRect(20, 10, 181, 26))
        self.comboChannel.setObjectName(_fromUtf8("comboChannel"))
        self.channelHistoryTextEdit = QtGui.QPlainTextEdit(self.centralwidget)
        self.channelHistoryTextEdit.setGeometry(QtCore.QRect(20, 40, 371, 261))
        self.channelHistoryTextEdit.setObjectName(_fromUtf8("channelHistoryTextEdit"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(10, 310, 441, 81))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.gridLayoutWidget = QtGui.QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.postButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.postButton.setObjectName(_fromUtf8("postButton"))
        self.gridLayout.addWidget(self.postButton, 0, 1, 1, 1)
        self.messageEditField = QtGui.QLineEdit(self.gridLayoutWidget)
        self.messageEditField.setObjectName(_fromUtf8("messageEditField"))
        self.gridLayout.addWidget(self.messageEditField, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 464, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Slack Client PyQT", None))
        self.postButton.setText(_translate("MainWindow", "Post", None))

