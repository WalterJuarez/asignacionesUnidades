# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(375, 297)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 20, 71, 31))
        font = QFont()
        font.setFamilies([u"Microsoft Sans Serif"])
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(140, 100, 111, 31))
        self.label_2.setFont(font)
        self.txt_usuario = QLineEdit(self.centralwidget)
        self.txt_usuario.setObjectName(u"txt_usuario")
        self.txt_usuario.setGeometry(QRect(90, 60, 191, 31))
        font1 = QFont()
        font1.setFamilies([u"Microsoft Sans Serif"])
        font1.setPointSize(12)
        self.txt_usuario.setFont(font1)
        self.txt_usuario.setAlignment(Qt.AlignCenter)
        self.txt_contra = QLineEdit(self.centralwidget)
        self.txt_contra.setObjectName(u"txt_contra")
        self.txt_contra.setGeometry(QRect(90, 140, 191, 31))
        self.txt_contra.setFont(font1)
        self.txt_contra.setEchoMode(QLineEdit.Password)
        self.txt_contra.setAlignment(Qt.AlignCenter)
        self.btn_ingresar = QPushButton(self.centralwidget)
        self.btn_ingresar.setObjectName(u"btn_ingresar")
        self.btn_ingresar.setGeometry(QRect(140, 190, 91, 41))
        self.btn_ingresar.setFont(font1)
        self.lbl_recuperar = QLabel(self.centralwidget)
        self.lbl_recuperar.setObjectName(u"lbl_recuperar")
        self.lbl_recuperar.setGeometry(QRect(20, 260, 181, 16))
        font2 = QFont()
        font2.setFamilies([u"Microsoft Sans Serif"])
        font2.setPointSize(9)
        self.lbl_recuperar.setFont(font2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Inicio de sesi\u00f3n", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Usuario", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Contrase\u00f1a", None))
        self.btn_ingresar.setText(QCoreApplication.translate("MainWindow", u"Ingresar", None))
        self.lbl_recuperar.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><a href=\"recuperar\">Olvid\u00e9 mi usuario y contrase\u00f1a</a></p><p><br/></p></body></html>", None))
    # retranslateUi

