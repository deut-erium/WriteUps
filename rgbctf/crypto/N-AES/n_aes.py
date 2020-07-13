import binascii
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from os import urandom
from random import seed, randint

BLOCK_SIZE = 16


def rand_block(key_seed=urandom(1)):
    seed(key_seed)
    return bytes([randint(0, 255) for _ in range(BLOCK_SIZE)])


def encrypt(plaintext, seed_bytes):
    ciphertext = pad(b64decode(plaintext), BLOCK_SIZE)
    seed_bytes = b64decode(seed_bytes)
    assert len(seed_bytes) >= 8
    for seed in seed_bytes:
        ciphertext = AES.new(rand_block(seed), AES.MODE_ECB).encrypt(ciphertext)

    return b64encode(ciphertext)


def decrypt(ciphertext, seed_bytes):
    plaintext = b64decode(ciphertext)
    seed_bytes = b64decode(seed_bytes)
    for byte in reversed(seed_bytes):
        plaintext = AES.new(rand_block(byte), AES.MODE_ECB).decrypt(plaintext)

    return b64encode(unpad(plaintext, BLOCK_SIZE))


def gen_chall(text):
    text = pad(text, BLOCK_SIZE)
    for i in range(128):
        text = AES.new(rand_block(), AES.MODE_ECB).encrypt(text)

    return b64encode(text)


def main():
    challenge = b64encode(urandom(64))
    print(gen_chall(challenge).decode())
    while True:
        print("[1] Encrypt")
        print("[2] Decrypt")
        print("[3] Solve challenge")
        print("[4] Give up")

        command = input("> ")

        try:
            if command == '1':
                text = input("Enter text to encrypt, in base64: ")
                seed_bytes = input("Enter key, in base64: ")
                print(encrypt(text, seed_bytes))
            elif command == '2':
                text = input("Enter text to decrypt, in base64: ")
                seed_bytes = input("Enter key, in base64: ")
                print(decrypt(text, seed_bytes))
            elif command == '3':
                answer = input("Enter the decrypted challenge, in base64: ")
                if b64decode(answer) == challenge:
                    print("Correct!")
                    print("Here's your flag:")
                    with open("flag", 'r') as f:
                        print(f.read())
                else:
                    print("Incorrect!")
                break
            elif command == '4':
                break
            else:
                print("Invalid command!")
        except binascii.Error:
            print("Base64 error!")
        except Exception:
            print("Error!")

    print("Bye!")


if __name__ == '__main__':
    main()
