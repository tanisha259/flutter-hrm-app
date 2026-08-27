import 'package:flutter/material.dart';

class AppColors {
  static const Color primary = Color(0xFF3F51B5); // Indigo
  static const Color primaryDark = Color(0xFF303F9F);
  static const Color primaryLight = Color(0xFFC5CAE9);
  
  static const Color accent = Color(0xFF00BCD4);
  
  static const Color background = Color(0xFFF5F5F6);
  static const Color surface = Colors.white;
  
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF757575);
  
  static const Color success = Color(0xFF4CAF50);
  static const Color error = Color(0xFFF44336);
  static const Color warning = Color(0xFFFFC107);
  static const Color info = Color(0xFF2196F3);
}

class AppConstants {
  static const String appName = 'HRM App';
  
  // Attendance rules
  static const String officeStartTime = '09:00:00';
  static const String lateAfterTime = '09:15:00';
  
  // Shared Preferences Keys
  static const String keyToken = 'auth_token';
  static const String keyUser = 'auth_user';
}
