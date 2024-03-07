#!/usr/bin/python
"""
Arlo firmware extractor
binary parser
"""

from io import BytesIO

from .container.cimg import cimg, CIMG_MAGIC
from .container.ITVO import ITVO, ITVO_MAGIC
from .data import Arlo
from .ida import prepare_idb
from .io import download, write, peek_magic

def parse(stream):
    """ parse update binary """
    magic = peek_magic(stream)
    if magic is None:
        return None

    try:
        if magic == CIMG_MAGIC:
            return cimg(stream)
        if magic == ITVO_MAGIC:
            return ITVO(stream)
    except ValueError as err:
        print(f" (error parsing data: {magic}) ", end="")
        print(err)

    return None

def recurse_dump(container, name, i, ctype="unknown"):
    """ get data from parsed container """
    if container is None:
        yield None

    if not hasattr(container, "contained") or len(container.contained) == 0:
        name = name + f"-{ctype}"
        if hasattr(container, "content") and container.content is not None:
            yield {name: container.content}
        else:
            yield {name: container}

    else:
        name = name + f"-{container.magicstr}_{i:02}"

        if container.contained is not None and len(container.contained) > 0:
            for cctype, cont in container.contained.items():
                yield from recurse_dump(cont, name, i, cctype)
                i += 1
        else:
            if container.content is not None:
                yield {name: container.content}
            else:
                print(f"no data found! {name}")
                yield None

def dump(container, name):
    """ get data from parsed container """
    print(container.get_logs(), end="")
    if container.contained is not None:
        for i, cont in enumerate(container.contained.values()):
            yield from recurse_dump(cont, name, i)

def extract(path, data, i=0, config=None):
    """ extract and write containers from binary """
    if data is None or len(data) == 0:
        print("no data", end="")
        return
    container = parse(BytesIO(data))
    if container is None:
        print(f"unexpected container {peek_magic(BytesIO(data))}", end="")
        write(path, f"unknown_{i:02}.bin", data)
        return
    for sections in dump(container, f"{container.magicstr}_{i:02}"):
        if sections is None:
            print(" no data", end="")
        elif isinstance(sections, (dict)):
            for j in sections:
                if isinstance(sections[j], (bytes)):
                    write(path, f"{j}.bin", sections[j])
                elif isinstance(sections[j], (BytesIO)):
                    write(path, f"{j}.bin", sections[j].read())
                else:
                    raise ValueError(f"unhandled write for {type(sections[j])}")
        else:
            raise ValueError(f"unexpected dump type: {sections}")

    if config is not None:
        prepare_idb(path, config, container)

    return

def update_all(prefix, keep=True):
    """ download and write updates for all models """
    for key, class_info in Arlo.models.items():
        print(f"- {key}")
        for code, model_info in class_info.items():
            print(f"  - {model_info['name']}")

            firmwares = download(key, code, prefix, keep)
            if firmwares is None or len(firmwares) == 0:
                continue

            for i, firmware in enumerate(firmwares):
                if firmware["data"] is None:
                    print("empty dl")
                    continue

                print(f"    - {firmware['fname']:55s} ", end="")

                config = model_info.get("config", None)
                extract(firmware["path"], firmware["data"], i, config)
                print()

def update_one(prefix, key, code, model_info, keep=True):
    """ download and write updates for specific model """
    firmwares = download(key, code, prefix, keep)
    if firmwares is None or len(firmwares) == 0:
        return "no update found"

    ret = ""
    for i, firmware in enumerate(firmwares):
        if firmware["data"] is None:
            ret = ", ".join([ret, "empty dl"])
            continue

        print(f"- {firmware['fname']}: ", end="")
        config = model_info.get("config", None)
        extract(firmware["path"], firmware["data"], i, config)

    return ret
