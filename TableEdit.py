import sqlite3
from datetime import datetime


def AddVideo(cam,loc):
    conn = sqlite3.connect('capstoneSQLDB2.db')
    cur = conn.cursor()
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
                    VALUES (?,?,?,?,?)''', (code[0],date,time,cam,loc))
        conn.commit()
    cur.close()
    

def DelVideo(code):
    conn = sqlite3.connect('capstoneSQLDB2.db')
    cur = conn.cursor()
    cur.execute('Delete FROM VidHistory where code= ?',(code,))
    conn.commit()
    cur.close()

def AddBlueprint(name,loc):
    conn = sqlite3.connect('capstoneSQLDB2.db')
    cur = conn.cursor()
    cur.execute('SELECT name FROM blueprints where name=?',(name,))
    temp=cur.fetchone()
    if temp is None:
        cur.execute('''INSERT INTO blueprints (name,loc )
                    VALUES (?,?)''', (name,loc))
        conn.commit()
    cur.close()


##FOR TESTING
"""AddVideo(0,"D:\\Projects\\object detection using SSD\\sample\\funny_dog.mp4")
AddVideo(0,"D:\\Projects\\object detection using SSD\\sample\\horses_in_desert.mp4")   

AddVideo(0,"D:/Projects/CAPSTONE/SAMPLES/video.mp4")
AddVideo(0,"D:/Projects/CAPSTONE/SAMPLES/video1.mp4")
AddVideo(0,"D:/Projects/CAPSTONE/SAMPLES/video2.mp4")

AddVideo(2,"D:/Projects/CAPSTONE/output3_yolov3S.mp4")

DelVideo(7)

DelVideo(3)
DelVideo(4)
DelVideo(5)

AddVideo(2,"D:/Projects/CAPSTONE/SAMPLES/video.mp4")
AddVideo(2,"D:/Projects/CAPSTONE/SAMPLES/video1.mp4")
AddVideo(2,"D:/Projects/CAPSTONE/SAMPLES/video2.mp4")
"""

#Blueprint testing
"""
AddBlueprint("bp 1","D:/Projects/CAPSTONE/blueprints/blueprint1.jpg")
AddBlueprint("bp 2","D:/Projects/CAPSTONE/blueprints/blueprint2.jpg")
AddBlueprint("bp 3","D:/Projects/CAPSTONE/blueprints/blueprint3.jpg")

AddVideo(2,"D:/Projects/CAPSTONE/SAMPLES/video5.mp4")
AddVideo(2,"D:/Projects/CAPSTONE/SAMPLES/video4.mp4")

AddVideo(2,"D:/Projects/CAPSTONE/SAMPLES/video5_2.mp4")

AddBlueprint("bp 4","D:/Projects/CAPSTONE/blueprints/blueprint4.jpg")
AddBlueprint("bp 5","D:/Projects/CAPSTONE/blueprints/blueprint5.jpg")"""
