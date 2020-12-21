import cv2
import pyzbar.pyzbar as pyzbar
import time


def capture():
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap.set(3, 440)
    cap.set(4, 380)
    while True:
        ret, frame = cap.read()
        decodedObj = pyzbar.decode(frame)
        for obj in decodedObj:
            print("data:", obj.data.decode())
            cv2.putText(frame, str(obj.data),(50,50), font, 0.9, (255,0,0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1)& 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


capture()
