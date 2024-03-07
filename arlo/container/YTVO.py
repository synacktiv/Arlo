#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
YTVO
"""

from struct import pack

from .container import ContainerEndian

class YTVO(ContainerEndian):
    """ YTVO block """
    HDR_SIZE  = 0x10

    def __init__(self, stream, size, page_size=None, endian='<'):
        super().__init__(stream, endian)
        self._page_size = page_size
        self._size      = size - self.HDR_SIZE
        ## Force magic, not endian dependant
        #self.magic      = bytes(self.__class__.__name__, encoding="ascii")
        self._rev_crc = False
        self.handle()

    def handle(self):
        """ parse YTVO """
        self.hdr_parse(self._endian + "4sIHHH2s")
        magic    = self._obj[0]
        size     = self._obj[1]
        crc16    = self._obj[4]
        VO       = self._obj[5]

        if magic == b'\x00\x00\x00\x00': # para never set
            self._content = self._str.read(self._size).strip(b'\x00')
            return

        if magic != self.magic:
            raise ValueError(f"unexpected magic {magic}")

        if VO != b"VO":
            raise ValueError(f"unexpected trailer {VO}")

        self.crc(crc16, pack(self._endian + "4sIHH", magic, self._obj[1],
                             self._obj[2], self._obj[3]))

        if self._page_size is not None:
            self._str.seek(self._page_size, 0)
            #self._content = self._str.read(self._size - self._page_size)
            self._content = self._str.read(self._page_size).strip(b'\xff')
            self._content = self._content.strip(b'\x00')
            if len(self._content) != size:
                self.log("inconsistent para env size")
        else:
            self._content = self._str.read(self._size)

    def __repr__(self):
        return f'DATA {self._content[:4]} '
