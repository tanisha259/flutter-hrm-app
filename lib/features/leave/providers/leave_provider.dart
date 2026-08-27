import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/leave_repository.dart';

final leaveBalancesProvider = FutureProvider<List<LeaveBalance>>((ref) {
  final repo = ref.watch(leaveRepoProvider);
  return repo.getBalances('EMP001');
});

final leaveHistoryProvider = FutureProvider.autoDispose<List<LeaveRequest>>((ref) {
  final repo = ref.watch(leaveRepoProvider);
  return repo.getLeaveHistory('EMP001');
});
