import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/constants/app_constants.dart';

class AuthSession {
  final String token;
  final String employeeId;
  AuthSession({required this.token, required this.employeeId});
}

abstract class AuthRepository {
  Future<AuthSession> login(String email, String password);
  Future<void> logout();
  Future<AuthSession?> getSession();
}

class MockAuthRepository implements AuthRepository {
  @override
  Future<AuthSession> login(String email, String password) async {
    await Future.delayed(const Duration(seconds: 1));
    if (email == 'tanisha@example.com' && password == 'Password@123') {
      final session = AuthSession(token: 'mock_token_123', employeeId: 'EMP001');
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString(AppConstants.keyToken, session.token);
      await prefs.setString(AppConstants.keyUser, session.employeeId);
      return session;
    }
    throw Exception('Invalid email or password');
  }

  @override
  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(AppConstants.keyToken);
    await prefs.remove(AppConstants.keyUser);
  }

  @override
  Future<AuthSession?> getSession() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString(AppConstants.keyToken);
    final empId = prefs.getString(AppConstants.keyUser);
    if (token != null && empId != null) {
      return AuthSession(token: token, employeeId: empId);
    }
    return null;
  }
}
