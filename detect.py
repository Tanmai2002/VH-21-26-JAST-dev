import cv2 as cv
import numpy as np
path="C:\\Users\\tanma\\Desktop\\myprograms\\VSCODE\\JAST Hack\\VH-21-26-JAST-dev\\cars.xml"
cascade=cv.CascadeClassifier(path)
img=cv.imread('car1.jpg')
cap=cv.VideoCapture("C:\\Users\\tanma\\Desktop\\myprograms\\VSCODE\\JAST Hack\\VH-21-26-JAST-dev\\test1.mp4")
while cap.isOpened():
    _,read=cap.read()
    read=cv.resize(read,(416,416))
    
    imgBW=cv.cvtColor(read,cv.COLOR_BGR2GRAY)
    det=cascade.detectMultiScale(imgBW,1.1,4)
    for (x,y,w,h) in det:
        cv.rectangle(read,(x,y),(x+w,y+h),(255,255,0),2)

    cv.imshow("try",read)
    cv.waitKey(1)
img=cv.resize(img,(416,416))
imgBW=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
det=cascade.detectMultiScale(imgBW,1.1,5)
print(det)
for (x,y,w,h) in det:
    cv.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
cv.imshow('test',imgBW)
cv.waitKey(0)