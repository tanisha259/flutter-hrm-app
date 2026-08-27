class TimeUtils {
  static String calculateWorkingHours(DateTime checkIn, DateTime? checkOut) {
    if (checkOut == null) return '--h --m';
    final duration = checkOut.difference(checkIn);
    final hours = duration.inHours;
    final minutes = duration.inMinutes % 60;
    return '${hours.toString().padLeft(2, '0')}h ${minutes.toString().padLeft(2, '0')}m';
  }

  static String determineStatus(
    DateTime checkIn,
    String officeStartTimeStr,
    String lateThresholdStr,
  ) {
    final lateParts = lateThresholdStr.split(':');
    final lateThreshold = DateTime(
      checkIn.year,
      checkIn.month,
      checkIn.day,
      int.parse(lateParts[0]),
      int.parse(lateParts[1]),
    );

    if (checkIn.isAfter(lateThreshold)) {
      return 'Late';
    }
    return 'Present';
  }
}
