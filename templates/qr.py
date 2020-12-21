import cv2
import numpy as np
from pyzbar.pyzbar import decode
import winsound
import time

# img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)
cap.set(3, 340)
cap.set(4, 280)

with open('myDataFile.text') as f:
    myDataList = f.read().splitlines()

mylist = list()
myData = ""
while True:
    success, img = cap.read()
    for qrcode in decode(img):
        myData = qrcode.data.decode('utf-8')
        # print(myData)
        if myData not in mylist:
            mylist.append(myData)

        if myData in myDataList:
            myOutput = myData
            # 'Authorized'
            myColor = (0, 255, 0)
            
        else:
            myOutput = 'Un-Authorized'
            myColor = (0, 0, 255)

        pts = np.array([qrcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = qrcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myColor, 2)

    cv2.imshow('Result', img)
    # if myData:
    #     print(myData)
    #     time.sleep(3)
    #     break;
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

print(mylist)