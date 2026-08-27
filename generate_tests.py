import os
import json

files = {
    'test/time_utils_test.dart': '''import \\'package:flutter_test/flutter_test.dart\\';
import \\'package:hrm_app/core/utils/time_utils.dart\\';

void main() {
  group(\\'TimeUtils\\', () {
    test(\\'calculateWorkingHours correctly calculates duration\\', () {
      final checkIn = DateTime(2026, 8, 27, 9, 0);
      final checkOut = DateTime(2026, 8, 27, 18, 0); // 9 hours
      
      final result = TimeUtils.calculateWorkingHours(checkIn, checkOut);
      expect(result, \\'09h 00m\\');
      
      final checkIn2 = DateTime(2026, 8, 27, 9, 15);
      final checkOut2 = DateTime(2026, 8, 27, 18, 15);
      expect(TimeUtils.calculateWorkingHours(checkIn2, checkOut2), \\'09h 00m\\');
    });
    
    test(\\'determineStatus calculates Late correctly\\', () {
      final checkInOnTime = DateTime(2026, 8, 27, 9, 10);
      expect(TimeUtils.determineStatus(checkInOnTime, \\'09:00\\', \\'09:15\\'), \\'Present\\');
      
      final checkInLate = DateTime(2026, 8, 27, 9, 20);
      expect(TimeUtils.determineStatus(checkInLate, \\'09:00\\', \\'09:15\\'), \\'Late\\');
    });
  });
}
''',
    'test/attendance_test.dart': '''import \\'package:flutter_test/flutter_test.dart\\';
import \\'package:hrm_app/features/attendance/data/attendance_repository.dart\\';
import \\'package:shared_preferences/shared_preferences.dart\\';

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test(\\'Check-in sets status properly\\', () async {
    final repo = MockAttendanceRepository();
    await repo.init();
    final att = await repo.checkIn(\\'EMP001\\');
    expect(att.checkIn, isNotNull);
    expect(att.checkOut, isNull);
  });
  
  test(\\'Check-out before check-in throws\\', () async {
    final repo = MockAttendanceRepository();
    await repo.init();
    expect(() => repo.checkOut(\\'EMP001\\'), throwsException);
  });
}
''',
    'test/auth_test.dart': '''import \\'package:flutter_test/flutter_test.dart\\';
import \\'package:hrm_app/features/authentication/data/auth_repository.dart\\';
import \\'package:shared_preferences/shared_preferences.dart\\';

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test(\\'Valid login returns session\\', () async {
    final repo = MockAuthRepository();
    final session = await repo.login(\\'tanisha@example.com\\', \\'Password@123\\');
    expect(session.token, \\'mock_token_123\\');
    expect(session.employeeId, \\'EMP001\\');
  });

  test(\\'Invalid login throws\\', () async {
    final repo = MockAuthRepository();
    expect(() => repo.login(\\'wrong@email.com\\', \\'badpass\\'), throwsException);
  });
}
'''
}

for path, content in files.items():
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
