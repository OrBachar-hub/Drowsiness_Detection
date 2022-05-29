from operator import itemgetter
import cv2
import winsound
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import pyttsx3
import sys
import datetime
from PyQt5.QtGui import QTextCursor
import cv2
import os
from keras.models import load_model
from pygame import mixer
import numpy as np 
from pygame.locals import *

def StartCamera(volume):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    mixer.init()
    sound = mixer.Sound('alarm.wav')
    lbl=['Close','Open']
    model = load_model('finalmodel.h5')
    leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')
    faceCascade = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
    path = os.getcwd()
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    count=0 
    score=0 
    thicc=2
    while(True):
        _, img = cap.read()
        height,width = img.shape[:2]
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        predictions = []
        left_eye = leye.detectMultiScale(img_gray)
        right_eye =  reye.detectMultiScale(img_gray)
        faces = faceCascade.detectMultiScale(img_gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        if len(faces) > 0:
            #   choose the closest face
            persons = [(x, y, w, h, w * h) for (x, y, w, h) in faces]
            #  Draw a rectangle around the faces
            (x, y, w, h) = max(persons, key=itemgetter(4))[:-1]
            # Draw a rectangle around the faces
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            for (ex,ey,ew,eh) in right_eye:
                cv2.rectangle(img, (ex,ey) , (ex+ew,ey+eh) , (250,0,0) , 1 )
                r_eye = img[ey:ey+eh, ex:ex+ew]
                r_eye = cv2.resize(r_eye, (32, 32))
                r_eye = np.array(r_eye)
                r_eye = np.expand_dims(r_eye, axis=0)
                ypred = model.predict(r_eye)
                ypred = np.argmax(ypred[0], axis=0)
                predictions.append(ypred)
            for (ex,ey,ew,eh) in left_eye:
                cv2.rectangle(img, (ex,ey) , (ex+ew,ey+eh) , (250,0,0) , 1 )
                l_eye = img[ey:ey+eh, ex:ex+ew]
                l_eye = cv2.resize(l_eye, (32, 32))
                l_eye = np.array(l_eye)
                l_eye = np.expand_dims(l_eye, axis=0)
                ypred = model.predict(l_eye)
                ypred = np.argmax(ypred[0], axis=0)
                predictions.append(ypred)
            if all(i==0 for i in predictions):
                score=score+1
                cv2.putText(img,"Closed",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
            else:
                score=score-1
                cv2.putText(img,"Open",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
            if(score<0):
                score=0   
            cv2.putText(img,'Score:'+str(score),(100,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
            if(score>6):
                cv2.imwrite(os.path.join(path,'image.jpg'),img)
                try:
                    sound.play()
                    speak(volume, "hey, wake up")
                except: 
                    pass
                if(thicc<20):
                    thicc= thicc+2
                else:
                    thicc=thicc-2
                    if(thicc<2):
                        thicc=2
                cv2.rectangle(img,(0,0),(width,height),(0,0,255),thicc) 
            cv2.imshow('frame',img)
            waitkey = cv2.waitKey(1)
            if waitkey & 0xFF == ord('q') or waitkey == ord('q') or waitkey == ord('Q'):
                cap.release()
                cv2.destroyAllWindows()
                break
def speak(volume, text,gender="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"):
    converter = pyttsx3.init()
    converter.setProperty('rate', 150)
    converter.setProperty('volume', volume)
    converter.setProperty('voice', gender)
    converter.say(text)
    converter.runAndWait()

class Ui_MainWindow():
    switch_window = QtCore.pyqtSignal()
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.gender_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        self.volume = 0.8

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        ##
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(600, 350, 121, 111))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.stopButton.setFont(font)
        self.stopButton.setStyleSheet("QPushButton {\n"
"    border-image: url(:/stop/stop.jpeg);\n"
"    color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 55px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }\n"
"border-image: url(:/stop/stop.jpeg);")
        self.stopButton.setText("Quit")
        self.stopButton.setObjectName("stopButton")
        ##
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(430, 350, 121, 111))
        self.playButton.setStyleSheet("QPushButton {\n"
"    border-image: url(:/play/play.jpeg);\n"
"    color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 55px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        self.playButton.setText("Play")
        self.playButton.setObjectName("playButton")
        font = QtGui.QFont()
        font.setPointSize(32)
        self.playButton.setFont(font)
        ##
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 801, 561))
        font = QtGui.QFont()
        font.setFamily("Kristen ITC")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.background.setFont(font)
        self.background.setAutoFillBackground(False)
        self.background.setStyleSheet("border-image: url(images/3.jpg);\n")
        self.background.setText("")
        self.background.setTextFormat(QtCore.Qt.RichText)
        self.background.setObjectName("background")
        self.welcome = QtWidgets.QLabel(self.centralwidget)
        self.welcome.setGeometry(QtCore.QRect(460, 100, 271, 91))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(55)
        font.setBold(True)
        font.setWeight(75)
        self.welcome.setFont(font)
        self.welcome.setAutoFillBackground(False)
        self.welcome.setObjectName("welcome")
        self.volumeButton = QtWidgets.QSlider(self.centralwidget)
        self.volumeButton.setGeometry(QtCore.QRect(490, 230, 171, 31))
        self.volumeButton.setMaximum(10)
        self.volumeButton.setSingleStep(1)
        self.volumeButton.setPageStep(10)
        self.volumeButton.setOrientation(QtCore.Qt.Horizontal)
        self.volumeButton.setObjectName("volumeButton")
        self.volumeLable = QtWidgets.QLabel(self.centralwidget)
        self.volumeLable.setGeometry(QtCore.QRect(520, 200, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Narkisim")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(50)
        self.volumeLable.setFont(font)
        self.volumeLable.setObjectName("volumeLable")
        self.background.raise_()
        self.stopButton.raise_()
        self.playButton.raise_()
        self.welcome.raise_()
        self.volumeButton.raise_()
        self.volumeLable.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.playButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.volumeButton.valueChanged.connect(self.valuechange)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Drowsiness Detection"))
        self.welcome.setText(_translate("MainWindow", "Welcome"))
        self.volumeLable.setText(_translate("MainWindow", "Volume"))

    def start(self):
        print("start")
        speak(self.volume, "are you ready? let's go")
        StartCamera(self.volume)

    def stop(self):
        print("stop")
        flag2 = False
        waitkey = ord('q')
        sys.exit()

    def male_voice(self):
        self.gender_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"

    def female_voice(self):
        self.gender_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

    def valuechange(self):
        self.volume = float(self.volumeButton.value()/10)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
