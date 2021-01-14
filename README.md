# CAPSTONE-PROJECT-Real-Time-Path-Detector-with-Survilance-System

In this project is focused to reduce individual people detection and their path tracking from video obtained from CCTV footages. 

The App uses PyQt5 for desktop app GUI, SQL lite Browser for database management and CCS templates for themes in GUI.  

The app has 2 separate app windows and layout of different types of user (admin: owner of system & normal user) and in build media player to see videos and live footages. Admin has extra functionalities than normal user, rest remaining the same.
A person can see live footages and archived videos, manage users, delete archived videos, change theme and track individuals in a given video.

For tracking induvial/s the user must specify the video using video code and camera number. 
The detection of individuals in a given video and their paths is done by processing the input video through a modified YOLO v3 model (modified using Pytorch, while having Tensorflow.Keras backend) having stacked up CNN and ANN layers, Computer Vision techniques and tracking algorithm: Deepsort Algorithm.

After the processing of video, an output video showing uniquely identified individuals having unique tracker ids along with color. In video the path over last 30 frames of each individual can be seen.

All the ids and the corresponding centers of detection boxes in all instances are stored in a pickle file. These are later used to show/plot a single or more person/s movements on the blueprint (where camera was situated). The people whose path is to be plotted on blueprint, their unique ids has to be entered by the user.

See screenshots and final submission folders for outputs and better insight on the work and outputs
