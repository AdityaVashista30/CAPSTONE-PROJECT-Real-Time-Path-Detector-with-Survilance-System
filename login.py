import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow
from PyQt5.uic import loadUi
import sqlite3
from nUser import nuser 

class Login(QMainWindow):
    def __init__(self):
        self.conn = sqlite3.connect('capstone.db')
        self.cur = self.conn.cursor()
        super(Login,self).__init__()
        loadUi('login.ui',self)
        self.pushButton.clicked.connect(self.checkLogin)
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)


    
    def checkLogin(self):
        user=self.user.text()
        password=self.password.text()
        self.cur.execute('SELECT Password,Type FROM Users WHERE User = ? ', (user,))
        row = self.cur.fetchone()
        if row is None:
            self.label.setText("INVALID USER/Password")
        elif str(row[0])!=password:
             self.label.setText("INVALID USER/Password")
        else:
            if row[1]=="Admin":
                self.label.setText("Admin Login Succesful") #TEMP
            else:
                self.window2 = nuser()
                self.close()
                self.window2.show()

        
        
        
def main():        
    app = QApplication(sys.argv)
    window=Login()
    window.setWindowTitle('Login')
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
