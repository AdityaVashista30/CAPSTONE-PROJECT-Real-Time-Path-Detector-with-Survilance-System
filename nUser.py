import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow
from PyQt5.uic import loadUi
import sqlite3

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('nUser.ui',self)
        self.tabWidget.tabBar().setVisible(False)
        self.handleButtons()
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def handleButtons(self):
        self.homePage.clicked.connect(self.openHome)
        self.liveFPage.clicked.connect(self.openLFoot)
        self.oldFPage.clicked.connect(self.openOFoot)
        self.pathPage.clicked.connect(self.openTracker)
        self.logoutPage.clicked.connect(self.openLogout)
        self.darkO.clicked.connect(self.Dark_Orange_Theme)
        self.darkB.clicked.connect(self.Dark_Blue_Theme)
        self.darkG.clicked.connect(self.Dark_Gray_Theme)
        self.qdark.clicked.connect(self.QDark_Theme)
        
    def openHome(self):
        self.tabWidget.setCurrentIndex(0)
    def openLFoot(self):
        self.tabWidget.setCurrentIndex(1)
    def openOFoot(self):
        self.tabWidget.setCurrentIndex(2)
    def openTracker(self):
        self.tabWidget.setCurrentIndex(3)
    def openLogout(self):
        self.tabWidget.setCurrentIndex(4)
    
    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Gray_Theme(self):
        style = open('themes/darkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)




def main():        
    app = QApplication(sys.argv)
    window=Login()
    window.setWindowTitle('Login')
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
