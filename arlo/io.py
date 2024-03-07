#!/usr/bin/python
"""
Arlo firmware extractor
I/O (network & disk)
"""

import os

from struct import unpack, error
from urllib.parse import urlparse
from requests import get
from requests.exceptions import JSONDecodeError, Timeout

from .data import Arlo

def wget(url, timeout=10):
    """ requests get wrapper """
    headers = {"User-Agent": "curl/7.88.1",
               "Cache-Control": "no-cache",
               "ETag": "deadbeef", }
    return get(url=url, headers=headers, timeout=timeout)

def _parse_json(json):
    """ extract information from downloaded JSON """
    lst = {}
    for entry in json["models"]:
        #if not "modelId in entry:
        #    raise ValueError(f"missing modelId in entry")
        if "defaultPath" not in entry:
            raise ValueError("missing defaultPath in entry")
        for path in entry["defaultPath"]:
            if "md5sum" not in path:
                key  = entry["modelId"] + "_" + entry["version"]
            else:
                key  = path["md5sum"]
            lst[key] =  {"file": path["file"], "version": entry["version"],}

    return lst

def do_download(model):
    """ download update for model """
    url = Arlo.json_url(model)
    try:
        resp = wget(url)
    except Timeout:
        print(f"    - {url} time out")
        return None

    if not resp.ok:
        print(f"    - {url} HTTP {resp.status_code}")
        return None
    try:
        if resp.content == b"":
            print(f"    - {url} HTTP empty")
            return None
        json = resp.json()
    except JSONDecodeError:
        return None

    lst = _parse_json(json)

    ret = []
    for _, info in lst.items():
        url   = Arlo.base_url() + info["file"]
        finfo = urlparse(url)
        try:
            resp  = wget(url)
        except Timeout:
            print(f"    - {url} time out")
            return None

        if not resp.ok:
            print(f"    - {url} HTTP {resp.status_code}")
        else:
            ret.append({
                "version": info["version"],
                "path": finfo.path,
                "data": resp.content,
            })

    return ret

def write(path, fname, binary):
    """ write binary to path """
    os.makedirs(path, mode=0o755, exist_ok=True)
    with open(f"{path}/{fname}", "wb") as file:
        file.write(binary)
    return f"{path}/{fname}"

def append(path, fname, text):
    """ append text to file in path """
    os.makedirs(path, mode=0o755, exist_ok=True)
    with open(f"{path}/{fname}", "a", encoding="utf-8") as file:
        file.write(text)

def get_fname(url):
    """ get fname from url """
    return os.path.basename(url)

def get_path(class_type, model, prefix, version):
    """ build path string """
    return f"{prefix}/{class_type}/{model}/{version}"

def download(class_type, model, prefix, save=False):
    """ download update for model and eventually write it to disk """
    ret = []
    infos = do_download(model)
    if infos is None:
        return None

    for info in infos:
        path  = get_path(class_type, model, prefix, info["version"])
        fname = get_fname(info["path"])
        if save:
            write(path, fname, info["data"])
        ret.append({
            "path":  path,
            "fname": fname,
            "data":  info["data"],
        })

    return ret

def peek_magic(stream):
    """ peek magic in stream """
    if stream is None:
        return None

    magic = None
    try:
        magic = unpack("<4s", stream.read(4))[0]
        stream.seek(-4, 1)
    except error:
        print(" (error peeking magic) ", end="")

    return magic
