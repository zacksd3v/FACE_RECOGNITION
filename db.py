import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {

    'databaseURL':"https://facedetection-9fcae-default-rtdb.firebaseio.com/",
    'storagrBucket': "facedetection-9fcae.appspot.com"
})

ref = db.reference('Students')
print("updating db....")
data = {
    "20241":
    {
        "name":"Muhammad Nasir",
        "matric_no":"PSC/2019/12345",
        "department":"Computer Science",
        "starting_year":2019,
        "total_attendance":6,
        "standing":"G",
        "years": 4,
        "last_attendance_time":"2024-04-26 00:54:34"
    }, 

    "20242":
    {
        "name":"Tukur Bello",
        "matric_no":"PSC/2019/12341",
        "department":"Computer Science",
        "starting_year":2019,
        "total_attendance":6,
        "standing":"G",
        "years": 4,
        "last_attendance_time":"2024-04-26 00:54:34"
    },

    "20243":
    {
        "name":"Arma Ya'u Bichi",
        "matric_no":"PSC/2019/12342",
        "department":"Agricultural Science",
        "starting_year":2000,
        "total_attendance":6,
        "standing":"F",
        "years": 5,
        "last_attendance_time":"2024-04-26 00:54:34"
    },

    "20244":
    {
        "name":"Yusuf Sirajo",
        "matric_no":"PSC/2019/12343",
        "department":"Computer Science",
        "starting_year":2009,
        "total_attendance":6,
        "standing":"G",
        "years": 4,
        "last_attendance_time":"2024-04-26 00:54:34"
    },

    "20245":
    {
        "name":"Zacks Bugs",
        "matric_no":"CSA/2019/12344",
        "department":"Cyber Security",
        "starting_year":2025,
        "total_attendance":6,
        "standing":"G",
        "years": 4,
        "last_attendance_time":"2024-04-26 00:54:34"
    }
}

for key, value in data.items():
    ref.child(key).set(value)
print("Updating Completed!!!")
