from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from datetime import datetime, timedelta

challenge_description("You can generate an access token for my network service, but you shouldn't be able to read the flag... I think.")
challenge_name = "It's as easy as access=0000"
FLAG = "ractf{XXX}"
KEY = get_random_bytes(16)

def get_flag(token, iv):
    token = bytes.fromhex(token)
    iv = bytes.fromhex(iv)
    try:
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(token)
        unpadded = unpad(decrypted, 16)
    except ValueError as e:
        return {"error": str(e)}
    if b"access=0000" in unpadded:
        return {"flag": FLAG}
    else:
        return {"error": "not authorized to read flag"}

def generate_token():
    expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")
    token = f"access=9999;expiry={expires_at}".encode()
    iv = get_random_bytes(16)
    padded = pad(token, 16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    ciphertext = iv.hex() + encrypted.hex()
    return {"token": ciphertext}

def start_challenge():
  menu = "Would you like to:\n[1] Create a guest token\n[2] Read the flag"
  while True:
    print(menu)
    choice = str(input("Your choice: "))
    while choice != "1" and choice != "2":
        choice = str(input("Please enter a valid choice. Try again: "))
    if choice == "1":
      print(generate_token())
    elif choice == "2":
      token = input("Please enter your admin token: ")
      while not token:
        token = input("Tokens can't be empty. Try again: ")
      iv = input("Please enter your token's initialization vector: ")
      while not iv:
        iv = input("Initialization vectors can't be empty. Try again: ")
      print(get_flag(token, iv))
 
start_challenge()