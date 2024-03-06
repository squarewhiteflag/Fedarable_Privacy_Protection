from nacl.public import PrivateKey, Box
import requests
import getpass
import hashlib
from requests.exceptions import Timeout
import json

def sendh(data,url):
    

global round_number

def round(round_number,message,url):
    if round_number == 1:
        global private_shamir_key
        private_shamir_key=PrivateKey.generate()
        global public_shamir_key
        public_shamir_key=private_shamir_key.public_key
        response = requests.post(url,json={'key':public_shamir_key})
        print(response)
        response_code = response.status_code
        if response_code == 200:
            round_number += 1
        
