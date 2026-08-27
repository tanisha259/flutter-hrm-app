import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/attendance_repository.dart';

final todayAttendanceProvider = StateNotifierProvider<TodayAttendanceNotifier, AsyncValue<Attendance?>>((ref) {
  return TodayAttendanceNotifier(ref.watch(attendanceRepoProvider), 'EMP001');
});

class TodayAttendanceNotifier extends StateNotifier<AsyncValue<Attendance?>> {
  final MockAttendanceRepository _repo;
  final String _employeeId;
  
  TodayAttendanceNotifier(this._repo, this._employeeId) : super(const AsyncValue.loading()) {
    refresh();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    try {
      final data = await _repo.getTodayAttendance(_employeeId);
      state = AsyncValue.data(data);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> checkIn() async {
    try {
      final data = await _repo.checkIn(_employeeId);
      state = AsyncValue.data(data);
    } catch (e) {
      rethrow;
    }
  }

  Future<void> checkOut() async {
    try {
      final data = await _repo.checkOut(_employeeId);
      state = AsyncValue.data(data);
    } catch (e) {
      rethrow;
    }
  }
}

final attendanceHistoryProvider = FutureProvider.autoDispose<List<Attendance>>((ref) {
  final repo = ref.watch(attendanceRepoProvider);
  return repo.getHistory('EMP001');
});
