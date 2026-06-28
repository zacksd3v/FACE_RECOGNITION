import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facedetection-9fcae-default-rtdb.firebaseio.com/"
})

ref = db.reference('Student')

data = {
    "20241": 
    {
        "name": "Muhammad Nasir",
        "deprt": "CMP",
        "time": "4-25-2024 02:30:00"
    }
}

for key, value in data.items():
    ref.child(key).set(value)