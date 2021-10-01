import cv2 as cv
import numpy as np
w=320
def findobj(outputs,img):
    hi,wi,c=img.shape
    bx=[]
    ids=[]
    confidence=[]
    nms=0.4
    for outp in outputs:
        for det in outp:
            prob=det[5:]
            id=np.argmax(prob)
            conf=prob[id]
            if conf>0.75:
                w,h=int(det[2]*wi),int(det[3]*hi)
                x,y=int(det[0]*wi-w/2),int(det[1]*hi-h/2)
                bx.append((x,y,w,h))
                ids.append(id)
                confidence.append(float(conf))
        # print(len(ids))
    finalIndex=cv.dnn.NMSBoxes(bx,confidence,0.75,nms)
    for i in finalIndex:
        i=i[0]
        t=bx[i]
        cv.rectangle(img,(t[0],t[1]),(t[0]+t[2],t[1]+t[3]),(255,55,0),2)
        print()

img=cv.imread('car1.jpg')
cap=cv.VideoCapture("cardetect/test1.mp4")
objecs=[]
with open('cardetect/objects.txt', 'rt') as f:
    objecs=f.read().rstrip('\n').split('\n')
print(objecs)
conf='cardetect/yolov3.cfg'
weights='cardetect/yolov3.weights'
net=cv.dnn.readNetFromDarknet(conf,weights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
layerNames=net.getLayerNames()
op=[layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

while cap.isOpened():
    _,read=cap.read()

    read=cv.resize(read,(w,w))
    blob=cv.dnn.blobFromImage(read,1/255,(w,w),[0,0,0],1)
    net.setInput(blob)
    fwd = net.forward(op)
    findobj(fwd,read)
    imgBW=cv.cvtColor(read,cv.COLOR_BGR2GRAY)
    cv.imshow("try",read)
    cv.waitKey(1)
