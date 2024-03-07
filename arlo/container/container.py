#!/usr/bin/python
"""
Arlo firmware extractor
Container
"""

from struct import unpack, pack
from io import BytesIO

try:
    from fastcrc.crc16 import xmodem
    CRC16 = True
except ModuleNotFoundError:
    print("no CRC16")
    CRC16 = False

class Container:
    """ generic container """
    HDR_SIZE = 4
    def __init__(self, stream):
        self._hdr     = None
        self._content = None
        self._obj     = None
        self._str     = stream
        self._msg     = []
        self.magic    = bytes(self.__class__.__name__, encoding="ascii")
        self._sub     = {}

    def hdr_parse(self, fmt):
        """ parse header from stream """
        self._hdr = self._str.read(self.HDR_SIZE)
        self._obj = unpack(fmt, self._hdr)

    @property
    def hdr(self):
        """ header bytes """
        return self._hdr

    @property
    def content(self):
        """ content bytes """
        return self._content

    @property
    def stream(self):
        """ content bytes stream """
        return BytesIO(self._content)

    @property
    def contained(self):
        """ content containers """
        if self._sub is None:
            return None
        return dict(sorted(self._sub.items()))

    @property
    def magicstr(self):
        """ magic as a string """
        return self.magic.decode("ascii")

    def __repr__(self):
        """ show details """
        return f"{self.magicstr} {self._sub}"

    def log(self, msg):
        """ add to logs """
        self._msg.append(msg)

    def get_logs(self):
        """ retrieve log string """
        msg = []
        logs = ", ".join(self._msg)

        if logs != "":
            msg = [": ".join([self.magicstr, logs])]

        if self.contained is not None:
            for _, value in self.contained.items():
                if hasattr(value, "get_logs"):
                    submsg = value.get_logs()
                    if submsg is not None and len(submsg) > 0:
                        msg.append(submsg)

        return " / ".join(msg)

class ContainerEndian(Container):
    """ container with endianness information """
    def __init__(self, stream, endian="<"):
        super().__init__(stream)
        if endian not in ("<", ">"):
            raise ValueError(f"invalid endianness {endian}")
        self._endian = endian
        if endian == ">":
            self.magic = bytes(reversed(self.magic))
            self._rev_crc = False
        else:
            self._rev_crc = True

    def crc(self, expected, data):
        """ check content's CRC """
        if CRC16 is False:
            return
        calc = xmodem(data)
        if self._rev_crc:
            calc = unpack(">H", pack("<H", calc))[0]
        if expected != calc:
            self.log(f"invalid CRC ({expected:x} {calc:x})")
