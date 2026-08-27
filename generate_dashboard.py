import os

files = {
    'lib/core/widgets/main_layout.dart': '''import \\'package:flutter/material.dart\\';
import \\'package:go_router/go_router.dart\\';

class MainLayout extends StatelessWidget {
  const MainLayout({super.key, required this.navigationShell});
  final StatefulNavigationShell navigationShell;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        selectedIndex: navigationShell.currentIndex,
        onDestinationSelected: (int index) {
          navigationShell.goBranch(
            index,
            initialLocation: index == navigationShell.currentIndex,
          );
        },
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard), label: \\'Home\\'),
          NavigationDestination(icon: Icon(Icons.access_time), label: \\'Attendance\\'),
          NavigationDestination(icon: Icon(Icons.event_note), label: \\'Leave\\'),
          NavigationDestination(icon: Icon(Icons.person), label: \\'Profile\\'),
        ],
      ),
    );
  }
}
''',
    'lib/features/dashboard/screens/dashboard_screen.dart': '''import \\'package:flutter/material.dart\\';
import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'package:go_router/go_router.dart\\';
import \\'../../profile/providers/profile_provider.dart\\';
import \\'../../attendance/providers/attendance_provider.dart\\';
import \\'package:intl/intl.dart\\';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final employeeAsync = ref.watch(employeeProvider);
    final todayAttendanceAsync = ref.watch(todayAttendanceProvider);

    return Scaffold(
      appBar: AppBar(title: const Text(\\'Dashboard\\')),
      body: RefreshIndicator(
        onRefresh: () async {
          ref.refresh(employeeProvider);
          await ref.read(todayAttendanceProvider.notifier).refresh();
        },
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            employeeAsync.when(
              data: (emp) => Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Row(
                    children: [
                      const CircleAvatar(radius: 30, child: Icon(Icons.person, size: 30)),
                      const SizedBox(width: 16),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(emp.name, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                          Text(emp.id, style: const TextStyle(color: Colors.grey)),
                        ],
                      )
                    ],
                  ),
                ),
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, st) => Text(\\'Error: \\\'),
            ),
            const SizedBox(height: 16),
            const Text(\\"Today's Attendance\\", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            todayAttendanceAsync.when(
              data: (attendance) {
                if (attendance == null || attendance.checkIn == null) {
                  return Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          const Text(\\'Not Checked In\\', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500)),
                          const SizedBox(height: 16),
                          ElevatedButton.icon(
                            icon: const Icon(Icons.camera_alt),
                            label: const Text(\\'Mark Check-In\\'),
                            onPressed: () async {
                              final result = await context.push(\\'/camera\\');
                              if (result == true) {
                                try {
                                  await ref.read(todayAttendanceProvider.notifier).checkIn();
                                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text(\\'Check-In Successful\\')));
                                } catch (e) {
                                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
                                }
                              }
                            },
                          )
                        ],
                      ),
                    ),
                  );
                }
                
                final dateFormat = DateFormat(\\'hh:mm a\\');
                return Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Text(\\'Status: \\\', style: const TextStyle(fontSize: 16)),
                        Text(\\'Check-In: \\\'),
                        if (attendance.checkOut != null)
                          Text(\\'Check-Out: \\\'),
                        Text(\\'Working Hours: \\\'),
                        const SizedBox(height: 16),
                        if (attendance.checkOut == null)
                          ElevatedButton.icon(
                            icon: const Icon(Icons.camera_alt),
                            label: const Text(\\'Mark Check-Out\\'),
                            style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                            onPressed: () async {
                              final result = await context.push(\\'/camera\\');
                              if (result == true) {
                                try {
                                  await ref.read(todayAttendanceProvider.notifier).checkOut();
                                  ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text(\\'Check-Out Successful\\')));
                                } catch (e) {
                                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
                                }
                              }
                            },
                          )
                        else
                          const Center(child: Text(\\'Attendance Completed\\', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, st) => Text(\\'Error: \\\'),
            )
          ],
        ),
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
