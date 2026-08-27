import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/auth_repository.dart';

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
