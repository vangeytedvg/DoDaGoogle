# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui//main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(656, 475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.googleDriveList = QtWidgets.QListWidget(self.centralwidget)
        self.googleDriveList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.googleDriveList.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.SelectedClicked)
        self.googleDriveList.setProperty("showDropIndicator", False)
        self.googleDriveList.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.googleDriveList.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.googleDriveList.setIconSize(QtCore.QSize(96, 96))
        self.googleDriveList.setResizeMode(QtWidgets.QListView.Adjust)
        self.googleDriveList.setViewMode(QtWidgets.QListView.IconMode)
        self.googleDriveList.setUniformItemSizes(True)
        self.googleDriveList.setWordWrap(False)
        self.googleDriveList.setObjectName("googleDriveList")
        self.horizontalLayout.addWidget(self.googleDriveList)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 656, 30))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setIconSize(QtCore.QSize(48, 48))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionE_xit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionE_xit.setIcon(icon)
        self.actionE_xit.setObjectName("actionE_xit")
        self.actionLoad_Files = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Network-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_Files.setIcon(icon1)
        self.actionLoad_Files.setObjectName("actionLoad_Files")
        self.menu_File.addAction(self.actionLoad_Files)
        self.menu_File.addAction(self.actionE_xit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.toolBar.addAction(self.actionLoad_Files)
        self.toolBar.addAction(self.actionE_xit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DoDa Google (GOneDrive)"))
        self.googleDriveList.setSortingEnabled(False)
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionE_xit.setText(_translate("MainWindow", "E&xit"))
        self.actionLoad_Files.setText(_translate("MainWindow", "Load folders"))
import images_rc
