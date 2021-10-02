import cv2 as cv
import numpy as np
#yolov3 weights to be included
w=608
conf = 'cardetect/yolov3.cfg'
weights = 'cardetect/yolov3.weights'
net = cv.dnn.readNetFromDarknet(conf, weights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
layerNames = net.getLayerNames()
op = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
def findobj(outputs,img,noOfRoads=1):
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
    z=[0]*noOfRoads
    for i in finalIndex:
        i=i[0]
        t=bx[i]
        if(ids[i]<1 or ids[i]>7):
            continue
        for i in range(noOfRoads):
            if (wi/noOfRoads)*(i+1)>t[0]:
                z[i]+=1
                break
        cv.rectangle(img,(t[0],t[1]),(t[0]+t[2],t[1]+t[3]),(255,255,0),2)
    cv.putText(img,str(z),(10,50),cv.FONT_HERSHEY_PLAIN,2,(255,0,255),1)
    print(str(z))

def processimg(read):
    read = cv.resize(read, (w, w))
    # cv.line(read,(w//2,0),(w//2,w),(0,255,255),1)
    blob = cv.dnn.blobFromImage(read, 1 / 255, (w, w), [0, 0, 0], 1)
    net.setInput(blob)
    fwd = net.forward(op)
    findobj(fwd, read,2)
    return read
def getmarkedVideo(path="cardetect/test3.mp4"):
    cap=cv.VideoCapture(path)
    # print(objecs)
    fourcc=cv.VideoWriter_fourcc(*"h264")
    writer=cv.VideoWriter('static/videos/compiled.mp4',fourcc,20.0,(w,w))
    while cap.isOpened():
        t,read=cap.read()
        if not t:
            break
        read2=processimg(read)

        #TO show or write in another video
        writer.write(read2)
        cv.imshow("try",read2)
        if cv.waitKey(1)==ord('q') & 0xFF:
            break
    writer.release()
    cap.release()
    cv.destroyAllWindows()
if __name__=="__main__":
    getmarkedVideo()