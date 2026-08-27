import 'package:flutter_riverpod/flutter_riverpod.dart';

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
    LeaveRequest(id: '1', employeeId: 'EMP001', leaveType: 'Sick Leave', fromDate: DateTime.now().subtract(const Duration(days: 5)), toDate: DateTime.now().subtract(const Duration(days: 5)), reason: 'Fever', status: 'Approved'),
  ];
  
  final List<LeaveBalance> _balances = [
    LeaveBalance(type: 'Casual Leave', balance: 8),
    LeaveBalance(type: 'Sick Leave', balance: 5),
    LeaveBalance(type: 'Earned Leave', balance: 10),
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
