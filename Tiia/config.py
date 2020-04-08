STATUS="Status"
MESSAGE="Message"
KEY = "Key"
IP="192.168.42.68"


URL = "http://"+IP+":8000/"


'''
Installataion
------------------------------------
1.Django
2.DjangoRestFramework
    pip install djangorestframework
    pip install markdown
    pip install django-filter 
3.OpenCv
    pip install opencv-python
4.SpeechRecognition
    pip install SpeechRecognition
5.pyttsx3
    pip install pyttsx3
6.pywin32
    pip install pywin32

----------------------------


In terminal
first> python manage.py runserver 0.0.0.0:8000
then you get ip of your system in console, copy and replace it on config.py
In second terminal 
second> python detect.py
In third terminal 
third> python TextToSpeech.py
then see the UI, its all done
'''