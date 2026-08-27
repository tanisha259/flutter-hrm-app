import 'package:flutter_test/flutter_test.dart';
import 'package:hrm_app/features/attendance/data/attendance_repository.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test('Check-in sets status properly', () async {
    final repo = MockAttendanceRepository();
    await repo.init();
    final att = await repo.checkIn('EMP001');
    expect(att.checkIn, isNotNull);
    expect(att.checkOut, isNull);
  });
  
  test('Check-out before check-in throws', () async {
    final repo = MockAttendanceRepository();
    await repo.init();
    expect(() => repo.checkOut('EMP001'), throwsException);
  });
}
