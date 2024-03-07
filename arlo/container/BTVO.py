#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
BTVO
"""

from struct import unpack
from .container import ContainerEndian
from .FILE import FILE

class BTVO(ContainerEndian):
    """ BTVO container """
    HDR_SIZE = 0x10

    def __init__(self, stream, endian="<"):
        super().__init__(stream, endian)
        self.handle()

    def handle(self):
        """ parse BTVO block """
        self.hdr_parse(self._endian + "4sIII")
        magic    = self._obj[0]
        size     = self._obj[2]
        num_sect = self._obj[3]

        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")

        long = False
        if size == 0x11 and num_sect == 0x12: # TBC
            long = True
            self.log("long")
            self.HDR_SIZE = 0x14
            self.hdr_parse(self._endian + "IIIII")
            size     = self._obj[3]
            num_sect = self._obj[4]

        for i in range(num_sect + 3):
            sect = FILE(self._str, endian=self._endian)
            if sect.is_valid:
                self._sub[f"{sect.magicstr}_{i+2:02}"] = sect
            self._str.seek(FILE.HDR_SIZE, 1)

        if long:
            sect = self._str.read(4)
            #crc16, VO = unpack(self._endian + "H2s", sect)
            _, VO = unpack(self._endian + "H2s", sect)
        else:
            sect = self._str.read(8)
            #_, crc16, VO = unpack(self._endian + "IH2s", sect)
            _, _, VO = unpack(self._endian + "IH2s", sect)
        if (self._endian == "<" and VO != b"VO") or \
                (self._endian == ">" and VO != b"JZ"):
            raise ValueError(f"unexpected trailer {VO}")

        #self.crc(crc16, b"")
