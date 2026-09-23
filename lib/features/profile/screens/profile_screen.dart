import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/profile_provider.dart';
import '../../authentication/providers/auth_provider.dart';

/// A screen displaying the logged-in employee's profile details and account actions.
class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final employeeAsync = ref.watch(employeeProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Profile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              ref.read(authStateProvider.notifier).logout();
            },
          )
        ],
      ),
      body: employeeAsync.when(
        data: (emp) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            const CircleAvatar(radius: 50, child: Icon(Icons.person, size: 50)),
            const SizedBox(height: 16),
            Text(emp.name, textAlign: TextAlign.center, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text(emp.id, textAlign: TextAlign.center, style: const TextStyle(color: Colors.grey)),
            const Divider(height: 40),
            ListTile(title: const Text('Department'), subtitle: Text(emp.department)),
            ListTile(title: const Text('Designation'), subtitle: Text(emp.designation)),
            ListTile(title: const Text('Email'), subtitle: Text(emp.email)),
            ListTile(title: const Text('Mobile'), subtitle: Text(emp.mobile)),
          ],
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, st) => Center(child: Text('Error: ')),
      ),
    );
  }
}
