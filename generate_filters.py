import os

files = {
    'lib/features/attendance/screens/attendance_history_screen.dart': '''import \\'package:flutter/material.dart\\';
import \\'package:flutter_riverpod/flutter_riverpod.dart\\';
import \\'package:intl/intl.dart\\';
import \\'../providers/attendance_provider.dart\\';
import \\'../data/attendance_repository.dart\\';

class AttendanceHistoryScreen extends ConsumerStatefulWidget {
  const AttendanceHistoryScreen({super.key});

  @override
  ConsumerState<AttendanceHistoryScreen> createState() => _AttendanceHistoryScreenState();
}

class _AttendanceHistoryScreenState extends ConsumerState<AttendanceHistoryScreen> {
  DateTime? _filterMonth;
  DateTime? _fromDate;
  DateTime? _toDate;

  List<Attendance> _applyFilters(List<Attendance> records) {
    var filtered = records;
    if (_filterMonth != null) {
      filtered = filtered.where((r) => r.date.year == _filterMonth!.year && r.date.month == _filterMonth!.month).toList();
    }
    if (_fromDate != null && _toDate != null) {
      filtered = filtered.where((r) => r.date.isAfter(_fromDate!.subtract(const Duration(days: 1))) && r.date.isBefore(_toDate!.add(const Duration(days: 1)))).toList();
    }
    return filtered;
  }

  @override
  Widget build(BuildContext context) {
    final historyAsync = ref.watch(attendanceHistoryProvider);
    final dateFormat = DateFormat(\\'dd MMM yyyy\\');
    final timeFormat = DateFormat(\\'hh:mm a\\');

    return Scaffold(
      appBar: AppBar(title: const Text(\\'Attendance History\\')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: () async {
                      final picked = await showDatePicker(context: context, initialDate: DateTime.now(), firstDate: DateTime(2020), lastDate: DateTime(2100));
                      if (picked != null) setState(() { _filterMonth = picked; _fromDate = null; _toDate = null; });
                    },
                    child: Text(_filterMonth == null ? \\'Select Month\\' : DateFormat(\\'MMM yyyy\\').format(_filterMonth!)),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ElevatedButton(
                    onPressed: () async {
                      final picked = await showDateRangePicker(context: context, firstDate: DateTime(2020), lastDate: DateTime(2100));
                      if (picked != null) setState(() { _fromDate = picked.start; _toDate = picked.end; _filterMonth = null; });
                    },
                    child: const Text(\\'Date Range\\'),
                  ),
                ),
                IconButton(icon: const Icon(Icons.clear), onPressed: () => setState(() { _filterMonth = null; _fromDate = null; _toDate = null; }))
              ],
            ),
          ),
          Expanded(
            child: historyAsync.when(
              data: (records) {
                final filtered = _applyFilters(records);
                if (filtered.isEmpty) return const Center(child: Text(\\'No attendance records match.\\'));
                
                int present = filtered.where((e) => e.status == \\'Present\\').length;
                int lateCount = filtered.where((e) => e.status == \\'Late\\').length;
                
                return Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(\\'Present: \ | Late: \\\', style: const TextStyle(fontWeight: FontWeight.bold)),
                    ),
                    Expanded(
                      child: ListView.builder(
                        itemCount: filtered.length,
                        itemBuilder: (context, index) {
                          final record = filtered[index];
                          return Card(
                            child: ListTile(
                              title: Text(dateFormat.format(record.date)),
                              subtitle: Text(\\'Check-In: \\\nCheck-Out: \\\nHours: \\\'),
                              trailing: Chip(label: Text(record.status), backgroundColor: record.status == \\'Late\\' ? Colors.orange.shade100 : Colors.green.shade100),
                            ),
                          );
                        },
                      ),
                    ),
                  ],
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
