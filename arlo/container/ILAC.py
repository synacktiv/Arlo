#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
ILAC
"""

from .container import ContainerEndian
from .DATA import DATA

class ILAC(ContainerEndian):
    """ ILAC container """
    HDR_SIZE  = 0x10
    PAGE_SIZE = 0x500

    # kvstore
    # 0x10: "HK_TOKEN", 0x11: "2G_PASSWD", 0x12: "DSC2_CERT", 0x14: "ASLV_DEK"
    # +1

    def __init__(self, stream, addr, endian="<"):
        super().__init__(stream, endian)
        self._addr = addr
        self.handle()

    def handle(self):
        """ parse ILAC block """
        self.hdr_parse(self._endian + "4sIII")
        magic    = self._obj[0]

        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")

        i = 0
        while (self._str.tell()) <= self.PAGE_SIZE:
            _pos = self._str.tell()
            sect = DATA(self._str, self._addr, endian=self._endian)
            if sect.is_valid:
                self._sub[f"{sect.magicstr}_{i+2:02}"] = sect
            self._str.seek(_pos + DATA.HDR_SIZE, 0)
            i += 1
