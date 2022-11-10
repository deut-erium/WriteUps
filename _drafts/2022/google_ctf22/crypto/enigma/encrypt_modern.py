#!/usr/bin/python3

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Ian Eldred Pudney

"""Encrypts or decrypts stdin with the provided command-line arguments."""

import os
import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

op = sys.argv[1]
if op != "encrypt" and op != "decrypt":
  raise RuntimeError(f"First argument must be 'encrypt' or 'decrypt', got {sys.argv}")


key = b" ".join(x.strip().encode("utf-8") for x in sys.argv[2:])
if op == "encrypt":
  salt = os.urandom(16)
else:
  salt = sys.stdin.buffer.read(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)
key = base64.urlsafe_b64encode(kdf.derive(key))
f = Fernet(key)

if op == "encrypt":
  plaintext = sys.stdin.buffer.read()
  ciphertext = f.encrypt(plaintext)
  sys.stdout.buffer.write(salt)
  sys.stdout.buffer.write(ciphertext)
else:
  ciphertext = sys.stdin.buffer.read()
  plaintext = f.decrypt(ciphertext)
  sys.stdout.buffer.write(plaintext)

