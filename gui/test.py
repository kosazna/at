# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerVwXFBS.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(545, 373)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(150, 60, 276, 248))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 4, 2, 4)
        self.listWidget = QListWidget(self.groupBox)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setCheckState(Qt.Unchecked);
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem1.setCheckState(Qt.Unchecked);
        __qlistwidgetitem2 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem2.setCheckState(Qt.Unchecked);
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.listWidget.setResizeMode(QListView.Adjust)
        self.listWidget.setSpacing(1)
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.listWidget)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox, 0, Qt.AlignHCenter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Select Shapefiles", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"ASTOTA", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Form", u"ASTENOT", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Form", u"PST", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.checkBox.setText(QCoreApplication.translate("Form", u"Select All", None))
    # retranslateUi
