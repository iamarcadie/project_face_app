import cv2
import os
import sys
import argparse as arg
import numpy as np
from face_detect import *
class Recognizer():
    def __init__(self,cascadePath,train_file,lbph_var):
        self._Face_Cascade = cv2.CascadeClassifier(cascadePath)
        self._Recognizer = cv2.face.LBPHFaceRecognizer_create(lbph_var[0], 
            lbph_var[1], lbph_var[2], lbph_var[3])
        self._Recognizer.read(train_file)
    def Draw_Rect(self,Image,face,color):
        x,y,w,h = face
        # line 1 : top left corner horizontal line 
        cv2.line(Image, (x, y), (int(x + (w/5)),y), color, 2)
        # line 2 : top right corner horizontal line 
        cv2.line(Image, (int(x+((w/5)*4)), y), (x+w, y), color, 2)
        # line 3 : top left corner vertical line 
        cv2.line(Image, (x, y), (x,int(y+(h/5))), color, 2)
        # line 4 : top right corner vertical line 
        cv2.line(Image, (x+w, y), (x+w, int(y+(h/5))), color, 2)
        # line 5 : bottom left corner vertical line 
        cv2.line(Image, (x, int(y+(h/5*4))), (x, y+h), color, 2)
        # line 6 : bottom left corner horizontal line 
        cv2.line(Image, (x, int(y+h)), (x + int(w/5) ,y+h), color, 2)
        # line 6 : bottom right corner horizontal line 
        cv2.line(Image, (x+int((w/5)*4), y+h), (x + w, y + h), color, 2)
        # line 6 : bottom right corner verticals line 
        cv2.line(Image, (x+w, int(y+(h/5*4))), (x+w, y+h), color, 2) 
    def FileRead(self):
        NAME = []  
        with open("users_name.txt", "r") as f :                      
            for line in f:         
                NAME.append (line.split(",")[1].rstrip())
        return NAME      
    def DispID(self,face, NAME, Image):
        x, y, w, h = face
        pt1 = (int(x + w/2.0 -50), int(y+h+40))
        pt2 = (int(x + w/2.0 +50),int(y+h+65))
        pt3 = (int(x + w/2.0 -46), int(y+h +(-int(y+h) + int(y+h+25))/2+48))
        triangle_cnt = np.array( [(int(x+w/2.0),int(y+h+10)),
            (int(x+w/2.0 -20),int(y+h+35)), 
            (int(x+w/2.0 +20),int(y+h+35))] )
        cv2.drawContours(Image, [triangle_cnt], 0, (255,255,255), -1)
        cv2.rectangle(Image,pt1, pt2, (255,255,255), -1)          
        cv2.rectangle(Image, pt1, pt2, (0,0,255), 1) 
        cv2.putText(Image, NAME ,pt3 , cv2.FONT_HERSHEY_PLAIN, 1.1, (0,0,255))  
    def Get_UserName(self,ID, conf):
        #print("[INFO] Confidence: " + "{:.2f} ".format(conf))
        if not ID > 0:
            return " Unknown "
        return self.FileRead()[ID -1]     
    def predict(self,img,skin_face_detector,size1,size2):
        if img is None:
            print("[INFO] Reaching the end of the video")
            print("[INFO] Exiting...") 
            return
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray1 = gray.copy()
        #gray = cv2.equalizeHist(gray)
        gray = cv2.resize(gray, (0,0), fx=1/3, fy=1/3)
        faces = self._Face_Cascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=4,minSize=(30, 30))
        if len(faces) == 0 :
            img1 = cv2.resize(img, (0,0), fx=1/3, fy=1/3)
            faces = skin_face_detector.Detect_Face_Img(img1,size1,size2)
        for _,face in enumerate(faces):
            self.Draw_Rect(img, face*3, [0,255,0])
            x,y,w,h = face*3
            id1, conf = self._Recognizer.predict(gray1[y:y + h, x:x + w])
                # Check that the face is recognized
            if (conf >100): 
                self.DispID(face*3, self.Get_UserName(0, conf), img) 
            else:
                self.DispID(face*3, self.Get_UserName(id1, conf), img)   
        return img
def Arg_Parse():
    Arg_Par = arg.ArgumentParser()
    Arg_Par.add_argument("-v", "--video",
                    help = "path of the video or if not then webcam")
    Arg_Par.add_argument("-c", "--camera",
                    help = "Id of the camera")
    arg_list = vars(Arg_Par.parse_args())