import 'dart:io';

class FaceVerificationResult {
  final bool verified;
  final double confidence;
  final String message;

  FaceVerificationResult({
    required this.verified,
    required this.confidence,
    required this.message,
  });
}

/// Service interface for biometrically verifying an employee's face against their registered profile.
abstract class FaceVerificationService {
  Future<FaceVerificationResult> verifyFace({
    required File capturedImage,
    required String registeredImageUrl,
  });
}

class MockFaceVerificationService implements FaceVerificationService {
  @override
  Future<FaceVerificationResult> verifyFace({
    required File capturedImage,
    required String registeredImageUrl,
  }) async {
    await Future.delayed(const Duration(seconds: 2));
    return FaceVerificationResult(
      verified: true,
      confidence: 0.95,
      message: 'Face verified successfully',
    );
  }
}
