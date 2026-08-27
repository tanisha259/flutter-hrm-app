class Employee {
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
      name: 'Tanisha Pandit',
      department: 'Information Technology',
      designation: 'Software Developer',
      email: 'tanisha@example.com',
      mobile: '+91 98765 43210'
    );
  }
}
