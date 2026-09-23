import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// Screen managing the password recovery flow via OTP verification.
class ForgotPasswordScreen extends StatefulWidget {
  const ForgotPasswordScreen({super.key});

  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  int _step = 1;
  final _emailController = TextEditingController();
  final _otpController = TextEditingController();
  final _passController = TextEditingController();
  
  bool _isLoading = false;

  void _nextStep() async {
    setState(() => _isLoading = true);
    await Future.delayed(const Duration(seconds: 1));
    setState(() => _isLoading = false);

    if (_step == 1 && _emailController.text.isNotEmpty) {
      // Send OTP
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Demo OTP is 123456')));
      setState(() => _step = 2);
    } else if (_step == 2 && _otpController.text == '123456') {
      setState(() => _step = 3);
    } else if (_step == 3 && _passController.text.isNotEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Password Reset Successful!')));
      context.pop();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Invalid input, please check.')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Forgot Password')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (_step == 1) ...[
              const Text('Enter your Email or Mobile', style: TextStyle(fontSize: 18)),
              const SizedBox(height: 16),
              TextField(controller: _emailController, decoration: const InputDecoration(labelText: 'Email / Mobile')),
            ],
            if (_step == 2) ...[
              const Text('Enter OTP', style: TextStyle(fontSize: 18)),
              const SizedBox(height: 16),
              TextField(controller: _otpController, decoration: const InputDecoration(labelText: 'OTP')),
            ],
            if (_step == 3) ...[
              const Text('Create New Password', style: TextStyle(fontSize: 18)),
              const SizedBox(height: 16),
              TextField(controller: _passController, obscureText: true, decoration: const InputDecoration(labelText: 'New Password')),
            ],
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _isLoading ? null : _nextStep,
              child: _isLoading ? const CircularProgressIndicator() : Text(_step == 3 ? 'Reset Password' : 'Continue'),
            )
          ],
        ),
      ),
    );
  }
}
