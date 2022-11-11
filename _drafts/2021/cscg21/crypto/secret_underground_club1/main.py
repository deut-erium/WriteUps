from Crypto.PublicKey import RSA
import base64

from secret import FLAG

def main():
    key = RSA.generate(1024)

    p, q, d, e, n = key.p, key.q, key.d, key.e, key.n

    print(f"[DEBUG]: e={e:x}")
    print(f"[DEBUG]: n={n:x}")

    print(
    r"""
 ____  _____ ____  ____  _____ _____    _     _      ____  _____ ____  _____ ____  ____  _     _      ____    ____  _     _     ____ 
/ ___\/  __//   _\/  __\/  __//__ __\  / \ /\/ \  /|/  _ \/  __//  __\/  __//  __\/  _ \/ \ /\/ \  /|/  _ \  /   _\/ \   / \ /\/  _ \
|    \|  \  |  /  |  \/||  \    / \    | | ||| |\ ||| | \||  \  |  \/|| |  _|  \/|| / \|| | ||| |\ ||| | \|  |  /  | |   | | ||| | //
\___ ||  /_ |  \_ |    /|  /_   | |    | \_/|| | \||| |_/||  /_ |    /| |_//|    /| \_/|| \_/|| | \||| |_/|  |  \_ | |_/\| \_/|| |_\\
\____/\____\\____/\_/\_\\____\  \_/    \____/\_/  \|\____/\____\\_/\_\\____\\_/\_\\____/\____/\_/  \|\____/  \____/\____/\____/\____/
                                                                                                                                                                                                                         
Welcome to the secret underground club.
To log in please provide a signature with the private key you received.
""")

    try:
        message = int(input("Message:"), 16)
        signature = int(input("Signature:"), 16)

        if message == pow(signature, e, n) and message > 1 and signature > 1:
            print("Welcome")
            print(FLAG)
        else:
            print("Sorry mate")
    except:
        print("Computer is tired. Computer is going to sleep.")
        exit(1)


if __name__ == '__main__':
    main()