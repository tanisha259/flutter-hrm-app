import os

files = {
    'lib/features/authentication/providers/auth_provider.dart': '''import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'../data/auth_repository.dart\\';

final authRepoProvider = Provider<AuthRepository>((ref) => MockAuthRepository());

final authStateProvider = StateNotifierProvider<AuthNotifier, AsyncValue<AuthSession?>>((ref) {
  return AuthNotifier(ref.watch(authRepoProvider));
});

class AuthNotifier extends StateNotifier<AsyncValue<AuthSession?>> {
  final AuthRepository _repo;
  AuthNotifier(this._repo) : super(const AsyncValue.loading()) {
    _init();
  }

  Future<void> _init() async {
    try {
      final session = await _repo.getSession();
      state = AsyncValue.data(session);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> login(String email, String password) async {
    state = const AsyncValue.loading();
    try {
      final session = await _repo.login(email, password);
      state = AsyncValue.data(session);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> logout() async {
    await _repo.logout();
    state = const AsyncValue.data(null);
  }
}
''',
    'lib/features/attendance/providers/attendance_provider.dart': '''import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'../data/attendance_repository.dart\\';

final todayAttendanceProvider = StateNotifierProvider<TodayAttendanceNotifier, AsyncValue<Attendance?>>((ref) {
  return TodayAttendanceNotifier(ref.watch(attendanceRepoProvider), \\'EMP001\\');
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
  return repo.getHistory(\\'EMP001\\');
});
''',
    'lib/features/leave/providers/leave_provider.dart': '''import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'../data/leave_repository.dart\\';

final leaveBalancesProvider = FutureProvider<List<LeaveBalance>>((ref) {
  final repo = ref.watch(leaveRepoProvider);
  return repo.getBalances(\\'EMP001\\');
});

final leaveHistoryProvider = FutureProvider.autoDispose<List<LeaveRequest>>((ref) {
  final repo = ref.watch(leaveRepoProvider);
  return repo.getLeaveHistory(\\'EMP001\\');
});
''',
    'lib/features/profile/providers/profile_provider.dart': '''import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'../data/employee_repository.dart\\';

final employeeRepoProvider = Provider((ref) => MockEmployeeRepository());

final employeeProvider = FutureProvider<Employee>((ref) {
  final repo = ref.watch(employeeRepoProvider);
  return repo.getEmployee(\\'EMP001\\');
});
'''
}

for path, content in files.items():
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
