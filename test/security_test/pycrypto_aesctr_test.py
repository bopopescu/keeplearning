#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FileName  : pycrypto_aesctr_test.py
# Author    : wuqingfeng@

from Crypto.Cipher import AES
import hashlib
import binascii
import os

password = 'hello'
plaintext = '13000000001'

def encrypt(plaintext, key, mode, iv):
    encobj = AES.new(key, mode, iv,counter=lambda: os.urandom(16))
    return encobj.encrypt(plaintext)

if __name__ == '__main__':
    key = hashlib.sha256(password).digest()
    iv = hex(10)[2:8].zfill(16)
    print "IV: " + iv
    ciphertext = encrypt(plaintext, key, AES.MODE_CTR, iv)
    # print ciphertext
    print "Cipher (CTR):", binascii.hexlify(bytearray(ciphertext)), ", len:", len(bytearray(ciphertext))