import sys
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot,QSize, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow,QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3
import cv2
from player import Player
from timeit import time
from datetime import datetime
import pickle
from plot_track import plot_trackers
from deep_sort_yolov3.main import yoloTracker
from deep_sort_yolov3.yolo import YOLO

class nuser(QMainWindow):
    def __init__(self):
        super(nuser,self).__init__()
        loadUi('nUser.ui',self)
        self.tabWidget.tabBar().setVisible(False)
        self.handleButtons()
        style = open('themes/darkblue.css' , 'r')
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
        self.trackStart.clicked.connect(self.callTracker) #*
        self.showPlot.clicked.connect(self.displayOutput) #*
        self.trackVideoShow.clicked.connect(self.playTrackedVid) #*
        
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
        conn = sqlite3.connect('capstoneSQLDB2.db')
        cur = conn.cursor()
        cur.execute("SELECT NAME FROM BLUEPRINTS")
        items=cur.fetchall()
        l=["BLUEPRINT"]
        self.blueprintSelect.clear() 
        for i in items:
            l.append(i[0])
        self.blueprintSelect.addItems(l)
        cur.close()

        
    def openLogout(self):
        self.stop_cam()
        self.tabWidget.setCurrentIndex(4)
    
    def show_Old_Vid(self):
        self.tabWidget.setCurrentIndex(2)
        conn = sqlite3.connect('capstoneSQLDB2.db')
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
            self.Vname="outputVideo\\"+str(time.time()).split(".")[0]+".mp4"
 
            i=0
            while i<22000:
                i+=1
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,self.video_size.width())
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,self.video_size.height())
            self.rec=cv2.VideoWriter(self.Vname,cv2.VideoWriter_fourcc(*'MJPG'),10, (self.video_size.width(),self.video_size.height())) 
            self.timer =QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(0.005)

    def update_frame(self):
        ret,frame=self.capture.read()
        if ret==True:
            self.rec.write(frame) 
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
        conn = sqlite3.connect('capstoneSQLDB2.db')
        cur = conn.cursor()
        loc="D:\\Projects\\CAPSTONE\\"+self.Vname
        cur.execute('SELECT Loc FROM VidHistory where loc=?',(loc,))
        temp=cur.fetchone()
        if temp is None:
            cur.execute('SELECT code FROM LCODE')
            code=cur.fetchone()
            cur.execute('UPDATE LCODE SET code = code + 1 WHERE code = ?',(code[0],))
            conn.commit()
            t=datetime.now()
            date=str(t.date())
            time=str(t.time())
            cur.execute('''INSERT INTO VidHistory (Code, Date, Time,Cam,Loc )
                        VALUES (?,?,?,?,?)''', (code[0],date,time,1,loc))
            conn.commit()
        cur.close()

    def stop_cam(self):
        if self.camOn:
            self.capture.release()
            self.rec.release()
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
        conn = sqlite3.connect('capstoneSQLDB2.db')
        cur = conn.cursor()
        code=self.lineEdit.text()
        cur.execute('SELECT Loc FROM VidHistory WHERE Code = ? ', (code,))
        loc =cur.fetchone()
        if loc is not None:
            self.window3 = Player(loc[0])
            self.window3.resize(640,480)
            self.window3.show()
        cur.close()
    
    def enableItems(self):
        self.listView_3.setEnabled(True)
        self.blueprintSelect.setEnabled(True)
        self.trackVideoShow.setEnabled(True)
        self.trackIDs.setEnabled(True)
        self.idList.setEnabled(True)
        self.showPlot.setEnabled(True)
    
    def disableItems(self):
        self.listView_3.setEnabled(False)
        self.blueprintSelect.setEnabled(False)
        self.trackVideoShow.setEnabled(False)
        self.trackIDs.setEnabled(False)
        self.idList.setEnabled(False)
        self.showPlot.setEnabled(False)
        pixmap = QPixmap('D:/Projects/CAPSTONE/reset.PNG')
        self.outputImg.setPixmap(pixmap)
        
# =============================================================================
#         img=cv2.imread("reset.png")
#         qformat = QImage.Format_RGB888
#         img = QImage(img, img.shape[1], img.shape[0],img.strides[0], qformat)
#         img = img.rgbSwapped()
#         self.outputImg.setPixmap(QPixmap.fromImage(img))
#         self.outputImg.setScaledContents(True)
# =============================================================================
    
    def callTracker(self):
        cam=self.camCode.text()
        vid=self.vidCode.text()
        if len(cam)==0 or len(vid)==0:
            self.trackStatus.setText("ENTER ALL MANDATORY FIELDS")
            self.disableItems()
        else:
            conn = sqlite3.connect('capstoneSQLDB2.db')
            cur = conn.cursor()
            cur.execute('SELECT loc FROM VidHistory WHERE Code=? AND Cam=?',(vid,cam,))
            loc=cur.fetchone()
            cur.close()
            if loc is None:
                self.trackStatus.setText("ENTER VALID CODE COMBINATION")
                self.disableItems()
            else:
                self.trackStatus.setText("TRACKING IN PROGRESS")
                yoloTracker(YOLO(),loc[0],"D:/Projects/CAPSTONE/outputVid.mp4")
                self.trackStatus.setText("TRACKING SUCCESFULLY DONE")
                f=open("D:/Projects/CAPSTONE/cordinates.pkl",'rb')
                d=pickle.load(f)
                l=list(d.keys())
                l.sort()
                self.idList.setRowCount(len(l))
                for i in range(len(l)):
                    self.idList.setItem(i,0, QTableWidgetItem(str(l[i])))
                self.enableItems()
                self.playTrackedVid()
            
    
    def displayOutput(self):
        blueprint=self.blueprintSelect.currentText()
        if blueprint=='BLUEPRINT':
            self.trackStatus.setText("SELECT A BLUEPRINT")
        else:
            ids=self.trackIDs.text()
            if len(ids)==0:
                self.trackStatus.setText("ENTER PEOPLE IDS FOR TRACKING")
            else:
                f=open("D:/Projects/CAPSTONE/cordinates.pkl",'rb')
                d=pickle.load(f)
                l=list(d.keys())
                l2=[]
                c=True
                ids=ids.split(",")
                for i in ids:
                    if i.isdigit() and (int(i) in l):
                        l2.append(int(i))
                    else:
                        c=False
                        break
                if c:
                    self.trackStatus.setText("")
                    conn = sqlite3.connect('capstoneSQLDB2.db')
                    cur = conn.cursor()
                    cur.execute('SELECT loc FROM blueprints WHERE name=?',(blueprint,))
                    loc=cur.fetchone()
                    cur.close()
                    plot_trackers(loc[0],l2)
                    pixmap = QPixmap('D:/Projects/CAPSTONE/plotted.jpg')
                    pixmap=pixmap.scaled(self.outputImg.size())
                    self.outputImg.setPixmap(pixmap)
                else:
                    self.trackStatus.setText("ENTER VALID IDs!")
                

    def playTrackedVid(self):
        #loc="D:/Projects/CAPSTONE/output3_yolov3S.mp4" ##FOR TESTING ONLY
        loc="D:/Projects/CAPSTONE/outputVid.mp4"
        self.window4=Player(loc)
        self.window4.resize(1280,960)
        self.window4.show()
        


def main():        
    app = QApplication(sys.argv)
    window=nuser()
    window.setWindowTitle('USER WINDOW')
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()
