import cv2
import pyttsx3
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from Project.models import *
from Project.serializer import *


def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--image')
    #
    # args = parser.parse_args()
    # print("Recieved args : ", args)
    # print("Recieved args type : ", type(args.image))

    faceProto = "opencv_face_detector.pbtxt"
    faceModel = "opencv_face_detector_uint8.pb"
    ageProto = "age_deploy.prototxt"
    ageModel = "age_net.caffemodel"
    genderProto = "gender_deploy.prototxt"
    genderModel = "gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    # video = cv2.VideoCapture(args.image if args.image else 0)
    video = cv2.VideoCapture(0)
    # video=cv2.VideoCapture('fz.jpg')  #file name
    padding = 20
    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break

        resultImg, faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            print("No face detected")

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1] - padding):
                         min(faceBox[3] + padding, frame.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                        :min(faceBox[2] + padding, frame.shape[1] - 1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
            print(f'Gender: {gender}')

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]
            print(f'Age: {age[1:-1]} years')

            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2, cv2.LINE_AA)
            # cv2.imshow("Detecting age and gender", resultImg)
            print("Sucess")

            return {'age':age,'gender':gender}


class DetectView(ListAPIView):
    serializer_class = AdsSerializer
    def put(self,request):
        return Response(
            {
                "Status":False,
                "Message":"Not Ready"
            }
        )
        print("Starting detection module ")
        os.system("python ./Project/detect.py")


        return Response(
            {
                "Status":True,
                "Message":"Detection mode started"
            }
        )
    def get_queryset(self):
        # data = main()
        data = Ads.objects.all()
        return data

        # os.system("python ./Project/detect.py")

        # return Response(
        #     {
        #         "Status":True,
        #         "age":data.age,
        #         "gender":data.gender,
        #         "you":data.you,
        #         "bot":data.bot,
        #     }
        # )


    def post(self,request):
        print("Recieved ",self.request.POST)
        obj = Ads.objects.first()

        if self.request.POST.get("Key") == "image":
            print("Image data recieved ")
            age=self.request.POST.get('age')
            gender=self.request.POST.get('gender')
            gend = gender.lower()
            if gend =="male":
                gend="m"
            else:
                gend="f"

            obj.age=age
            obj.gender=gend
        elif self.request.POST.get("Key") == "voice":
            print("Voice data recieved ")

            you = self.request.POST.get('you')
            bot = self.request.POST.get('bot')
            print("You > ",you)
            print("Jasi > ",bot)
            obj.you = you
            obj.bot = bot
        obj.save()
        print("Saved ")


        return Response(
            {
                "Status":True,
                "message":"Saved"
            }
        )

class AdverticementView(ListAPIView):
    serializer_class = AdsSerializer
    def get_queryset(self):
        qs = Adverticements.objects.all()
        return qs



def speak(audioString):
    print(audioString)

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    voice = engine.getProperty('voice')

    engine.setProperty('rate', rate - 70)
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")

    engine.say(audioString)
    engine.runAndWait()
    #
    # print(audioString)
    # # tts = gTTS(text=audioString, lang='en')
    #
    # engine = pyttsx3.init()
    # engine.say(audioString)
    # engine.runAndWait()

class Announce(ListAPIView):
    serializer_class = AnnouncementSerializer
    def get_queryset(self):
        queryset = Announcement.objects.filter(id=1)
        return queryset
    def post(self,request):
        message = self.request.POST.get("message")
        speak(message)
        return Response(
            {
            "Status":True,
            "Message":"Announce completed",
            }
        )