import cv2
import pickle
import os
import face_recognition 
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {

    'databaseURL':"https://facedetection-9fcae-default-rtdb.firebaseio.com/",
    'storageBucket': "facedetection-9fcae.appspot.com"
})


# Importing Student Images.
folderPath = 'images'
pathList = os.listdir(folderPath)
# print(pathList)
imgList = []
studentIds = []

for path in pathList:
    img = cv2.imread(os.path.join(folderPath, path))
    img = cv2.resize(img, (300, 300))  # Resize the image to (400, 400)
    imgList.append(img)
    studentIds.append(os.path.splitext(path)[0])

    # wnn code dn zai mana uploadings dn images dn mu zuwa firebase-db
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    # nn wurin dole sai y zama upload_from_filename() BA upload_from_file b().
    blob.upload_from_filename(fileName)
    # print(path)
    # print(os.path.splitext(path)[0])
print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # munyi changing/coverting color anan.
        
        face_locations = face_recognition.face_locations(img)
       
        if not face_locations:
            print("No faces found in the image:", img)
            continue

        encode = face_recognition.face_encodings(img, [face_locations[0]])[0]
        # encode = face_recognition.face_encodings(img)[0] # munyi finding encoding dn mu anan.
        encodeList.append(encode)
    
    return encodeList

print('Encoding started.....')
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
# print(encodeListKnown)
print('Encoding completed!.....')

file = open('EncodeFile.p', 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print('File saved')
