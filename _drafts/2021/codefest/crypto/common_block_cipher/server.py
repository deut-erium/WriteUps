import os
import random
import socketserver
import threading
import time
from binascii import hexlify, unhexlify

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor

from secret import flag

key = os.urandom(16)
iv = strxor(b'\xff'*16, key)

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            choice = self.request.recv(1).decode()
            cipher = AES.new(key, AES.MODE_CBC, iv)

            if choice == '1':
                self.request.sendall(b'Enter hex to encrypt:')
                data = unhexlify(self.request.recv(1024))
                ret = cipher.encrypt(pad(data, 16))
                self.request.sendall(ret)

            elif choice == '2':
                self.request.sendall(b'Enter hex to decrypt:')
                data = unhexlify(self.request.recv(1024))
                ret = unpad(cipher.decrypt(data), 16)
                self.request.sendall(ret)
            
            elif choice == '3':
                self.request.sendall(b'Give me the key:')
                data = unhexlify(self.request.recv(1024))
                if data == key:
                    self.request.sendall(flag)
                else:
                    print(key.hex())
                    print(iv.hex())
                    self.request.sendall(b'Try harder\n')

        except:
            pass

        finally:
            self.request.sendall(b'bye!\n')

class MyThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass


class MyTCPServer(socketserver.TCPServer):
    pass

if __name__ == '__main__':
    PORT = 9000
    print('serving at PORT', PORT)
    server = MyThreadedServer(('0.0.0.0', PORT), Handler)
    server.allow_reuse_address = True

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    while True:
        time.sleep(20)
