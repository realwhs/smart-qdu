#coding:utf-8
from Crypto.Cipher import AES
from smart_qdu.const import ENCRYPT_KEY
#用于教务账号密码的AES加密解密模块


def encrypt(text):
    while len(text) % 16 != 0:
        text += " "
    obj = AES.new(ENCRYPT_KEY)
    encryption_text = obj.encrypt(text)
    return encryption_text


def decrypt(encryption_text):
    obj = AES.new(ENCRYPT_KEY)
    text = obj.decrypt(encryption_text)
    return text.strip()
