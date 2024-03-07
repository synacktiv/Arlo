#!/usr/bin/python
"""
Arlo firmware extractor
DSA
"""

from os.path import join, dirname

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA1
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from asn1crypto.algos import DSASignature

class DSA(): # pylint: disable=too-few-public-methods
    """ DSA handling """
    def __init__(self, fname=None, prefix=None):
        if fname is None:
            if prefix is None:
                fname = join(dirname(__file__), "test_dsa_pub.pem")
            else:
                fname = join(dirname(__file__), f"{prefix}_dsa_pub.pem")
        with open(fname, "rb") as pem:
            lines = pem.read()
        self.__pkey = load_pem_public_key(lines, default_backend())

    def verify(self, sig, data):
        """ verify data against sig using loaded public key """
        dsasig = DSASignature.load(sig, strict=False) # strip ExtraData
        return self.__pkey.verify(dsasig.dump(), data, SHA1())
