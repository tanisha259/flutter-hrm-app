import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/employee_repository.dart';

final employeeRepoProvider = Provider((ref) => MockEmployeeRepository());

final employeeProvider = FutureProvider<Employee>((ref) {
  final repo = ref.watch(employeeRepoProvider);
  return repo.getEmployee('EMP001');
});
