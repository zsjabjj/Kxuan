# coding: utf8
import random
import string
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class Prpcrypt(object):
    def __init__(self):
        random.seed()
        chars = string.ascii_letters + string.digits
        suiji = ''.join([random.choice(chars) for _ in range(16)])
        self.key = suiji
        self.mode = AES.MODE_CBC

        # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        text = text.encode("utf-8")
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 128
        count = len(text)
        # print(count)
        add = length - (count % length)
        # print(add)
        text = text + (b'\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode("ASCII")

        # 解密后，去掉补足的空格用strip() 去掉

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(b'\0').decode("utf-8")


if __name__ == '__main__':
    # random.seed()
    # chars = string.ascii_letters + string.digits
    # suiji = ''.join([random.choice(chars) for _ in range(16)])
    # pc = Prpcrypt(suiji)  # 初始化密钥
    pc = Prpcrypt()  # 初始化密钥
    e = pc.encrypt("my book is free")
    d = pc.decrypt(e)
    print(e, d)
    e = pc.encrypt("123456")
    d = pc.decrypt(e)
    print(e, d)
    print(len(e))

















# from Crypto import Random
# from Crypto.Cipher import AES
# import base64
# from hashlib import md5
#
# def pad(data):
#     length = 16 - (len(data) % 16)
#     data = data.encode()
#     return data + (chr(length)*length).encode()
#
# def unpad(data):
#     return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]
#
# def bytes_to_key(data, salt, output=48):
#     # extended from https://gist.github.com/gsakkis/4546068
#     assert len(salt) == 32, len(salt)
#     data = data.encode()
#     data += salt
#     key = md5(data).digest()
#     print(key)
#     final_key = key
#     while len(final_key) < output:
#         key = md5(key + data).digest()
#         final_key += key
#     return final_key[:output]
#
# def encrypt(message, passphrase):
#     salt = Random.new().read(32)
#     # salt = Random.new()
#     print(salt)
#     key_iv = bytes_to_key(passphrase, salt, 32+16)
#     key = key_iv[:32]
#     iv = key_iv[32:]
#     aes = AES.new(key, AES.MODE_CBC, iv)
#     return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))
#
# def decrypt(encrypted, passphrase):
#     encrypted = base64.b64decode(encrypted)
#     assert encrypted[0:8] == b"Salted__"
#     salt = encrypted[8:16]
#     key_iv = bytes_to_key(passphrase, salt, 32+16)
#     key = key_iv[:32]
#     iv = key_iv[32:]
#     aes = AES.new(key, AES.MODE_CBC, iv)
#     return unpad(aes.decrypt(encrypted[16:]))
#
# message = 'haha'
# passphrase = 'hehe'
# a = encrypt(message, passphrase)
# print(a)
# print(len(a))

