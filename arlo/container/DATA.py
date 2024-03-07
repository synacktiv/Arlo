#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
DATA
"""

from .container import ContainerEndian

class DATA(ContainerEndian):
    """ DATA block """
    HDR_SIZE = 0x10

    def __init__(self, stream, addr, endian='<'):
        super().__init__(stream, endian)
        self._offset = addr
        self._addr   = 0
        self._size   = 0
        self._maxsz  = 0
        self._used   = False
        # Force magic, not endian dependant
        self.magic    = bytes(self.__class__.__name__, encoding="ascii")
        self.handle()

    def handle(self):
        """ parse DATA """
        self.hdr_parse(self._endian + "IIII")
        self._addr  = self._obj[0]
        self._size  = self._obj[1]
        self._maxsz = self._obj[2]
        self._used  = self._obj[3] == 1

        if self.is_valid:
            self._str.seek(self._addr - self._offset, 0)
            self._content = self._str.read(self._size)

    def __repr__(self):
        return f'{self.magicstr} {self._size}'

    @property
    def addr(self):
        """ DATA's address property """
        return self._addr

    @property
    def size(self):
        """ DATA's size property """
        return self._size

    @property
    def max_size(self):
        """ DATA's size property """
        return self._maxsz

    @property
    def used(self):
        """ DATA's size property """
        return self._used

    @property
    def is_valid(self):
        """ checks for valid DATA """
        sane = self.used and self.max_size >= self.size
        sane = sane and self.addr > self._offset
        if not sane:
            return sane

        smin = self._str.tell() + self._offset
        self._str.seek(0, 2)
        smax = self._str.tell() + self._offset
        self._str.seek(smin, 0)
        assert smax >= 0
        msg = f"DATA address is out of stream 0 <= {self._addr} <= {smax}"
        assert 0 <= self._addr <= smax, (msg)
        end = self._addr + self._size
        msg = f"DATA size is out of stream 0 <= {end} <= {smax}"
        assert 0 <= end <= smax, (msg)

        return sane
