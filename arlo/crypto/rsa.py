#!/usr/bin/python
"""
Arlo firmware extractor
RSA
"""

from os.path import join, dirname

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15

class RSA(): # pylint: disable=too-few-public-methods
    """ RSA handling """
    def __init__(self, fname=None, prefix=None):
        if fname is None:
            if prefix is None:
                fname = join(dirname(__file__), "test_rsa_priv.pem")
            else:
                fname = join(dirname(__file__), f"{prefix}_rsa_priv.pem")
        with open(fname, 'rb') as pem:
            lines = pem.read()
        self.__pkey = load_pem_private_key(lines, None, default_backend())

    def decrypt(self, enc):
        """ decrypt enc using loaded private key """
        return self.__pkey.decrypt(enc, PKCS1v15())
