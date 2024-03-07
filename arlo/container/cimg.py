#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
cimg
"""

from datetime import datetime

from cryptography.exceptions import InvalidSignature

from ..crypto.dsa import DSA
from ..crypto.rsa import RSA
from ..crypto.aes import AES

from .container import Container
from .part import part

class cimg(Container):
    """ cimg container """
    #HDR_SIZE = 0x178
    HDR_SIZE = 0

    def __init__(self, stream):
        super().__init__(stream)
        self._aes       = None
        self._num_parts = 0
        self.handle()

    def handle_crypto(self, key, signature, signed, prefix):
        """ decrypt and verify signature """
        try:
            a_dsa = DSA(prefix=prefix)
            a_dsa.verify(signature, signed)
        except InvalidSignature:
            self.log("invalid signature")
        except FileNotFoundError:
            self.log("signature unsupported")

        try:
            self._aes = AES(RSA(prefix=prefix).decrypt(key))
        except ValueError as e:
            self.log(f"{e.args[0]}")
        except FileNotFoundError:
            self.log("decryption unsupported")

    def handle(self):
        """ parse cimg block """
        _pos = self._str.tell()
        self.HDR_SIZE = 0x10
        self.hdr_parse("<4sIII")
        magic      = self._obj[0]
        version    = self._obj[1]
        hdr_size   = self._obj[2]
        total_size = self._obj[3]

        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")

        self.log(f"v{version}")
        comment = b''
        self.HDR_SIZE = hdr_size - 0x10
        if version == 1:
            self.hdr_parse("<72s256s16sIIII")
            signature  = self._obj[0]
            key        = self._obj[1]
            #hw_rev     = self._obj[3]
            #fw_rev     = self._obj[4]
            timestamp  = self._obj[5]
            num_parts  = self._obj[6]
        elif version == 2:
            self.hdr_parse("<104s256s20sIII")
            signature  = self._obj[0]
            key        = self._obj[1]
            comment    = self._obj[2]
            timestamp  = self._obj[4]
            num_parts  = self._obj[5]
        else:
            raise ValueError(f"unexpected header version {version:04x}")

        #if hdr_size != self.HDR_SIZE:
        #    raise ValueError(f"unexpected header size {hdr_size:04x}")
        if num_parts <= 0:
            raise ValueError(f"unexpected num parts {num_parts:04x}")

        timestamp = datetime.fromtimestamp(timestamp).isoformat()
        self.log(f"{timestamp}")
        comment = comment.decode("utf-8").rstrip("\x00\x0d\x0a")
        if len(comment) > 0:
            self.log(f"({comment})")

        if version == 1:
            curr = self._str.tell()
            signed = b''
            self._str.seek(_pos, 0)
            signed = signed + self._str.read(16)
            self._str.seek(_pos + 0x58, 0)
            signed = signed + self._str.read(total_size)
            self._str.seek(curr, 0)
            self.handle_crypto(key, signature, signed, f"{self.magicstr}_v{version}")
        else:
            signed = b''
            self.handle_crypto(key, signature, signed, f"{self.magicstr}_v{version}")

        for idx in range(num_parts):
            cpart = part(self._str)
            cpart.decrypt(self._aes)
            self._sub[f"part_{idx:02}"] = cpart

CIMG_MAGIC = bytes(cimg.__name__, encoding='ascii')
