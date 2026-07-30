# 🚦 Smart Traffic Monitoring System

## AI Powered Real-Time Vehicle Analytics Platform

An intelligent traffic monitoring system powered by **YOLO Object Detection**, **ByteTrack Object Tracking**, and **Streamlit Dashboard** for real-time vehicle analytics.

The system detects and tracks vehicles, counts traffic flow, estimates vehicle speed, detects violations, analyzes traffic density, and stores all monitoring data in an SQLite database.

---

# 📌 Project Overview

Smart Traffic Monitoring System is an AI-based computer vision solution designed to automate traffic surveillance and provide real-time analytics.

The system uses deep learning and computer vision techniques to analyze traffic videos and generate useful insights such as:

* Vehicle count
* Vehicle classification
* Entry and exit monitoring
* Speed estimation
* Overspeed violation detection
* Traffic density analysis
* Emergency vehicle priority handling
* Interactive analytics dashboard

---

# ✨ Features

## 🚗 AI Vehicle Detection

* Real-time object detection using YOLO
* Detects multiple vehicle categories:

  * 🚙 Cars
  * 🚚 Trucks
  * 🚌 Buses
  * 🏍 Motorcycles

---

## 🎯 Object Tracking

Implemented:

* ByteTrack tracking algorithm
* Unique vehicle ID assignment
* Vehicle movement tracking
* Duplicate counting prevention

---

## 📊 Vehicle Counting

The system provides:

* Total vehicle count
* Class-wise vehicle statistics

Example:

```
Cars        : 49
Trucks      : 3
Bus         : 2
Motorcycle  : 0
```

---

## 🚦 Entry / Exit Monitoring

AI-based virtual line crossing system:

* Vehicle entry detection
* Vehicle exit detection
* Traffic flow analysis

---

## ⚡ Speed Estimation

Features:

* Real-time vehicle speed calculation
* Pixel-to-meter calibration
* Overspeed detection

Example:

```
Speed Limit: 10 km/h

Vehicle Speed:
Car ID 22 → 20.19 km/h

Status:
Overspeed Violation
```

---

## 🚨 Violation Detection

Currently supported:

✅ Overspeed Detection

Future:

* Red light violation
* Wrong direction driving
* Helmet detection
* Number plate recognition

---

# 📈 Smart Dashboard

Built with Streamlit.

Dashboard provides:

## Live Statistics

* Total Vehicles
* Violations
* Entry Count
* Exit Count
* Vehicle Categories

## Traffic Analytics

* Vehicle distribution charts
* Speed analytics
* Density visualization
* Vehicle heatmap

## Database Management

* SQLite integration
* Session-based traffic records
* Searchable vehicle history

---

# 🏗 Project Architecture

```
Smart_Traffic_Monitoring/

│
├── app.py
├── requirements.txt
├── README.md
│
├── models/
│   └── yolo11n.pt
│
├── detection/
│   ├── tracker.py
│   ├── counter.py
│   ├── speed.py
│   ├── density.py
│   ├── violation.py
│   └── line_counter.py
│
├── database/
│   ├── database.py
│   └── traffic.db
│
├── dashboard/
│   ├── dashboard.py
│   ├── charts.py
│   ├── heatmap.py
│   ├── sidebar.py
│   └── admin_panel.py
│
├── config/
│   ├── config.py
│   └── classes.py
│
├── assets/
│   └── logo.png
│
└── screenshots/
    └── dashboard.png

```

---

# 🛠 Technologies Used

## Artificial Intelligence

* YOLO Object Detection
* ByteTrack Tracking
* Computer Vision

## Programming

* Python 3.12

## Libraries

* OpenCV
* Ultralytics YOLO
* NumPy
* Pandas
* Streamlit
* Plotly

## Database

* SQLite

---

# ⚙ Installation

Clone repository:

```bash
git clone https://github.com/yourusername/Smart_Traffic_Monitoring.git
```

Go inside project:

```bash
cd Smart_Traffic_Monitoring
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶ Run Application

## Start AI Detection

```bash
python app.py
```

## Start Dashboard

```bash
streamlit run dashboard/dashboard.py
```

---

## Dashboard



# 📊 Sample Output

```
Session ID: 28035


Total Vehicles : 55

Violations     : 30

Entry          : 27

Exit           : 0


Cars           : 49
Trucks         : 3
Bus            : 2

```

---

# 🚀 Future Improvements

Planned upgrades:

* 🔴 Traffic signal violation detection
* 🪪 Automatic Number Plate Recognition (ANPR)
* 🏍 Helmet detection
* 🚑 Automatic emergency vehicle priority
* ☁ Cloud deployment
* 📱 Mobile monitoring application
* 🌐 Live CCTV camera integration

---

# 👨‍💻 Author

**Sharif Ullah**

BS Artificial Intelligence

Computer Vision | Machine Learning | Deep Learning

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

## License

This project is developed for educational and research purposes.
