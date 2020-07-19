import sqlite3
from datetime import datetime


def AddVideo(cam,loc):
    conn = sqlite3.connect('capstone.db')
    cur = conn.cursor()
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
    cur.close
    



##FOR TESTING
AddVideo(0,"H:\\Projects\\object detection using SSD\\sample\\funny_dog.mp4")
AddVideo(0,"H:\\Projects\\object detection using SSD\\sample\\horses_in_desert.mp4")