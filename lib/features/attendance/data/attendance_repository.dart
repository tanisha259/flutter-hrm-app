import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/utils/time_utils.dart';
import '../../../core/constants/app_constants.dart';

class Attendance {
  final String id;
  final String employeeId;
  final DateTime date;
  final DateTime? checkIn;
  final DateTime? checkOut;
  final String status;

  Attendance({required this.id, required this.employeeId, required this.date, this.checkIn, this.checkOut, required this.status});
  
  String get workingHours => checkIn != null ? TimeUtils.calculateWorkingHours(checkIn!, checkOut) : '--h --m';

  Map<String, dynamic> toJson() => {
    'id': id, 'employeeId': employeeId, 'date': date.toIso8601String(),
    'checkIn': checkIn?.toIso8601String(), 'checkOut': checkOut?.toIso8601String(), 'status': status
  };

  factory Attendance.fromJson(Map<String, dynamic> json) => Attendance(
    id: json['id'], employeeId: json['employeeId'], date: DateTime.parse(json['date']),
    checkIn: json['checkIn'] != null ? DateTime.parse(json['checkIn']) : null,
    checkOut: json['checkOut'] != null ? DateTime.parse(json['checkOut']) : null,
    status: json['status']
  );
}

class MockAttendanceRepository {
  List<Attendance> _records = [];
  bool _isInit = false;

  Future<void> init() async {
    if (_isInit) return;
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getStringList('attendance_records');
    if (data != null) {
      _records = data.map((e) => Attendance.fromJson(jsonDecode(e))).toList();
    }
    _isInit = true;
  }

  Future<void> _save() async {
    final prefs = await SharedPreferences.getInstance();
    final data = _records.map((e) => jsonEncode(e.toJson())).toList();
    await prefs.setStringList('attendance_records', data);
  }

  Future<List<Attendance>> getHistory(String employeeId) async {
    await init();
    return _records.where((a) => a.employeeId == employeeId).toList();
  }

  Future<Attendance?> getTodayAttendance(String employeeId) async {
    await init();
    final now = DateTime.now();
    try {
      return _records.firstWhere((a) => a.employeeId == employeeId && a.date.year == now.year && a.date.month == now.month && a.date.day == now.day);
    } catch (e) {
      return null;
    }
  }

  Future<Attendance> checkIn(String employeeId) async {
    await init();
    final existing = await getTodayAttendance(employeeId);
    if (existing != null && existing.checkIn != null) {
      throw Exception('Already checked in today');
    }
    final now = DateTime.now();
    final status = TimeUtils.determineStatus(now, AppConstants.officeStartTime, AppConstants.lateAfterTime);
    final att = Attendance(id: now.millisecondsSinceEpoch.toString(), employeeId: employeeId, date: now, checkIn: now, status: status);
    _records.insert(0, att);
    await _save();
    return att;
  }

  Future<Attendance> checkOut(String employeeId) async {
    await init();
    final existing = await getTodayAttendance(employeeId);
    if (existing == null || existing.checkIn == null) {
      throw Exception('Not checked in');
    }
    if (existing.checkOut != null) {
      throw Exception('Already checked out');
    }
    final idx = _records.indexWhere((a) => a.id == existing.id);
    final updated = Attendance(
      id: existing.id, employeeId: employeeId, date: existing.date,
      checkIn: existing.checkIn, checkOut: DateTime.now(), status: existing.status,
    );
    _records[idx] = updated;
    await _save();
    return updated;
  }
}
final attendanceRepoProvider = Provider((ref) => MockAttendanceRepository());
