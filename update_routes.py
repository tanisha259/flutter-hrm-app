import os

app_router_path = 'lib/core/routes/app_router.dart'
app_router_content = '''import \\'package:go_router/go_router.dart\\';
import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'../../features/authentication/screens/login_screen.dart\\';
import \\'../../features/dashboard/screens/dashboard_screen.dart\\';
import \\'../../features/attendance/screens/camera_screen.dart\\';

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: \\'/login\\',
    routes: [
      GoRoute(
        path: \\'/login\\',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: \\'/dashboard\\',
        builder: (context, state) => const DashboardScreen(),
      ),
      GoRoute(
        path: \\'/camera\\',
        builder: (context, state) => const CameraScreen(),
      ),
    ],
  );
});
'''

dashboard_path = 'lib/features/dashboard/screens/dashboard_screen.dart'
dashboard_content = '''import \\'package:flutter/material.dart\\';
import \\'package:go_router/go_router.dart\\';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(\\'Dashboard\\'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => context.go(\\'/login\\'),
          )
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircleAvatar(
              radius: 50,
              child: Icon(Icons.person, size: 50),
            ),
            const SizedBox(height: 16),
            const Text(\\'Tanisha Pandit\\', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const Text(\\'EMP001\\', style: TextStyle(fontSize: 16, color: Colors.grey)),
            const SizedBox(height: 40),
            ElevatedButton.icon(
              icon: const Icon(Icons.camera_alt),
              label: const Text(\\'Mark Check-In\\'),
              onPressed: () async {
                final result = await context.push(\\'/camera\\');
                if (result == true && context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text(\\'Check-In Successful\\', style: TextStyle(color: Colors.white)), backgroundColor: Colors.green),
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}
'''

with open(app_router_path, 'w', encoding='utf-8') as f:
    f.write(app_router_content)

with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(dashboard_content)

