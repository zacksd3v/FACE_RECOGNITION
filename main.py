import os
import cv2
import numpy
import cvzone
import pickle
import numpy as np
import firebase_admin
import face_recognition
from firebase_admin import db
from datetime import datetime
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {

    'databaseURL':"https://facedetection-9fcae-default-rtdb.firebaseio.com/",
    'storageBucket': "facedetection-9fcae.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread("resources/bg_edit.png")
imgSize = cv2.resize(imgBackground, (0, 0), fx=0.6, fy=0.6)

# Importing Images Modes.
folderModePath = 'resources/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgMode = cv2.imread(os.path.join(folderModePath, path))
    imgMode = cv2.resize(imgMode, (300, 300))  # Resize the image to (400, 400)
    imgModeList.append(imgMode)

# Za muyi importing encode file din mu anan.
print('Loading Encoded file......')
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print('Encoded files loaded...')

modeType = 0
counter = 0
id = -1

while True:
    success, img = cap.read()

    # Ann zamuyi resizing images dn mu.
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) # munyi changing/coverting color anan.

    # wnn code dn yana ditecting current face.
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    img_resized = cv2.resize(img, (600, 400))  # Resize the image to a slightly smaller size
    imgSize[140:140 + 400, 60:60 + 600] = img_resized # Frame size na Camera

    imgSize[65:65 + 500, 770:770 + 300] = cv2.resize(imgModeList[modeType], (300, 500)) # Frame size na Modes
    
    # wann code yana detecting correct face ne. snn yana zama True based on small number da yayi printing.
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print('matches', matches)
            # print('faceDis', faceDis)

            # Idan face dn mutum yyi detecting, zai bamu matche 0
            matchesIndex = np.argmin(faceDis)
            print('matches', matchesIndex)

            if matches[matchesIndex]:
                # print('Known Face Detected!')
                # print(studentIds[matchesIndex])

                # wnn code din shine na rectangle din dake ditecting face na mutum.
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 60 + x1, 140 + y1, x2 - x1, y2 - y1 # wnn lissafin sae yyi dai-dai da na imgBackground dn k.
                imgSize = cvzone.cornerRect(imgSize, bbox, rt=0)
                id = studentIds[matchesIndex]

                if counter == 0:
                    cvzone.putTextRect(imgSize, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgSize)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
                    imgStudent = []

        if counter != 0:
            if counter == 1: 
                # Daga nn muke downloading daga firebase db student data.
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # Daga nn muke getting student images dga firebase storage.
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Ann zamuyi updating studentInfo
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], 
                                                "%Y-%m-%d %H:%M:%S")

                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgSize[65:65 + 500, 770:770 + 300] = cv2.resize(imgModeList[modeType], (300, 500)) # Frame size na Modes
        
            if modeType != 3:
                
                if 10 < counter  < 20:
                    modeType = 2

                imgSize[65:65 + 500, 770:770 + 300] = cv2.resize(imgModeList[modeType], (300, 500)) # Frame size na Modes

                if counter <= 10:
                    cv2.putText(imgSize, str(studentInfo['total_attendance']), (840, 100), 
                                cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                    cv2.putText(imgSize, str(studentInfo['matric_no']), (899, 388), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgSize, str(studentInfo['department']), (860, 455), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgSize, str(studentInfo['standing']), (860, 540), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgSize, str(studentInfo['starting_year']), (1030, 540), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgSize, str(studentInfo['years']), (940, 540), 
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1) 
                    offset = (414 - w) // 2
                    cv2.putText(imgSize, str(studentInfo['name']), (715 + offset, 340), 
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    
                    imgSize[110:110 + 200, 838:838 + 200] = imgStudent

                counter += 1
    
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgSize[65:65 + 500, 770:770 + 300] = cv2.resize(imgModeList[modeType], (300, 500)) # Frame size na Modes
    else:
        modeType = 0
        counter = 0
    cv2.imshow("Attendance Face Recognition Management System", imgSize)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release
cv2.destroyAllWindows()

