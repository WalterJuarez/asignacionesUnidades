# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'credenciales.ui'
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
    QPushButton, QSizePolicy, QStatusBar, QToolButton,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(290, 398)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.txt_nameUser = QLineEdit(self.centralwidget)
        self.txt_nameUser.setObjectName(u"txt_nameUser")
        self.txt_nameUser.setGeometry(QRect(40, 50, 201, 31))
        font = QFont()
        font.setFamilies([u"Microsoft Sans Serif"])
        font.setPointSize(12)
        self.txt_nameUser.setFont(font)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(110, 30, 61, 21))
        self.label_4.setFont(font)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(110, 90, 61, 21))
        self.label_5.setFont(font)
        self.txt_apellidoUser = QLineEdit(self.centralwidget)
        self.txt_apellidoUser.setObjectName(u"txt_apellidoUser")
        self.txt_apellidoUser.setGeometry(QRect(40, 110, 201, 31))
        self.txt_apellidoUser.setFont(font)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(110, 150, 61, 21))
        self.label_6.setFont(font)
        self.txt_user = QLineEdit(self.centralwidget)
        self.txt_user.setObjectName(u"txt_user")
        self.txt_user.setGeometry(QRect(40, 170, 201, 31))
        self.txt_user.setFont(font)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(70, 210, 141, 21))
        self.label_7.setFont(font)
        self.txt_passwordNew = QLineEdit(self.centralwidget)
        self.txt_passwordNew.setObjectName(u"txt_passwordNew")
        self.txt_passwordNew.setGeometry(QRect(40, 230, 201, 31))
        self.txt_passwordNew.setFont(font)
        self.txt_passwordNew.setEchoMode(QLineEdit.Password)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(70, 270, 141, 21))
        self.label_8.setFont(font)
        self.txt_passwordNew1 = QLineEdit(self.centralwidget)
        self.txt_passwordNew1.setObjectName(u"txt_passwordNew1")
        self.txt_passwordNew1.setGeometry(QRect(40, 290, 201, 31))
        self.txt_passwordNew1.setFont(font)
        self.txt_passwordNew1.setEchoMode(QLineEdit.Password)
        self.btn_aceptarCreden = QPushButton(self.centralwidget)
        self.btn_aceptarCreden.setObjectName(u"btn_aceptarCreden")
        self.btn_aceptarCreden.setGeometry(QRect(100, 340, 75, 31))
        font1 = QFont()
        font1.setFamilies([u"Microsoft Sans Serif"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.btn_aceptarCreden.setFont(font1)
        self.btn_verPass = QToolButton(self.centralwidget)
        self.btn_verPass.setObjectName(u"btn_verPass")
        self.btn_verPass.setGeometry(QRect(250, 230, 31, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cambio de credenciales", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Nombre:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Apellido:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Usuario:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Nueva contrase\u00f1a:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Repita contrase\u00f1a:", None))
        self.btn_aceptarCreden.setText(QCoreApplication.translate("MainWindow", u"Aceptar", None))
        self.btn_verPass.setText("")
    # retranslateUi

