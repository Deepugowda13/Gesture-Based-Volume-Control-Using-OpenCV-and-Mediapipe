# 🖐️ Gesture-Based Volume Control Using OpenCV and Mediapipe

This project implements a real-time gesture-based system volume controller using Python. It allows users to control their system’s audio volume by adjusting the distance between their thumb and index finger in front of a webcam.

---

## 📌 Features

- 🎯 Real-time hand gesture detection using webcam
- 🔊 Volume control based on finger distance
- 📊 Visual feedback: On-screen volume bar and percentage
- 🎨 Volume bar color customization (default: blue)
- ⚠️ Popup warning at 100% volume
- 🧠 Smooth, intuitive user interaction using Computer Vision

---

## 🧰 Technologies Used

- **Python**
- **OpenCV** – Real-time image processing
- **Mediapipe** – Hand landmark detection
- **pycaw** – Audio control interface (Windows)
- **math, numpy** – For distance calculation and interpolation

---

## 🖥️ Demo

### 🔊 Volume Increase Example
![Volume Increase](images/volume%20increaser.png)

### 🔉 Volume Decrease Example
![Volume Decrease](images/volume%20decrease.png)

---

## 🛠️ Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gesture-volume-control.git
   cd gesture-volume-control
