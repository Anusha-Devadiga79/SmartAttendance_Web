# SmartAttendance_Web
A facial recognition-based Smart Attendance System using Python, OpenCV, Flask, and Google Sheets. Features real-time face detection, admin dashboard, shortage tracking, and dual attendance storage (Excel + Google Sheets). Developed by Anusha Devadiga and team for academic use.

# Smart Attendance System using Face Recognition 🎓📸

A real-time facial recognition-based attendance management system built with Python, OpenCV, Flask, and Google Sheets.  
This system allows educational institutions to automate attendance and manage records efficiently through a secure admin dashboard.

> ⚠️ **Note**: The `data/` folder containing student face images is not included in this repository to ensure privacy.

---

## 🚀 Key Features

- 🔐 **Admin Dashboard** – Secure login with access to all attendance functions.
- 📷 **Real-Time Face Recognition** – Uses a webcam to recognize students and mark attendance.
- 📊 **Dual Storage** – Stores attendance in both Excel and Google Sheets.
- 📆 **Daily Tracking** – Automatically creates or updates columns based on current date.
- 🟢 **Manual or Scheduled** – Attendance can be triggered manually or set for a specific time.
- 📉 **Shortage Tracking** – Displays students with low attendance.
- ❌ **Absent List** – Lists today's absentees.
- ➕ ➖ **Add/Remove Student** – Easy interface to update the student database.

---

## 🗂️ Project Structure

```

SmartAttendanceSystem/
│
├── app.py                # Flask-based admin interface
├── chat.py               # Attendance script using face recognition
├── camera.py             # For adding new student face data
├── templates/            # HTML files for dashboard and views
│   ├── index.html
│   ├── dashboard.html
│   ├── absentees.html
│   ├── shortage.html
│   ├── add\_student.html
│   ├── remove\_student.html
│   └── taking\_attendance.html
├── requirements.txt      # Dependencies
└── README.md             # Project info (you are here)

````

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Anusha-Devadiga79/SmartAttendance_Web.git
cd SmartAttendance_Web
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Google Sheets API Credentials

Place your Google API credentials JSON file and update the path in `chat.py`.

---

## 🧪 How to Use

### ➕ Add a Student

```bash
python camera.py
```

### 🟢 Start Attendance (Manual)

```bash
python chat.py
```

### 🌐 Launch Admin Dashboard

```bash
python app.py
```

---

## 🧾 Admin Dashboard Functionalities

| Feature             | Description                            |
| ------------------- | -------------------------------------- |
| 🔒 Login            | Admin-only access                      |
| 👥 View Absentees   | Shows students who were not recognized |
| 📉 Shortage List    | Displays students with low attendance  |
| ➕ Add Student       | Capture face and register new student  |
| ➖ Remove Student    | Delete student from database           |
| 🟢 Start Attendance | Trigger attendance manually            |
| 🖨️ Print Reports   | (Coming Soon) Export data for printing |

---

## 👨‍💻 Developed By

This project was developed as part of our academic work by:

* **Anusha Devadiga**
* **Sahana Patil**
* **Anusha Hakati**

*BCA, Bharatesh College of Computer Applications*
*Academic Year: 2024–2025*

---

## 🔒 Privacy Notice

This system involves facial data. Please ensure proper consent is obtained before collecting or processing face images.
The `data/` folder containing images is excluded from this public repository to respect privacy.

---

## 📄 License

This project is released for **educational and non-commercial use only**.
Please contact the authors if you wish to reuse it for other purposes.
