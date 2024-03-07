#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
PTVO
"""

from struct import pack
from io import BytesIO
from .container import ContainerEndian
from .YTVO import YTVO

class PTVO(ContainerEndian):
    """ PTVO container """
    HDR_SIZE  = 0x0c

    def __init__(self, stream, page_size=None, endian="<"):
        super().__init__(stream, endian)
        self._page_size = page_size
        self._rev_crc = False
        self.handle()

    def handle(self):
        """ parse PTVO block """
        self.hdr_parse(self._endian + "4sIH2s")
        magic    = self._obj[0]
        size     = self._obj[1]
        crc16    = self._obj[2]
        VO       = self._obj[3]

        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")

        if (self._endian == "<" and VO != b"VO") or \
                (self._endian == ">" and VO != b"JZ"):
            raise ValueError(f"unexpected trailer {VO}")

        self.crc(crc16, pack(self._endian + "4sI", magic, size))

        _pos = self._str.tell()
        self._str.seek(0, 2)
        smax = self._str.tell()
        self._str.seek(_pos, 0)
        assert smax >= 0
        assert 0 <= size <= smax, (f"invalid size (0 <= {size:x} <= {smax:x})")

        self._content = BytesIO(self._str.read(size))
        self._str.seek(_pos, 0)

        self.HDR_SIZE = 0x14
        self.hdr_parse(self._endian + "IIIIH2s")
        num_para  = self._obj[0]
        para_size = self._obj[1]
        crc16     = self._obj[4]
        WO        = self._obj[5]

        if WO != b"WO":
            raise ValueError(f"unexpected magic3 {WO}")

        self.crc(crc16, pack(self._endian + "IIII", num_para, para_size,
                             self._obj[2], self._obj[3]))

        if self._page_size is not None:
            self._str.seek(self._page_size, 0)
        for i in range(num_para):
            data = BytesIO(self._str.read(para_size))
            ytvo = YTVO(data, size=para_size, page_size=self._page_size,
                        endian=self._endian)
            self._sub[f"{ytvo.magicstr}_{i:02}"] = ytvo
