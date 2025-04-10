# Lokari IoT
## UNI051 - MasiBelajar IoT 

This repository contains IoT code for Lokari project.

### ESP32 BASE
MicroPython code that reads temperature and humidity from a DHT11 sensor, checks for changes in readings, and sends the data to Ubidots IoT platform over Wi-Fi. It also controls an LED connected to a PIR sensor.
#### Core Functionality
- Wi-Fi connectivity
- Sensor reading with debounce logic
- Data push to Ubidots
- LED hardware interface

### ESP32 CAM
Arduino (C++) code is for an ESP32-CAM board using the ESP32 Camera Web Server. This is a common setup for streaming camera footage over Wi-Fi using a web browser.
#### Core Functionality
- Initializes and configures a camera module (e.g., AI Thinker ESP32-CAM).
- Connects to Wi-Fi.
- Starts a web server to stream live video from the camera.
