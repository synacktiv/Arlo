#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
WTVO
"""

from io import BytesIO
from .container import ContainerEndian
from .FILE import FILE
from .BTVO import BTVO
from .PTVO import PTVO

class WTVO(ContainerEndian):
    """ WTVO container """
    HDR_SIZE = 0x8

    def __init__(self, stream, endian='<'):
        super().__init__(stream, endian)
        self._pos = stream.tell()
        self.handle()

    def handle(self):
        """ parse WTVO block """
        self.hdr_parse(self._endian + "4sI")
        magic = self._obj[0]
        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")

        firmware = FILE(self._str, endian=self._endian)
        if firmware.content is not None and len(firmware.content) > 0:
            btvo = BTVO(BytesIO(firmware.content), endian=self._endian)
            self._sub[f"{btvo.magicstr}_00"] = btvo
        else:
            self.log("no firmware")
        self._str.seek(FILE.HDR_SIZE, 1)

        para = FILE(self._str, endian=self._endian)
        if para.content is not None and len(para.content) > 0:
            ptvo = PTVO(BytesIO(para.content), page_size=None, endian=self._endian)
            self._sub[f"{ptvo.magicstr}_00"] = ptvo
        self._str.seek(FILE.HDR_SIZE, 1)

        self.HDR_SIZE = 0x1c
        self.hdr_parse(self._endian + "I20sHH")
        updt_sub = self._obj[0]
        if updt_sub != 0:
            self.log("has update func")
        comment = self._obj[1]
        comment = comment.decode("utf-8").rstrip("\x00\x0d\x0a")
        if len(comment) > 0:
            self.log(f"({comment})")
        crc16   = self._obj[2]

        pos = self._str.tell()
        self._str.seek(self._pos + 0x40, 0)
        check = self._str.read(firmware.size + para.size)
        self._str.seek(pos, 0)

        self.crc(crc16, check)

WTVO_MAGIC = bytes(WTVO.__name__, encoding="ascii")
OVTW_MAGIC = bytes(reversed(WTVO_MAGIC))
