#!/usr/bin/python
# pylint: disable=invalid-name
"""
Arlo firmware extractor
FILE
"""

from struct import unpack

from .container import ContainerEndian

class FILE(ContainerEndian):
    """ FILE block """
    HDR_SIZE = 0x8

    def __init__(self, stream, endian='<'):
        super().__init__(stream, endian)
        self._type   = None
        self._addr   = 0
        self._size   = 0
        self._pos    = stream.tell()
        # Force magic, not endian dependant
        self.magic    = bytes(self.__class__.__name__, encoding="ascii")
        self.handle()

    def handle(self):
        """ parse FILE """
        curr = self._str.tell()

        self._str.seek(self._pos, 0)
        info = self._str.read(self.HDR_SIZE)
        self._addr, self._size  = unpack(self._endian + "II", info)
        if self.is_valid:
            self._str.seek(self._addr, 0)
            self._content = self._str.read(self._size)
            if len(self._content) >= 4:
                if self._content[:4] == b'\xf8\xf0\x9f\xe5':
                    self._type = 'CODE'
                else:
                    self._type = 'DATA'

        self._str.seek(curr, 0)

    def __repr__(self):
        if self._type is None:
            return 'unparsed'
        if self._type != 'DATA':
            return f'{self._type}'
        return f'{self._type} {self._content[:4]}'

    @property
    def addr(self):
        """ FILE's address property """
        return self._addr

    @property
    def size(self):
        """ FILE's size property """
        return self._size

    @property
    def is_valid(self):
        """ checks for valid FILE """
        sane = self._addr != 0 and self._addr != 0xb and self._size != 0
        if not sane:
            return sane

        smin = self._str.tell()
        self._str.seek(0, 2)
        smax = self._str.tell()
        self._str.seek(smin, 0)
        assert smax >= 0
        msg = f"FILE address is out of stream 0 <= {self._addr} <= {smax}"
        assert 0 <= self._addr <= smax, (msg)
        end = self._addr + self._size
        msg = f"FILE size is out of stream 0 <= {end} <= {smax}"
        assert 0 <= end <= smax, (msg)

        return sane
