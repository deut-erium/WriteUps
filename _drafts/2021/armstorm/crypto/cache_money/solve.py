import requests
import json
URL = 'https://cachemoney.2021.chall.actf.co/'
ENC = URL+'api/enc'
DEC = URL+'api/dec'

def encrypt(message:bytes,key='secret128'):
    post_data = {'a':list(message)}
    if key in ['secret128','secret192','secret256']:
        post_data['secret']=key
    else:
        post_data['secret']='XXX'
        #key of bytes or bytearray
        post_data['k']=list(key)
    r = requests.post(ENC,json=post_data)
    response = r.json()
    return bytes.fromhex(response['result']),response['time']

def decrypt(message:bytes,key='secret128'):
    post_data = {'a':list(message)}
    if key in ['secret128','secret192','secret256']:
        post_data['secret']=key
    else
        post_data['secret']='XXX'
        #key of bytes or bytearray
        post_data['k']=list(key)
    r = requests.post(DEC,json=post_data)
    response = r.json()
    return bytes.fromhex(response['result']),response['time']


