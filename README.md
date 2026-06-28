# Face Recognition Attendance Management System 🤖📸

A real-time, smart attendance management system that uses **Computer Vision (OpenCV)** and deep learning-based **Face Recognition** to automate student attendance. The project is tightly integrated with **Firebase** for cloud data architecture and profile asset storage.

---

## ✨ Features

- **Real-Time Face Detection**: Captures live video feeds and maps facial biometrics instantaneously.
- **High-Accuracy Face Matching**: Utilizes a deep learning vector distance engine to match current live frames against pre-encoded student profiles.
- **Dynamic Graphical Layer UI**: Overlays dynamic bounding box corners on detected faces using `cvzone` and renders active layout frames.
- **Firebase Cloud Database**: Real-time integration to sync and download student metadata (Name, Matric No, Department, Standing, Academic Year).
- **Firebase Cloud Storage Fetching**: Dynamically downloads and decodes student avatar imagery payloads straight into the active stream frame.
- **Anti-Spam Attendance Lockout**: Features a 30-second localized cooldown check per student to prevent consecutive duplicate attendance logging.
- **State-Driven Display Modes**: Rotates across active, loading, marked, and cooldown UI layout states dynamically based on recognition events.

---

## 🛠️ Architecture & Core Dependencies

- **Programming Language**: Python 3.x
- **Core Frameworks**:
  - `opencv-python`: Handles hardware video capture matrices and real-time graphics injection.
  - `face-recognition`: High-accuracy face localization and biometric 128-d encoding engine.
  - `firebase-admin`: Handles asynchronous pipeline requests to Google Firebase RTDB and Storage buckets.
  - `cvzone`: Injects stylized bounding layouts and modular textual blocks.
  - `numpy`: Executes structural matrix manipulations and array byte conversion algorithms.

---

## 🚀 How It Works (Internal Blueprint)

1. **Biometric Matrix Comparison**: Live frames are scaled down (`0.25x`) and converted from BGR to RGB format to accelerate CPU face location scanning.
2. **Euclidean Distance argmin Engine**: `face_recognition.face_distance` returns vector scores. The script passes this through `np.argmin()` to isolate the lowest error index value, matching the structural profile ID.
3. **Firebase State Synchronization**: Upon a valid true-match event, the application initializes a thread to fetch demographic node blocks (`Students/{id}`). 
4. **Time Delta Verification**: It parses the `last_attendance_time` timestamp string into a `datetime` object. If `total_seconds() > 30`, it increments the attendance counter database property globally and updates the network cluster.
5. **Dynamic Frame Ingestion**: The system continuously maps raw coordinate blocks to splice graphics onto the target positions of your background asset (`resources/bg_edit.png`).

---

## 📥 Getting Started & Configuration

### Prerequisites
Ensure your device has Python 3.9+ installed along with CMake (required to compile the native standard C++ `dlib` library).

### 1. Project Directory Structure
Make sure your file structure contains the required binary cache files and graphic modules:
```text
├── main.py                   # The execution script provided above
├── serviceAccountKey.json    # Your private Firebase configuration credentials file
├── EncodeFile.p              # Binary pickle cache bundle containing known structural face encodings
└── resources/
    ├── bg_edit.png           # Master canvas layout file
    └── modes/                # Mode configuration asset folders
```

### 2. Dependency Installation
Execute this block inside your target terminal environment:
```bash
pip install opencv-python numpy face-recognition firebase-admin cvzone
```

### 3. Execution
Provide your `serviceAccountKey.json` inside the root tree directory, then boot the processing stream:
```bash
python main.py
```
*Press **'q'** on your keyboard at any point during execution to gracefully kill open threads and kill visual windows.*

---

## 🛡️ License & Credit
Distributed under the MIT License.

**Powered by RNG Tech-301** 🚀
s