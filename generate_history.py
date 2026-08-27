import os

files = {
    'lib/features/attendance/screens/attendance_history_screen.dart': '''import \\'package:flutter/material.dart\\';
import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'package:intl/intl.dart\\';
import \\'../providers/attendance_provider.dart\\';

class AttendanceHistoryScreen extends ConsumerWidget {
  const AttendanceHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final historyAsync = ref.watch(attendanceHistoryProvider);
    final dateFormat = DateFormat(\\'dd MMM yyyy\\');
    final timeFormat = DateFormat(\\'hh:mm a\\');

    return Scaffold(
      appBar: AppBar(title: const Text(\\'Attendance History\\')),
      body: historyAsync.when(
        data: (records) {
          if (records.isEmpty) {
            return const Center(child: Text(\\'No attendance records found.\\'));
          }
          return ListView.builder(
            itemCount: records.length,
            itemBuilder: (context, index) {
              final record = records[index];
              return Card(
                child: ListTile(
                  title: Text(dateFormat.format(record.date)),
                  subtitle: Text(\\'Check-In: \\\nCheck-Out: \\\nHours: \\\'),
                  trailing: Chip(label: Text(record.status), backgroundColor: record.status == \\'Late\\' ? Colors.orange.shade100 : Colors.green.shade100),
                ),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, st) => Center(child: Text(\\'Error: \\\')),
      ),
    );
  }
}
''',
    'lib/features/profile/screens/profile_screen.dart': '''import \\'package:flutter/material.dart\\';
import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'../providers/profile_provider.dart\\';
import \\'../../authentication/providers/auth_provider.dart\\';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final employeeAsync = ref.watch(employeeProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text(\\'My Profile\\'),
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
            ListTile(title: const Text(\\'Department\\'), subtitle: Text(emp.department)),
            ListTile(title: const Text(\\'Designation\\'), subtitle: Text(emp.designation)),
            ListTile(title: const Text(\\'Email\\'), subtitle: Text(emp.email)),
            ListTile(title: const Text(\\'Mobile\\'), subtitle: Text(emp.mobile)),
          ],
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, st) => Center(child: Text(\\'Error: \\\')),
      ),
    );
  }
}
''',
    'lib/features/leave/screens/leave_history_screen.dart': '''import \\'package:flutter/material.dart\\';
import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'package:go_router/go_router.dart\\';
import \\'package:intl/intl.dart\\';
import \\'../providers/leave_provider.dart\\';

class LeaveHistoryScreen extends ConsumerWidget {
  const LeaveHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final historyAsync = ref.watch(leaveHistoryProvider);
    final balancesAsync = ref.watch(leaveBalancesProvider);
    final dateFormat = DateFormat(\\'dd MMM yyyy\\');

    return Scaffold(
      appBar: AppBar(title: const Text(\\'Leave\\')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push(\\'/apply_leave\\'),
        icon: const Icon(Icons.add),
        label: const Text(\\'Apply Leave\\'),
      ),
      body: Column(
        children: [
          balancesAsync.when(
            data: (balances) => Container(
              height: 100,
              padding: const EdgeInsets.all(8),
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: balances.length,
                itemBuilder: (context, index) {
                  final b = balances[index];
                  return Card(
                    child: Container(
                      width: 120,
                      padding: const EdgeInsets.all(8),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(b.type, textAlign: TextAlign.center, style: const TextStyle(fontSize: 12)),
                          Text(b.balance.toString(), style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            loading: () => const SizedBox(height: 100, child: Center(child: CircularProgressIndicator())),
            error: (err, st) => const SizedBox(height: 100),
          ),
          const Divider(),
          Expanded(
            child: historyAsync.when(
              data: (records) {
                if (records.isEmpty) {
                  return const Center(child: Text(\\'No leave requests found.\\'));
                }
                return ListView.builder(
                  itemCount: records.length,
                  itemBuilder: (context, index) {
                    final req = records[index];
                    return Card(
                      child: ListTile(
                        title: Text(req.leaveType),
                        subtitle: Text(\\'\ - \\\n\ Days\\'),
                        trailing: Chip(label: Text(req.status)),
                      ),
                    );
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, st) => Center(child: Text(\\'Error: \\\')),
            ),
          )
        ],
      ),
    );
  }
}
'''
}

for path, content in files.items():
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
