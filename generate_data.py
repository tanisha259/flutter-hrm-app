import os

files = {
    'lib/core/utils/time_utils.dart': '''import \\'package:intl/intl.dart\\';
import \\'package:flutter/material.dart\\';

class TimeUtils {
  static String calculateWorkingHours(DateTime checkIn, DateTime? checkOut) {
    if (checkOut == null) return \\'--h --m\\';
    final duration = checkOut.difference(checkIn);
    final hours = duration.inHours;
    final minutes = duration.inMinutes % 60;
    return \\'h m\\';
  }

  static String determineStatus(DateTime checkIn, String officeStartTimeStr, String lateThresholdStr) {
    final now = DateTime.now();
    final officeStartParts = officeStartTimeStr.split(\\':\\');
    final lateParts = lateThresholdStr.split(\\':\\');
    
    final lateThreshold = DateTime(checkIn.year, checkIn.month, checkIn.day, int.parse(lateParts[0]), int.parse(lateParts[1]));
    
    if (checkIn.isAfter(lateThreshold)) {
      return \\'Late\\';
    }
    return \\'Present\\';
  }
}
''',
    'lib/features/authentication/data/auth_repository.dart': '''import \\'package:shared_preferences/shared_preferences.dart\\';
import \\'../../../core/constants/app_constants.dart\\';

class AuthSession {
  final String token;
  final String employeeId;
  AuthSession({required this.token, required this.employeeId});
}

abstract class AuthRepository {
  Future<AuthSession> login(String email, String password);
  Future<void> logout();
  Future<AuthSession?> getSession();
}

class MockAuthRepository implements AuthRepository {
  @override
  Future<AuthSession> login(String email, String password) async {
    await Future.delayed(const Duration(seconds: 1));
    if (email == \\'tanisha@example.com\\' && password == \\'Password@123\\') {
      final session = AuthSession(token: \\'mock_token_123\\', employeeId: \\'EMP001\\');
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.keyToken, session.token);
      await prefs.setString(AppConstants.keyUser, session.employeeId);
      return session;
    }
    throw Exception(\\'Invalid email or password\\');
  }

  @override
  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AppConstants.keyToken);
    await prefs.remove(AppConstants.keyUser);
  }

  @override
  Future<AuthSession?> getSession() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(AppConstants.keyToken);
    final empId = prefs.getString(AppConstants.keyUser);
    if (token != null && empId != null) {
      return AuthSession(token: token, employeeId: empId);
    }
    return null;
  }
}
''',
    'lib/features/profile/data/employee_repository.dart': '''class Employee {
  final String id;
  final String name;
  final String department;
  final String designation;
  final String email;
  final String mobile;

  Employee({required this.id, required this.name, required this.department, required this.designation, required this.email, required this.mobile});
}

class MockEmployeeRepository {
  Future<Employee> getEmployee(String id) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return Employee(
      id: id,
      name: \\'Tanisha Pandit\\',
      department: \\'Information Technology\\',
      designation: \\'Software Developer\\',
      email: \\'tanisha@example.com\\',
      mobile: \\'+91 98765 43210\\'
    );
  }
}
''',
    'lib/features/attendance/data/attendance_repository.dart': '''import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'../../../core/utils/time_utils.dart\\';
import \\'../../../core/constants/app_constants.dart\\';

class Attendance {
  final String id;
  final String employeeId;
  final DateTime date;
  final DateTime? checkIn;
  final DateTime? checkOut;
  final String status;

  Attendance({required this.id, required this.employeeId, required this.date, this.checkIn, this.checkOut, required this.status});
  
  String get workingHours => checkIn != null ? TimeUtils.calculateWorkingHours(checkIn!, checkOut) : \\'--h --m\\';
}

class MockAttendanceRepository {
  final List<Attendance> _mockRecords = [
    Attendance(id: \\'1\\', employeeId: \\'EMP001\\', date: DateTime.now().subtract(const Duration(days: 1)), checkIn: DateTime.now().subtract(const Duration(days: 1, hours: 8)), checkOut: DateTime.now().subtract(const Duration(days: 1, hours: -1)), status: \\'Present\\'),
    Attendance(id: \\'2\\', employeeId: \\'EMP001\\', date: DateTime.now().subtract(const Duration(days: 2)), checkIn: DateTime.now().subtract(const Duration(days: 2, hours: 8, minutes: 20)), checkOut: DateTime.now().subtract(const Duration(days: 2, hours: -1)), status: \\'Late\\'),
  ];
  
  Attendance? _todayAttendance;

  Future<List<Attendance>> getHistory(String employeeId, {DateTime? startDate, DateTime? endDate}) async {
    await Future.delayed(const Duration(milliseconds: 500));
    var results = _mockRecords.where((a) => a.employeeId == employeeId).toList();
    if (_todayAttendance != null) results.insert(0, _todayAttendance!);
    return results;
  }

  Future<Attendance?> getTodayAttendance(String employeeId) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return _todayAttendance;
  }

  Future<Attendance> checkIn(String employeeId) async {
    await Future.delayed(const Duration(milliseconds: 500));
    if (_todayAttendance != null && _todayAttendance!.checkIn != null) {
      throw Exception(\\'Already checked in today\\');
    }
    final now = DateTime.now();
    final status = TimeUtils.determineStatus(now, AppConstants.officeStartTime, AppConstants.lateAfterTime);
    _todayAttendance = Attendance(id: DateTime.now().millisecondsSinceEpoch.toString(), employeeId: employeeId, date: now, checkIn: now, status: status);
    return _todayAttendance!;
  }

  Future<Attendance> checkOut(String employeeId) async {
    await Future.delayed(const Duration(milliseconds: 500));
    if (_todayAttendance == null || _todayAttendance!.checkIn == null) {
      throw Exception(\\'Not checked in\\');
    }
    if (_todayAttendance!.checkOut != null) {
      throw Exception(\\'Already checked out\\');
    }
    _todayAttendance = Attendance(
      id: _todayAttendance!.id,
      employeeId: employeeId,
      date: _todayAttendance!.date,
      checkIn: _todayAttendance!.checkIn,
      checkOut: DateTime.now(),
      status: _todayAttendance!.status,
    );
    return _todayAttendance!;
  }
}
final attendanceRepoProvider = Provider((ref) => MockAttendanceRepository());
''',
    'lib/features/leave/data/leave_repository.dart': '''import \\'package:flutter_riverpod/flutter_riverpod.dart\\';

class LeaveRequest {
  final String id;
  final String employeeId;
  final String leaveType;
  final DateTime fromDate;
  final DateTime toDate;
  final String reason;
  final String status;
  
  int get numberOfDays => toDate.difference(fromDate).inDays + 1;

  LeaveRequest({required this.id, required this.employeeId, required this.leaveType, required this.fromDate, required this.toDate, required this.reason, required this.status});
}

class LeaveBalance {
  final String type;
  final int balance;
  LeaveBalance({required this.type, required this.balance});
}

class MockLeaveRepository {
  final List<LeaveRequest> _mockRequests = [
    LeaveRequest(id: \\'1\\', employeeId: \\'EMP001\\', leaveType: \\'Sick Leave\\', fromDate: DateTime.now().subtract(const Duration(days: 5)), toDate: DateTime.now().subtract(const Duration(days: 5)), reason: \\'Fever\\', status: \\'Approved\\'),
  ];
  
  final List<LeaveBalance> _balances = [
    LeaveBalance(type: \\'Casual Leave\\', balance: 8),
    LeaveBalance(type: \\'Sick Leave\\', balance: 5),
    LeaveBalance(type: \\'Earned Leave\\', balance: 10),
  ];

  Future<List<LeaveRequest>> getLeaveHistory(String employeeId) async {
    await Future.delayed(const Duration(milliseconds: 500));
    return _mockRequests;
  }

  Future<List<LeaveBalance>> getBalances(String employeeId) async {
    return _balances;
  }

  Future<void> applyLeave(LeaveRequest request) async {
    await Future.delayed(const Duration(milliseconds: 800));
    _mockRequests.insert(0, request);
  }
}
final leaveRepoProvider = Provider((ref) => MockLeaveRepository());
'''
}

for path, content in files.items():
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
