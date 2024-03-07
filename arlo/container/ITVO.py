#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
ITVO
"""

from .container import ContainerEndian
from .FILE import FILE
from .BTVO import BTVO
from .PTVO import PTVO
from .ILAC import ILAC

class ITVO(ContainerEndian):
    """ ITVO container """
    HDR_SIZE  = 0x4c
    PAGE_SIZE = 0x1000

    def __init__(self, stream, endian="<"):
        super().__init__(stream, endian)
        # Force magic, not endian dependant
        self.magic    = bytes(self.__class__.__name__, encoding="ascii")
        self.handle()

    def handle(self):
        """ parse BTVO block """
        self.hdr_parse(self._endian + "4s18I")
        magic    = self._obj[0]

        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")

        firmware = FILE(self._str, endian=self._endian)
        if firmware.is_valid:
            self._sub["BTVO_00"] = BTVO(firmware.stream)
        self._str.seek(FILE.HDR_SIZE, 1)

        para = FILE(self._str, endian=self._endian)
        if para.is_valid:
            self._sub["PTVO_01"] = PTVO(para.stream, page_size=self.PAGE_SIZE)
        self._str.seek(FILE.HDR_SIZE, 1)

        firmware = FILE(self._str, endian=self._endian)
        if firmware.is_valid:
            self._sub["BTVO_03"] = BTVO(firmware.stream)
        self._str.seek(FILE.HDR_SIZE, 1)

        para = FILE(self._str, endian=self._endian)
        if para.is_valid:
            self._sub["PTVO_04"] = PTVO(para.stream,
                                             page_size=self.PAGE_SIZE)
        self._str.seek(FILE.HDR_SIZE, 1)

        ilac = FILE(self._str, endian=self._endian)
        if ilac.is_valid:
            self._sub["CALI_05"] = ILAC(ilac.stream, ilac.addr)
        self._str.seek(FILE.HDR_SIZE, 1)

        logs = FILE(self._str, endian=self._endian)
        if logs.is_valid:
            self._sub["LOGS_06"] = logs
        self._str.seek(FILE.HDR_SIZE, 1)

ITVO_MAGIC = bytes(ITVO.__name__, encoding='ascii')
