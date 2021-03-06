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
        loadUi('login.ui',self)
        self.pushButton.clicked.connect(self.checkLogin)
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)


    
    def checkLogin(self):
        conn = sqlite3.connect('capstoneSQLDB2.db')
        cur = conn.cursor()
        user=self.user.text()
        password=self.password.text()
        cur.execute('SELECT Password,Type FROM Users WHERE User = ? ', (user,))
        row =cur.fetchone()
        cur.close()
        if row is None:
            self.label.setText("INVALID USER/PASSWORD")
        elif str(row[0])!=password:
             self.label.setText("INVALID USER/PASSWORD")
        else:
            if row[1]=="Admin":
                from Admin import admin
                self.window2 = admin()
                self.close()
                self.window2.setWindowTitle('ADMIN WINDOW')
                self.window2.show()
            else:
                from nUser import nuser
                self.window2 = nuser()
                self.close()
                self.window2.setWindowTitle('USER WINDOW')
                self.window2.show()

        
        
        
def main():        
    app = QApplication(sys.argv)
    window=Login()
    window.setWindowTitle('Login')
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
