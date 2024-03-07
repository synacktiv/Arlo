#!/usr/bin/python -u
"""
Arlo firmware extractor
binary parser
"""

from copy import deepcopy

from .container.cimg import CIMG_MAGIC
from .container.ITVO import ITVO_MAGIC
from .io import write, append

TEMPLATE_PREFIX = """
from glob import glob
import ida_segment, ida_bytes, ida_idp, ida_auto, ida_kernwin, ida_pro

ida_idp.set_processor_type("arm", ida_idp.SETPROC_LOADER)
phy_segs = [
    # SRAM
    [ 0x10000000, 0x000fffff, "SRAM_CODE",       "CODE", ],
    [ 0x10190000, 0x00008000, "system_internal", "DATA", ],
    # DDR
    [ 0x20000000, 0x007effff, "DDR_CODE",        "CODE", ],
    [ 0x207f0000, 0x00010000, "d2_reg_table",    "DATA", ],
    [ 0x207e0000, 0x00010000, "asrp_fw",         "DATA", ],
    [ 0x20780000, 0x00060000, "dspg_fw",         "DATA", ],
    [ 0x27c00000, 0x00100000, "vam_md_model",    "DATA", ],
    [ 0x90000000, 0x0fffffff, "TBD0",            "IO",   ],
    [ 0xA0000000, 0x0fffffff, "TBD1",            "IO",   ],
    [ 0xC0000000, 0x0fffffff, "TBD2",            "IO",   ],
]
# IO: https://hex-rays.com/products/decompiler/manual/tricks.shtml#01
for seg in phy_segs:
    if seg[0] + seg[1] > 0xffffffff:
        print("[!] clamp segment size to max 0xffffffff")
        seg[1] = 0xffffffff - seg[0]

    if seg[3] == "CODE":
        flags = ida_segment.ADDSEG_SPARSE|ida_segment.ADDSEG_OR_DIE
    else:
        flags = ida_segment.ADDSEG_SPARSE|ida_segment.ADDSEG_NOAA
    if ida_segment.add_segm(0, seg[0], seg[0] + seg[1], seg[2], seg[3], flags) != 1:
        print(f"[!] ida_segment.add_segm ({seg[2]}) error")

segs = """

TEMPLATE_SUFFIX = """
for seg in segs:
    f_ea = seg["addr"]
    files = glob(seg["id"])
    if len(files) == 1:
        with open(files[0], "rb") as file:
            ida_bytes.put_bytes(f_ea, file.read())
    else:
        print(f"[!] multiple input bytes candidates: {files}")

for seg in filter(lambda s: "CODE" in s[3], phy_segs):
    ida_auto.plan_range(seg[0], seg[0] + seg[1])

if ida_auto.auto_wait():
    ida_idp.process_config_directive("PACK_DATABASE=2");
    ida_pro.qexit(0)
"""

def write_idp_helpers(path, info, name, glob_prefix, suffix=""):
    """ write IDA scripts for config """
    curr_info = deepcopy(info)
    for seg in curr_info:
        file_id   = seg["id"]
        seg["id"] = f"{glob_prefix}{file_id:02}.bin"
    write(path, f"{name}{suffix}.py", idb_script(curr_info).encode('utf-8'))

    cmdline = f"idapro -pARM -S{name}{suffix}.py -t -A {name}{suffix}.idb\n"
    append(path, f"create_idb{suffix}.sh", cmdline)

def prepare_idb(path, config, container):
    """ write IDA scripts for each fw of config """
    if container.magic == CIMG_MAGIC:
        for name in config:
            glob_prefix = "./*WTVO_[0-9][0-9]-BTVO_[0-9][0-9]-FILE_"
            write_idp_helpers(path, config[name], name, glob_prefix)
    elif container.magic == ITVO_MAGIC:
        i = 0
        for suffix in ["-current", "-recovery"]:
            for name in config:
                glob_prefix = f"./*ITVO_00-BTVO_{i:02}-FILE_"
                write_idp_helpers(path, config[name], name, glob_prefix, suffix)
            i += 1

def idb_script(info):
    """ return loading IDA script for specific fw """
    return TEMPLATE_PREFIX + str(info) + TEMPLATE_SUFFIX
