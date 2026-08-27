import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:intl/intl.dart';
import '../providers/leave_provider.dart';

class LeaveHistoryScreen extends ConsumerWidget {
  const LeaveHistoryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final historyAsync = ref.watch(leaveHistoryProvider);
    final balancesAsync = ref.watch(leaveBalancesProvider);
    final dateFormat = DateFormat('dd MMM yyyy');

    return Scaffold(
      appBar: AppBar(title: const Text('Leave')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => context.push('/apply_leave'),
        icon: const Icon(Icons.add),
        label: const Text('Apply Leave'),
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
                  return const Center(child: Text('No leave requests found.'));
                }
                return ListView.builder(
                  itemCount: records.length,
                  itemBuilder: (context, index) {
                    final req = records[index];
                    return Card(
                      child: ListTile(
                        title: Text(req.leaveType),
                        subtitle: Text('${dateFormat.format(req.fromDate)} - ${dateFormat.format(req.toDate)}\n${req.numberOfDays} Days'),
                        trailing: Chip(label: Text(req.status)),
                      ),
                    );
                  },
                );
              },
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (err, st) => Center(child: Text('Error: $err')),
            ),
          )
        ],
      ),
    );
  }
}
