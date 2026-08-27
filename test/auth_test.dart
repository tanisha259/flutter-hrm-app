import 'package:flutter_test/flutter_test.dart';
import 'package:hrm_app/features/authentication/data/auth_repository.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  test('Valid login returns session', () async {
    final repo = MockAuthRepository();
    final session = await repo.login('tanisha@example.com', 'Password@123');
    expect(session.token, 'mock_token_123');
    expect(session.employeeId, 'EMP001');
  });

  test('Invalid login throws', () async {
    final repo = MockAuthRepository();
    expect(() => repo.login('wrong@email.com', 'badpass'), throwsException);
  });
}
