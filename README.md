# Complete Flutter HRM Employee Attendance Application

A comprehensive HRM application built with Flutter, Riverpod, and Clean Architecture.

## Features
- **Authentication**: Login and Forgot Password flows.
- **Session Management**: JWT/token persistence using `shared_preferences`.
- **Dashboard**: Real-time stats on attendance, check-in status, and working hours.
- **Attendance**: Check-in / Check-out capability utilizing the device's front camera.
- **Attendance Filtering**: View monthly attendance summaries and custom date-range filters.
- **Leave Management**: Apply for leaves (Casual, Sick, Earned) and view pending/approved statuses and balances.
- **Profile**: View logged-in employee details and securely log out.

## Architecture
The application uses a Feature-Based Clean Architecture approach:
```
UI -> StateNotifier/Provider -> Repository -> Data Source (Mock API / SharedPreferences)
```
- **State Management**: `flutter_riverpod`
- **Navigation**: `go_router` (including `StatefulShellRoute` for Bottom Navigation)
- **Local Persistence**: `shared_preferences`

## Face Recognition Limitation
**IMPORTANT:** The application uses Google ML Kit Face Detection (`google_mlkit_face_detection`) for determining if *exactly one face is present* in the camera frame. 

**Face Verification (Identity Check)**: Mock / Not connected to a real recognition engine. 
The system abstracts identity verification into `FaceVerificationService`, but currently injects a `MockFaceVerificationService` because no backend ML identity endpoint or on-device identity embedding model was provided.

## Mock Mode
The application heavily uses Mock Repositories (`MockAuthRepository`, `MockAttendanceRepository`, `MockLeaveRepository`) to simulate backend behavior, API latency, and data persistence via JSON encoding in `SharedPreferences`.

## Running the Application
Ensure you have the Flutter SDK installed on your machine.
```bash
flutter pub get
flutter analyze
flutter run
```

## Demo Credentials
To login, use the following credentials:
- **Email**: `tanisha@example.com`
- **Password**: `Password@123`

*(For the Forgot Password flow, the mock OTP is `123456`)*
