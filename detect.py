#A Gender and Age Detection program by Mahesh Sawant
# from time import time as currentTime
import time
from statistics import mode

import requests
import cv2
import math
import argparse
from Tiia.config import *

print(STATUS)

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes


parser=argparse.ArgumentParser()
parser.add_argument('--image')

args=parser.parse_args()
print("Recieved args : ",args)
print("Recieved args type : ",type(args.image))

faceProto="opencv_face_detector.pbtxt"
faceModel="opencv_face_detector_uint8.pb"
ageProto="age_deploy.prototxt"
ageModel="age_net.caffemodel"
genderProto="gender_deploy.prototxt"
genderModel="gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

video=cv2.VideoCapture(args.image if args.image else 0)
# video=cv2.VideoCapture(args.image if args.image else 0)
# video=cv2.VideoCapture('fz.jpg')  #file name

padding=20

age_list = []
gender_list = []
last_recorded_time = time.time()
delta = 0

while cv2.waitKey(1)<0 :
    curr_time = time.time()
    if curr_time - last_recorded_time >= 2.0:  # it has been at least 2 seconds
        # NOTE: ADD SOME STATEMENTS HERE TO PROCESS YOUR IMAGE VARIABLE, img
        try:
            # print("agelist", age_list)
            # print("gender list", gender_list)
            age=mode(age_list)
            gender = mode(gender_list)
            print("Age ",age)
            print("Gender ",gender)
            # print("3s reached")
            age_list.clear()
            gender_list.clear()

            API_ENDPOINT = URL+"detect/"

            data = {
                'age':age,
                'gender': gender,
                KEY:"image"
            }
            r = requests.post(url=API_ENDPOINT, data=data)

            # IMPORTANT CODE BELOW
            last_recorded_time = curr_time
            # time.sleep(1)
        except Exception as e:
            print("Excepction ",e)


    hasFrame,frame=video.read()
    if not hasFrame:
        cv2.waitKey()
        break
    
    resultImg,faceBoxes=highlightFace(faceNet,frame)
    if not faceBoxes:
        print("No face detected")



    for faceBox in faceBoxes:
        face=frame[max(0,faceBox[1]-padding):
                   min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                   :min(faceBox[2]+padding, frame.shape[1]-1)]
        blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds=genderNet.forward()
        gender=genderList[genderPreds[0].argmax()]
        # print(f'Gender: {gender}')

        ageNet.setInput(blob)
        agePreds=ageNet.forward()
        age=ageList[agePreds[0].argmax()]
        # print(f'Age: {age[1:-1]} years')

        cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
        # cv2.imshow("Detecting age and gender", resultImg)
        # print("Sucess")

        age_list.append(age)
        gender_list.append(gender)

        # API_ENDPOINT = URL+"detect/"
        #
        # data = {
        #     'age':age,
        #     'gender': gender,
        #     KEY:"image"
        # }
        # r = requests.post(url=API_ENDPOINT, data=data)
        # time.sleep(3)