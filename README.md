# 🏢 Flutter HRM & Employee Attendance System

![Flutter](https://img.shields.io/badge/Flutter-3.x-blue.svg?logo=flutter)
![Dart](https://img.shields.io/badge/Dart-3.x-blue.svg?logo=dart)
![Architecture](https://img.shields.io/badge/Architecture-Clean-brightgreen.svg)
![State Management](https://img.shields.io/badge/State-Riverpod-orange.svg)

A production-grade Human Resource Management (HRM) application built with **Flutter**. This application features a robust Clean Architecture design, reactive state management using Riverpod, and a smart Face Detection-based attendance system using Google ML Kit.

---

## ✨ Key Features

* **🔐 Authentication & Security:** Secure login and forgotten password recovery flow. Session persistence is handled locally via `SharedPreferences`.
* **📊 Smart Dashboard:** Real-time overview of today's attendance status, check-in/check-out times, total working hours, and available leave balances.
* **📸 Face Detection Attendance:** Enforces exactly *one* face in the camera frame before permitting an employee to mark their check-in or check-out, powered by `google_mlkit_face_detection`.
* **📅 Attendance History & Filters:** View past attendance records with dynamic filters for specific Date Ranges or Months. Automatically calculates total present and late days.
* **🏖️ Leave Management:** Apply for various types of leaves (Casual, Sick, Earned), track approval statuses, and view complete leave history.
* **👤 Employee Profile:** Display of logged-in employee details and secure logout functionality.

---

## 🏗️ Architecture & Tech Stack

This project strictly adheres to **Feature-Based Clean Architecture** to ensure maintainability, scalability, and separation of concerns.

* **Framework:** Flutter (Material 3)
* **State Management:** Riverpod (`flutter_riverpod`)
* **Routing:** GoRouter (including `StatefulShellRoute` for Bottom Navigation)
* **Local Persistence:** SharedPreferences (Mock database encoded in JSON)
* **Machine Learning:** Google ML Kit Face Detection
* **Hardware Access:** Camera plugin

### 📂 Directory Structure Overview
```text
lib/
 ┣ core/              # Shared utilities, routing, themes, and UI components
 ┣ features/          # Feature modules
 ┃ ┣ attendance/      # Face detection, check-in/out logic, history UI
 ┃ ┣ authentication/  # Login, Forgot Password, Auth state
 ┃ ┣ dashboard/       # Main overview screen
 ┃ ┣ leave/           # Leave application and history tracking
 ┃ ┗ profile/         # Employee profile and settings
 ┗ main.dart          # App entry point & ProviderScope
```

---

## 🚀 Installation & Setup Guidelines

Follow these steps to run the application locally on your machine.

### Prerequisites
* [Flutter SDK](https://docs.flutter.dev/get-started/install) installed.
* [Android Studio](https://developer.android.com/studio) installed (for the Android SDK and Emulator).
* **Important:** To test the Face Detection functionality on an Android Emulator, ensure your emulator's **Front Camera** is mapped to your computer's Webcam in the AVD Advanced Settings.

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/tanisha259/flutter-hrm-app.git
   cd "flutter-hrm-app"
   ```

2. **Install Dependencies**
   ```bash
   flutter pub get
   ```

3. **Run Code Analysis (Optional but recommended)**
   Ensure the codebase is clean before running:
   ```bash
   flutter analyze
   ```

4. **Run Unit Tests**
   Validate the core business logic (working hours, late calculations, auth):
   ```bash
   flutter test
   ```

5. **Launch the Application**
   Start your emulator or connect a physical device, then run:
   ```bash
   flutter run
   ```

---

## 🔑 Demo Credentials

To access the application, use the following mock credentials. 

| Field | Credential |
| :--- | :--- |
| **Email** | `tanisha@example.com` |
| **Password** | `Password@123` |

*(Note: For the Forgot Password flow, the mock OTP to proceed is `123456`)*

---

## ⚠️ Important Notes & Limitations

* **Face Detection vs. Verification:** The app successfully uses Google ML Kit to **detect** faces (ensuring a human face is present and that there are no multiple faces in the frame). However, actual identity **verification** (comparing the face to a registered employee database) is mocked via a `MockFaceVerificationService`. A real backend API endpoint or on-device embedding model would be required for true biometric identity verification in a production environment.
* **Mock Data Layer:** The application uses Repository pattern implementations (e.g., `MockAuthRepository`, `MockAttendanceRepository`) that simulate backend latency and save data locally to `SharedPreferences`. This ensures the app is fully testable and stateful without requiring an active external database.

---
*Built with ❤️ using Flutter.*
