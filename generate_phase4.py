import os

files = {
    'lib/features/attendance/data/face_verification_service.dart': '''import \\'dart:io\\';

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
      message: \\'Face verified successfully\\',
    );
  }
}
''',
    'lib/features/attendance/screens/camera_screen.dart': '''import \\'package:flutter/material.dart\\';
import \\'package:camera/camera.dart\\';
import \\'package:google_mlkit_face_detection/google_mlkit_face_detection.dart\\';
import \\'package:go_router/go_router.dart\\';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  List<CameraDescription> _cameras = [];
  bool _isDetecting = false;
  String _message = \\'Preparing Camera...\\';
  final FaceDetector _faceDetector = FaceDetector(options: FaceDetectorOptions(enableContours: true, enableClassification: true));
  
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
        _message = \\'Look directly at the camera.\\';
      });
      _startFaceDetection();
    }
  }

  void _startFaceDetection() {
    _controller!.startImageStream((CameraImage image) async {
      if (_isDetecting) return;
      _isDetecting = true;
      
      try {
        final WriteBuffer allBytes = WriteBuffer();
        for (final Plane plane in image.planes) {
          allBytes.putUint8List(plane.bytes);
        }
        final bytes = allBytes.done().buffer.asUint8List();

        final Size imageSize = Size(image.width.toDouble(), image.height.toDouble());
        final imageRotation = InputImageRotationValue.fromRawValue(_controller!.description.sensorOrientation) ?? InputImageRotation.rotation0deg;
        final inputImageFormat = InputImageFormatValue.fromRawValue(image.format.raw) ?? InputImageFormat.nv21;
        
        final planeData = image.planes.map((Plane plane) {
          return InputImagePlaneMetadata(
            bytesPerRow: plane.bytesPerRow,
            height: plane.height,
            width: plane.width,
          );
        }).toList();

        final inputImageData = InputImageData(
          size: imageSize,
          imageRotation: imageRotation,
          inputImageFormat: inputImageFormat,
          planeData: planeData,
        );

        final inputImage = InputImage.fromBytes(bytes: bytes, inputImageData: inputImageData);
        final faces = await _faceDetector.processImage(inputImage);
        
        if (mounted) {
          if (faces.isEmpty) {
            setState(() => _message = \\'No face detected. Please position your face correctly.\\');
          } else if (faces.length > 1) {
            setState(() => _message = \\'Multiple faces detected. Please ensure only your face is visible.\\');
          } else {
            setState(() => _message = \\'Face Detected! Verifying...\\');
            _controller!.stopImageStream();
            await Future.delayed(const Duration(seconds: 1));
            // Simulate verification
            context.pop(true);
          }
        }
      } catch (e) {
        print(e);
      }
      _isDetecting = false;
    });
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
          SafeArea(
            child: Align(
              alignment: Alignment.topLeft,
              child: IconButton(
                icon: const Icon(Icons.close, color: Colors.white),
                onPressed: () => context.pop(false),
              ),
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
