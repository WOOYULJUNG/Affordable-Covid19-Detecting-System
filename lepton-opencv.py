from import_clr import *

clr.AddReference("ManagedIR16Filters")

from Lepton import CCI
from IR16Filters import IR16Capture, NewIR16FrameEvent, NewBytesFrameEvent
from System.Drawing import ImageConverter
from System import Array, Byte
from matplotlib import pyplot as plt
import numpy
import time
import cv2
from PIL import Image
import serial
arduino = serial.Serial('COM3', 9600)

lep, = (dev.Open()
        for dev in CCI.GetDevices())

print(lep.sys.GetCameraUpTime())

numpyArr = None
def getFrameRaw(arr, width, height):
    global numpyArr
    numpyArr = numpy.fromiter(arr, dtype="uint16").reshape(height, width)

capture = IR16Capture()
capture.SetupGraphWithBytesCallback(NewBytesFrameEvent(getFrameRaw))

capture.RunGraph()

while numpyArr is None:
    time.sleep(.1)

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
 
    return processed_img

temlist = []
mode = 0 #얼굴 찾기, 얼굴 찾음 후 , 이후대기

while True:
    capture = IR16Capture()
    capture.SetupGraphWithBytesCallback(NewBytesFrameEvent(getFrameRaw))
    arr=numpyArr.reshape(60,80,1)
    arr=arr/100
    arr=arr-290
    arr=arr*256//23
    arr2=arr
    arr = numpy.c_[arr, arr, arr]

    #
    arr2 = arr2.reshape(60, 80)
    image2 = Image.fromarray(arr2.astype('uint8'), 'L')
    img2 = numpy.array(image2)

    face_cascade = cv2.CascadeClassifier('C:/Python/haarcascade/haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(img2,1.1,3)
    
    for x, y, w, h in faces:
        #temp=(numpyArr[int(x + w/2)][int(y + h*4/5)]-27315)/100
        temp = (numpy.max(numpyArr)-27315)/100
        #print(temp)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #cv2.line(img2, (x + w//2, y + h*4//5), (x + w//2, y + h*4//5), (0, 0, 255), 1)
    #
            
    if mode == 2:
        print("문이 열렸습니다")
        time.sleep(5)
        mode = 0
    elif mode == 1:
        if len(faces)!=0:
            temlist.append(temp)
            print("온도 수집중.."+str(len(temlist)))
        if len(temlist)==5:
            mode = 2
            print(sum(temlist)/5)
            c= str(sum(temlist)/5)
            c= c.encode('utf-8')
            arduino.write(c)
            temlist = []
    elif len(faces)!=0:
        mode = 1
    else:
        print("정면을 향해 서세요")
        
    image = Image.fromarray(arr.astype('uint8'), 'RGB')
    img = numpy.array(image)
    new_screen = process_img(img)

    dst = cv2.resize(img, dsize=(0, 0), fx=5, fy=5, interpolation=cv2.INTER_LINEAR)
    dst2 = cv2.resize(img2, dsize=(0, 0), fx=5, fy=5, interpolation=cv2.INTER_LINEAR)
    dst3 = cv2.resize(new_screen, dsize=(0, 0), fx=5, fy=5, interpolation=cv2.INTER_LINEAR)

    #cv2.imshow("src", dst)
    cv2.imshow("src2", dst2)
    cv2.imshow('contour', dst3)

    cv2.waitKey(25)




