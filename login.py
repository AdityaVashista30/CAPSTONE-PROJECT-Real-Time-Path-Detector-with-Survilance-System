import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow
from PyQt5.uic import loadUi
import sqlite3


class Login(QMainWindow):
    def __init__(self):
        self.conn = sqlite3.connect('capstone.db')
        self.cur = self.conn.cursor()
        super(Login,self).__init__()
        loadUi('login.ui',self)

        
        
        
def main():        
    app = QApplication(sys.argv)
    window=Login()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
