#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
part
"""

from zlib import decompress
from io import BytesIO

from .container import Container
from ..io import peek_magic
from .WTVO import WTVO, WTVO_MAGIC, OVTW_MAGIC

class part(Container):
    """ part container """
    HDR_SIZE = 0x20

    def __init__(self, stream):
        super().__init__(stream)
        self._content_raw = None
        self.handle()

    def handle(self):
        """ parse part block """
        self.hdr_parse("<4sIII16s")
        magic  = self._obj[0]
        ptype  = self._obj[1]
        size   = self._obj[2]
        flags  = self._obj[3]

        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")
        desc = ""
        if ptype == 1:
            desc = desc + "rootfs, "
        elif ptype == 2:
            desc = desc + "generic, "
        elif ptype == 3:
            desc = desc + "kernel, "
        else:
            desc = desc + "unknown, "
        if flags == 0:
            desc = desc + "stored"
        elif flags == 1:
            desc = desc + "compressed"
        elif flags == 2:
            desc = desc + "encrypted"
        elif flags == 3:
            desc = desc + "compressed+encrypted"
        else:
            desc = desc + "unknown"
        self._msg.append(f"{desc}")

        self._content_raw = self._str.read(size)

    def decrypt(self, aes):
        """ decrypt part """
        if aes is not None:
            dec = aes.decrypt(self._content_raw)
            self._content = BytesIO(dec)
            k = 0
            for cont_type, cont in self._parse(self._content):
                self._sub[f"{cont_type}_{k:02}"] = cont
                k += 1
        else:
            self._sub["encrypted_00"] = BytesIO(self._content_raw)

    _formats = {
            b"hsqs": "SquashFS", # unsquashfs
            b"*#$^": "NETGEARHDR0",
            b"UBI#": "UBI", # ubidump
            b"\xd0\x0d\xfe\xed": "pkgtb", # fdtextract/dumpimage
            b"MMM\x00": "MMM",
    }
    def _parse(self, stream):
        """ parse stream based on magic """
        if stream is None:
            yield None

        magic = peek_magic(stream)
        if magic is None:
            yield stream

        try:
            if magic == WTVO_MAGIC:
                ret = WTVO(stream)
                yield (ret.magicstr, ret)
            elif magic == OVTW_MAGIC:
                ret = WTVO(stream, endian=">")
                yield (ret.magicstr, ret)
            elif magic[:2] == b"x\x9c" or magic[:2] == b"x\x01" or \
                 magic[:2] == b"x\xda":
                self._msg.append("zlib")
                yield from self._parse(BytesIO(decompress(stream.read())))
            elif magic in self._formats:
                self.log(self._formats[magic])
                yield (self._formats[magic], stream)
            else:
                self._msg.append(f"unknown magic {magic}")
                yield ("unknown", stream)
        except ValueError as err:
            self._msg.append(f"error parsing container: {err}")
