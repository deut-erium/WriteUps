from Crypto.PublicKey import RSA
import base64
import os

from secret import FLAG

challenge = int.from_bytes(f"challenge_{os.urandom(8).hex()}".encode(), 'big')

def menu():
    print(
        r"""
[1] Login
[2] Support
[3] Exit
        """
    )
    return int(input("Option:"))

def int_to_bytes(i):
    return i.to_bytes((i.bit_length() + 7) // 8, 'big')

def chat():
    message = int(input("Message:"), 16)

    if b"challenge_" in int_to_bytes(message).lower():
        print("This message looks like a challenge")
    else:
        # TODO: Implement actual chat. Currently it's just a dummy.
        answer = message # put actual answer here
        signature = pow(answer, d, n)
        print(f"{message:x}#{signature:x}")

def login():
    print(f"Provide a valid signature for the following challenge: {challenge:x}")
    signature = int(input("Signature:"), 16)

    if challenge == pow(signature, e, n) and challenge > 1 and signature > 1:
        print("Welcome")
        print(FLAG)
    else:
        print("Sorry mate")

def main():
    global p, q, d, e, n
    key = RSA.generate(1024)

    p, q, d, e, n = key.p, key.q, key.d, key.e, key.n

    print(f"[DEBUG]: e={e:x}")
    print(f"[DEBUG]: n={n:x}")

    used_support = False

    print(
    r"""
 ____  _____ ____  ____  _____ _____    _     _      ____  _____ ____  _____ ____  ____  _     _      ____    ____  _     _     ____ 
/ ___\/  __//   _\/  __\/  __//__ __\  / \ /\/ \  /|/  _ \/  __//  __\/  __//  __\/  _ \/ \ /\/ \  /|/  _ \  /   _\/ \   / \ /\/  _ \
|    \|  \  |  /  |  \/||  \    / \    | | ||| |\ ||| | \||  \  |  \/|| |  _|  \/|| / \|| | ||| |\ ||| | \|  |  /  | |   | | ||| | //
\___ ||  /_ |  \_ |    /|  /_   | |    | \_/|| | \||| |_/||  /_ |    /| |_//|    /| \_/|| \_/|| | \||| |_/|  |  \_ | |_/\| \_/|| |_\\
\____/\____\\____/\_/\_\\____\  \_/    \____/\_/  \|\____/\____\\_/\_\\____\\_/\_\\____/\____/\_/  \|\____/  \____/\____/\____/\____/
                                                                                                                                                                                                                         
Welcome to the secret underground club.
To log in please provide a signature with the private key you received.

We had some issues with the login system and changed the procedure. 
If you have problems with the new process please ask our support team (of course all messages are signed by the support team, so you know it's us).
""")

    try:
        while True:
            option = menu()
            print()

            if option == 1:
                login()
            elif option == 2:
                if used_support:
                    print("Due to high demand we limited the support requests to one per login attempt")
                else:
                    chat()
                    used_support = True
            else:
                exit(0)
    except SystemExit:
        pass
    except:
        print("Computer is tired. Computer is going to sleep.")
        exit(1)


if __name__ == '__main__':
    main()