import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot,QSize, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow,QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3
import cv2
from player import Player

class admin(QMainWindow):
    def __init__(self):
        super(admin,self).__init__()
        loadUi('admin.ui',self)
        self.tabWidget.tabBar().setVisible(False)
        self.handleButtons()
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.camOn=False
        self.video_size=QSize(601,341)
        self.image=None
    
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
        self.showLive.clicked.connect(self.start_cam)
        self.pauseLive.clicked.connect(self.stop_cam)
        self.yes.clicked.connect(self.logoutYes)
        self.no.clicked.connect(self.openHome)
        self.showVid.clicked.connect(self.callPlayer)
        self.delVid.clicked.connect(self.del_Old_Vid)
        
    def openHome(self):
        self.stop_cam()
        self.tabWidget.setCurrentIndex(0)
    def openLFoot(self):
        self.tabWidget.setCurrentIndex(1)
    def openOFoot(self):
        self.stop_cam()
        self.show_Old_Vid()
    def openTracker(self):
        self.stop_cam()
        self.tabWidget.setCurrentIndex(3)
    def openLogout(self):
        self.stop_cam()
        self.tabWidget.setCurrentIndex(4)
    
    def show_Old_Vid(self):
        self.tabWidget.setCurrentIndex(2)
        conn = sqlite3.connect('capstoneSQLDB.db')
        cur = conn.cursor()
        data=cur.execute('SELECT Code,Date,Time,Cam FROM VidHistory')
        if data:
            self.vidTable.setRowCount(0)
            self.vidTable.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form) :
                    self.vidTable.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.vidTable.rowCount()
                self.vidTable.insertRow(row_position)
        cur.close()
        
    def del_Old_Vid(self):
        code=self.lineEdit_2.text()     
        conn = sqlite3.connect('capstoneSQLDB.db')
        cur = conn.cursor()
        cur.execute('Delete FROM VidHistory where code= ?',(code,))
        conn.commit()
        cur.close()
        self.show_Old_Vid()
        

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
    
    def start_cam(self):
        if self.camBox.currentText() !="SELECT":
            self.camOn=True
            if self.camBox.currentText() =="WEB CAM (TEMP)":
                self.capture=cv2.VideoCapture(0,cv2.CAP_DSHOW) 
 
            i=0
            while i<22000:
                i+=1
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,self.video_size.width())
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,self.video_size.height())
            self.timer =QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(0.01)

    def update_frame(self):
        ret,frame=self.capture.read()
        self.image=cv2.cvtColor(frame,1)
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:  
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        
        img = QImage(self.image, self.image.shape[1], self.image.shape[0],
                     self.image.strides[0], qformat)
        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setScaledContents(True)

    def stop_cam(self):
        if self.camOn:
            self.capture.release()
            self.camOn=False
            self.timer.stop()
            img=cv2.imread("reset.png")
            qformat = QImage.Format_RGB888
            img = QImage(img, img.shape[1], img.shape[0],img.strides[0], qformat)
            img = img.rgbSwapped()
            self.imgLabel.setPixmap(QPixmap.fromImage(img))
            self.imgLabel.setScaledContents(True)
            self.image=None
    
    def logoutYes(self):
        from login import Login
        self.window2 = Login()
        self.close()
        self.window2.show()
        
    def callPlayer(self):
        conn = sqlite3.connect('capstoneSQLDB.db')
        cur = conn.cursor()
        code=self.lineEdit.text()
        cur.execute('SELECT Loc FROM VidHistory WHERE Code = ? ', (code,))
        loc =cur.fetchone()
        if loc is not None:
            self.window3 = Player(loc[0])
            self.window3.resize(640,480)
            self.window3.show()
        cur.close()
        


def main():        
    app = QApplication(sys.argv)
    window=admin()
    window.setWindowTitle('ADMIN WINDOW')
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
