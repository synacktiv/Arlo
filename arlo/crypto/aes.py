#!/usr/bin/python
"""
Arlo firmware extractor
AES
"""

import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers.algorithms import AES256

class AES():
    """ AES handling """
    _SALT   = b"\xb3\x1a\xa1\xa9\xa2\x2b\xd3\xc6"
    _KEYLEN = 32
    _IVLEN  = 16
    def __init__(self, secret, count=10, algo='sha1'):
        self.__secret = secret
        self.__algo   = algo
        self.__count  = count
        (key, iv) = self.EVP_BytesToKey() # pylint: disable=invalid-name
        self.__cipher = Cipher(AES256(key), CBC(iv))

    def decrypt(self, enc):
        """ decrypt enc using loaded key/iv """
        decryptor = self.__cipher.decryptor()
        return decryptor.update(enc) + decryptor.finalize()

    def digest(self, block):
        """ hash block """
        digest = hashlib.new(self.__algo)
        digest.update(block)
        return digest.digest()

    def pbkdf1(self, block=''):
        """ perform pbkdf1 on block """
        dgst = self.digest(block + self.__secret + self._SALT)
        for _ in range(self.__count - 1):
            dgst = self.digest(dgst)
        return dgst

    def EVP_BytesToKey(self): # pylint: disable=invalid-name
        """ see https://www.openssl.org/docs/man3.1/man3/EVP_BytesToKey.html """
        stream = b''
        block = b''
        while len(stream) < (self._KEYLEN + self._IVLEN):
            block = self.pbkdf1(block)
            stream += block

        return (stream[:self._KEYLEN],
                stream[self._KEYLEN:self._KEYLEN+self._IVLEN])
