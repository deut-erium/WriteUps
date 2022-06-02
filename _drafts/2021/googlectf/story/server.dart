#!/usr/bin/env dart

import 'dart:convert';
import 'dart:io';

// NOTE: calculate and randomize functions are private (i.e., you don't have access).
import 'package:ctf_story/private.dart' show calculate, randomize;

int main(List<String> arguments) {
  final flag = File('flag.txt').readAsStringSync();
  print('Hello! Please tell me a fairy tale!');
  var line = stdin.readLineSync(encoding: utf8);
  if (utf8.encode(line).where((i) => i < 32 || i >= 128).isNotEmpty) {
    print('There are unprintable characters in your story.');
    return 0;
  }
  final firstText = line.toLowerCase();
  var crcValues = calculate(utf8.encode(line));
  print('The CRC values of your text are $crcValues.');
  List<String> expectedValues;
  do {
    expectedValues = randomize(utf8.encode(line));
  } while (expectedValues == crcValues);
  if (expectedValues == null) {
    print('Your story is too short. Bye!');
    return 0;
  }
  print('But I am looking for a story of $expectedValues.');
  line = stdin.readLineSync(encoding: utf8);
  final secondText = line.toLowerCase();
  crcValues = calculate(utf8.encode(line));
  if (firstText != secondText) {
    print('Perhaps you would like to start from scratch? Bye!');
    return 0;
  }
  if (List.generate(
              expectedValues.length, (i) => crcValues[i] == expectedValues[i])
          .indexOf(false) <
      0) {
    print('What a lovely story! Your flag is ${flag}');
  }
  print('Bye!');
  return 0;
}
