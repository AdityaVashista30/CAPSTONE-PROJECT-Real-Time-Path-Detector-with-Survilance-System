
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import pickle

#DUMMY BLUPRINT GENRATION
"""
vid=cv2.VideoCapture('output3_yolov3S.mp4')
whiteFrame = 255 * np.ones((int(vid.get(4)),int(vid.get(3)),3), np.uint8)
cv2.imwrite('blueprint1.jpg',whiteFrame)


vid=cv2.VideoCapture('D:/Projects/CAPSTONE/SAMPLES/video2.mp4')
whiteFrame = 255 * np.ones((int(vid.get(4)),int(vid.get(3)),3), np.uint8)
cv2.imwrite('blueprint2.jpg',whiteFrame)


vid=cv2.VideoCapture('D:/Projects/CAPSTONE/SAMPLES/video.mp4')
whiteFrame = 255 * np.ones((int(vid.get(4)),int(vid.get(3)),3), np.uint8)
cv2.imwrite('blueprint3.jpg',whiteFrame)
"""

def plot_trackerSingle(blueprint,id):
    f=open("D:/Projects/CAPSTONE/cordinates.pkl",'rb')
    d=pickle.load(f)
    img = Image.open(blueprint)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    xC=[]
    yC=[]
    for i in d[id]:
        xC.append(i[0])
        yC.append(i[1])
    rgb=np.random.rand(3,)
    #plt.scatter(x=xC, y=yC, c=[rgb], s=40)
    plt.scatter(x=xC, y=yC, c=[rgb])
    #print(rgb)
    plt.savefig("plotted.jpg",bbox_inches="tight",pad_inches=0.02,dpi=250)
    #plt.show()

def plot_trackers(blueprint,id_list):
    f=open("D:/Projects/CAPSTONE/cordinates.pkl",'rb')
    d=pickle.load(f)
    img = Image.open(blueprint)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    color=[]
    for i in id_list:
        xC=[]
        yC=[]
        for j in d[i]:
            xC.append(j[0])
            yC.append(j[1])
            
        rgb=np.random.rand(3,)
        while(list(rgb) in color):
            rgb=np.random.rand(3,)
        color.append(list(rgb))
        plt.scatter(x=xC, y=yC,s=10, c=[rgb],label=('Person '+str(i)))
        
    plt.legend()
    plt.savefig("plotted.jpg",bbox_inches="tight",pad_inches=0.02,dpi=250)
    #plt.show()
    
#plot_trackerSingle("blueprint1.jpg",21)
#plot_tracker("blueprint1.jpg",1)
 
#multiple people trackers test cases
"""
plot_trackers("blueprint1.jpg",[21])   
plot_trackers("blueprint1.jpg",[21,1])   
plot_trackers("blueprint1.jpg",[21,1,10])   
plot_trackers("blueprint1.jpg",[21,1,10,22,30])
plot_trackers("blueprint1.jpg",[21,1,30,3])      
"""

#EXTRA blueprints
"""
vid=cv2.VideoCapture('D:/Projects/CAPSTONE/SAMPLES/video4.mp4')
whiteFrame = 255 * np.ones((int(vid.get(4)),int(vid.get(3)),3), np.uint8)
cv2.imwrite('D:/Projects/CAPSTONE/blueprints/blueprint4.jpg',whiteFrame)

vid=cv2.VideoCapture('D:/Projects/CAPSTONE/SAMPLES/video5.mp4')
whiteFrame = 255 * np.ones((int(vid.get(4)),int(vid.get(3)),3), np.uint8)
cv2.imwrite('D:/Projects/CAPSTONE/blueprints/blueprint5.jpg',whiteFrame)
    """