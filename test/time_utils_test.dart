import 'package:flutter_test/flutter_test.dart';
import 'package:hrm_app/core/utils/time_utils.dart';

void main() {
  group('TimeUtils', () {
    test('calculateWorkingHours correctly calculates duration', () {
      final checkIn = DateTime(2026, 8, 27, 9, 0);
      final checkOut = DateTime(2026, 8, 27, 18, 0); // 9 hours
      
      final result = TimeUtils.calculateWorkingHours(checkIn, checkOut);
      expect(result, '09h 00m');
      
      final checkIn2 = DateTime(2026, 8, 27, 9, 15);
      final checkOut2 = DateTime(2026, 8, 27, 18, 15);
      expect(TimeUtils.calculateWorkingHours(checkIn2, checkOut2), '09h 00m');
    });
    
    test('determineStatus calculates Late correctly', () {
      final checkInOnTime = DateTime(2026, 8, 27, 9, 10);
      expect(TimeUtils.determineStatus(checkInOnTime, '09:00', '09:15'), 'Present');
      
      final checkInLate = DateTime(2026, 8, 27, 9, 20);
      expect(TimeUtils.determineStatus(checkInLate, '09:00', '09:15'), 'Late');
    });
  });
}
