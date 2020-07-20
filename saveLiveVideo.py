import cv2 
  
video = cv2.VideoCapture(0) 
if (video.isOpened() == False):  
    print("Error reading video file") 

frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
size = (frame_width, frame_height) 
   
result = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'), 10, size) 
    
while(True): 
    ret, frame = video.read() 
    if ret == True:   
        result.write(frame)  
        cv2.imshow('Frame', frame)  
        if cv2.waitKey(1) & 0xFF == ord(' q'): 
            break
  
    # Break the loop 
video.release() 
result.release() 
    
# Closes all the frames 
cv2.destroyAllWindows() 
   
print("The video was successfully saved") 
