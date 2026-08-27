import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';
import 'package:go_router/go_router.dart';
import '../data/face_verification_service.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  List<CameraDescription> _cameras = [];
  bool _isDetecting = false;
  bool _isVerifying = false;
  String _message = 'Preparing Camera...';

  final FaceDetector _faceDetector = FaceDetector(
    options: FaceDetectorOptions(
      enableContours: true,
      enableClassification: true,
    ),
  );

  // Mock verification service — swap with a real implementation when available
  final FaceVerificationService _verificationService =
      MockFaceVerificationService();

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    _cameras = await availableCameras();
    final frontCamera = _cameras.firstWhere(
      (camera) => camera.lensDirection == CameraLensDirection.front,
      orElse: () => _cameras.first,
    );

    _controller = CameraController(frontCamera, ResolutionPreset.medium);
    await _controller!.initialize();

    if (mounted) {
      setState(() {
        _message = 'Look directly at the camera.';
      });
      _startFaceDetection();
    }
  }

  void _startFaceDetection() {
    _controller!.startImageStream((CameraImage image) async {
      if (_isDetecting || _isVerifying) return;
      _isDetecting = true;

      try {
        // Build InputImage using the new API (no InputImageData / InputImagePlaneMetadata)
        final inputImage = _buildInputImage(image);
        if (inputImage == null) {
          _isDetecting = false;
          return;
        }

        final faces = await _faceDetector.processImage(inputImage);

        if (!mounted) {
          _isDetecting = false;
          return;
        }

        if (faces.isEmpty) {
          setState(() =>
              _message = 'No face detected. Please position your face correctly.');
        } else if (faces.length > 1) {
          setState(() => _message =
              'Multiple faces detected. Please ensure only your face is visible.');
        } else {
          // Exactly one face found — stop stream and run verification
          setState(() {
            _isVerifying = true;
            _message = 'Face Detected ✓ — Verifying Identity...';
          });
          await _controller!.stopImageStream();

          // Capture a still image for verification
          final XFile imageFile = await _controller!.takePicture();
          final File capturedFile = File(imageFile.path);

          final result = await _verificationService.verifyFace(
            capturedImage: capturedFile,
            // In production, pass the employee's registered photo URL here
            registeredImageUrl: 'mock://registered_employee_photo',
          );

          if (!mounted) return;

          if (result.verified) {
            setState(() => _message = 'Identity Verified ✓');
            await Future.delayed(const Duration(milliseconds: 600));
            context.pop(true); // success
          } else {
            setState(() {
              _isVerifying = false;
              _message = 'Face verification failed. Please try again.';
            });
            // Restart stream so the user can retry
            _startFaceDetection();
          }
        }
      } catch (e) {
        debugPrint('Face detection error: $e');
      }
      _isDetecting = false;
    });
  }

  /// Builds an [InputImage] from a [CameraImage] using the current ML Kit API.
  /// Uses [InputImage.fromBytes] with [InputImageMetadata] (new API).
  InputImage? _buildInputImage(CameraImage image) {
    final camera = _controller!.description;

    final rotation =
        InputImageRotationValue.fromRawValue(camera.sensorOrientation);
    if (rotation == null) return null;

    final format = InputImageFormatValue.fromRawValue(image.format.raw);
    if (format == null) return null;

    // For multi-plane images (YUV) concatenate all plane bytes
    final bytes = image.planes
        .expand((plane) => plane.bytes)
        .toList();
    final bytesUint8 = Uint8List.fromList(bytes);

    final metadata = InputImageMetadata(
      size: Size(image.width.toDouble(), image.height.toDouble()),
      rotation: rotation,
      format: format,
      bytesPerRow: image.planes.first.bytesPerRow,
    );

    return InputImage.fromBytes(bytes: bytesUint8, metadata: metadata);
  }

  @override
  void dispose() {
    _controller?.dispose();
    _faceDetector.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    return Scaffold(
      body: Stack(
        fit: StackFit.expand,
        children: [
          CameraPreview(_controller!),
          // Face‑frame overlay
          Center(
            child: Container(
              width: 240,
              height: 300,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.white, width: 2),
                borderRadius: BorderRadius.circular(16),
              ),
            ),
          ),
          // Status message
          SafeArea(
            child: Align(
              alignment: Alignment.bottomCenter,
              child: Container(
                margin: const EdgeInsets.all(24),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.black54,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  _message,
                  style: const TextStyle(color: Colors.white, fontSize: 16),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          ),
          // Close button
          SafeArea(
            child: Align(
              alignment: Alignment.topLeft,
              child: IconButton(
                icon: const Icon(Icons.close, color: Colors.white),
                onPressed: () => context.pop(false),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
