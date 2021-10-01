import cv2 as cv
import numpy as np
#yolov3 weights to be included
w=320
conf = 'cardetect/yolov3.cfg'
weights = 'cardetect/yolov3.weights'
net = cv.dnn.readNetFromDarknet(conf, weights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
layerNames = net.getLayerNames()
op = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
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
    z=0
    for i in finalIndex:
        i=i[0]
        t=bx[i]
        if(ids[i]<1 or ids[i]>7):
            z+=1
            continue
        cv.rectangle(img,(t[0],t[1]),(t[0]+t[2],t[1]+t[3]),(255,255,0),2)
    cv.putText(img,str(len(finalIndex-z)),(10,50),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),1)
    print(len(finalIndex-z))

# img=cv.imread('car1.jpg')
def processimg(read):
    read = cv.resize(read, (w, w))
    blob = cv.dnn.blobFromImage(read, 1 / 255, (w, w), [0, 0, 0], 1)
    net.setInput(blob)
    fwd = net.forward(op)
    findobj(fwd, read)
    return read
def getmarkedVideo(path="cardetect/test1.mp4"):
    cap=cv.VideoCapture(path)
    objecs=[]
    with open('cardetect/objects.txt', 'rt') as f:
        objecs=f.read().rstrip('\n').split('\n')
    # print(objecs)

    fourcc=cv.VideoWriter_fourcc(*"XVID")
    # writer=cv.VideoWriter('op2.avi',fourcc,10,(w,w))
    while cap.isOpened():
        _,read=cap.read()
        read2=processimg(read)
        # writer.write(read)
        # cv.imshow("try",read2)
        cv.waitKey(1)
        

getmarkedVideo()