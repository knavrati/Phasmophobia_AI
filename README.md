# Phasmophobia_AI
AI integration into Phasmophobia for assist in identifying ghosts.

Overview
Phasmophobia Ghost Detection AI is a Python-based application designed to assist players in the horror game Phasmophobia by automatically detecting and identifying ghost types in real-time. Leveraging computer vision, audio processing, and Google's Generative AI (Gemini) API, this tool analyzes live game screenshots to determine the type of ghost present based on in-game evidence.

Features
Real-time Screen Capture: Continuously captures live game screenshots using the mss library.
Image Processing: Utilizes OpenCV (cv2) and NumPy for processing images to detect in-game evidence.
Audio Notifications: Integrates text-to-speech (pyttsx3) to provide audible alerts about detected evidence.
Google Generative AI Integration: Sends processed images to the Gemini API for advanced analysis and content generation.
Evidence Matching: Matches detected evidence against a predefined ghost database to accurately identify the ghost type.
Automated Alerts: Notifies users through in-game overlays and external platforms (e.g., Discord) when specific evidence is found.
Secure Authentication: Manages secure API interactions and credentials using Google Auth libraries.
Containerization: Facilitates easy deployment and scalability using Docker.
Technologies Used
Programming Language: Python
Libraries & Frameworks: mss, cv2 (OpenCV), numpy, pyttsx3, google.generativeai
APIs: Google Gemini API
Authentication: google-auth, google-auth-oauthlib
Other Tools: Docker, Requests, JSON
Installation
Prerequisites
Python 3.7+ installed on your system.
Google Cloud Account with access to the Gemini API.
Client Secret JSON file for Google OAuth authentication.
Docker installed (optional, for containerization).
