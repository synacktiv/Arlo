from bip import *
#import idautils, ida_bytes

def curl_find():
    setopt = BipFunction.get_by_name('curl_easy_setopt')
    for call in setopt.xCodeTo:
        func = call.func
        hxf = func.hxcfunc
        for cn in hxf.get_cnode_filter_type(CNodeExprCall):
            caller = cn.caller.ignore_cast
            if not isinstance(caller, CNodeExprObj):
                continue # indirect call or something
            try:
                if GetElt(caller.value).name == setopt.name:
                    val = cn.ignore_cast.get_arg(1).ignore_cast
                    if val == 64:
                        print(f'found noverify 0x{caller.ea:08x} {val}')
                    elif val == 10065:
                        print(f'found capath 0x{caller.ea:08x} {val}')
                    elif val == 10029:
                        print(f'found headerdata 0x{caller.ea:08x} {val}')

            except ValueError:
                continue # ignore this

def set_name(cn, fname):
    try:
        cn.name = fname
        print(f"0x{cn.ea:08x}: renamed {fname}")
    except base.biperror.BipError:
        print(f"0x{cn.ea:08x}: can't rename {fname}")

def find_name(func, name, fmt_idx, fmt_match, name_idx):
    s = set()
    ea = 0
    hxf = func.hxcfunc
    for cn in hxf.get_cnode_filter_type(CNodeExprCall):
        ea = cn.ea
        caller = cn.caller.ignore_cast
        if not isinstance(caller, CNodeExprObj):
            if not isinstance(caller, CNodeExprHelper):
                if not isinstance(caller, (CNodeExprPtr, CNodeExprVar,
                                           CNodeExprRef, CNodeExprIdx,
                                           CNodeExprMemptr)):
                    print(f'[!] 0x{cn.ea:08x} {caller}')
            continue

        if GetElt(caller.value).name == name:
            try:
                if fmt_idx is not None:
                    arg = cn.get_arg(fmt_idx).ignore_cast
                    if isinstance(arg, (CNodeExprPtr, CNodeExprVar,
                                        CNodeExprRef, CNodeExprIdx)):
                        continue
                    if BipData.get_cstring(arg.value) is None:
                        print(f'[!] 0x{cn.ea:08x} {arg}')
                        continue
                    fmt = BipData.get_cstring(arg.value).decode()

                if fmt_idx is None or fmt.startswith(fmt_match):
                    #print(f'[!] 0x{cn.ea:08x} {fmt}')
                    arg = cn.get_arg(name_idx).ignore_cast
                    if isinstance(arg, (CNodeExprPtr, CNodeExprVar,
                                        CNodeExprRef, CNodeExprIdx)):
                        continue
                    fname = BipData.get_cstring(arg.value).decode()
                    s.add(fname)
                    #print(f'0x{cn.ea:08x} {fmt} {fname}')
                #else:
                #    print(f'[-] 0x{cn.ea:08x} {fmt}')
            except Exception as e:
                print(f'0x{ea:08x} {e}')

    if len(s) == 1:
        set_name(func, fname)
    elif len(s) == 0:
        pass
    else:
        print(f'[?] 0x{ea:08x} {s}')

known = {
        "logf": [
            { "fi": 1, "fm": "[%s]", "ni": 2, },
            { "fi": 1, "fm": "[LVS2]:%s", "ni": 2, },
            { "fi": 1, "fm": "[META]:%s", "ni": 2, },
            { "fi": 1, "fm": "[PB]:%s", "ni": 2, },
            { "fi": 1, "fm": "%s:", "ni": 2, },
            { "fi": 1, "fm": "%s()", "ni": 2, },
            { "fi": 1, "fm": "%s", "ni": 2, },
        ],
        "logf0": [
            { "fi": 1, "fm": "%s:", "ni": 2, },
            { "fi": 1, "fm": "%s()", "ni": 2, },
            { "fi": 1, "fm": "%s", "ni": 2, },
        ],
        "cim_read0": [
            { "fi": None, "fm": None, "ni": 1, },
        ],
        "cim_read1": [
            { "fi": None, "fm": None, "ni": 1, },
        ],
        "cim_write0": [
            { "fi": None, "fm": None, "ni": 1, },
        ],
        "cim_set_bool": [
            { "fi": None, "fm": None, "ni": 1, }
        ],
        "cim_dup_string": [
            { "fi": None, "fm": None, "ni": 1, },
        ],
        "cimd_read": [
            { "fi": None, "fm": None, "ni": 1, },
        ],
        "cimd_write": [
            { "fi": None, "fm": None, "ni": 1, },
        ],
        "automation_logf": [
            { "fi": 1, "fm": "automation:%s:%s()", "ni": 3,},
        ],
        "agw_logf": [
            { "fi": 1, "fm": "agw:%s:%s()", "ni": 3, },
        ],
        #"printf": [{ "fi": 0, "fm": None, "ni": 1, },],
        #"printf_0": [{ "fi": 0, "fm": None, "ni": 1, },],
}

def rename_known():
    for fname in known:
        f = BipFunction.get_by_name(fname)
        if f is None:
            continue
        for call in f.xCodeTo:
            try:
                func = call.func
                if not func.is_ida_name:
                    continue
                for data in known[fname]:
                    find_name(func, f.name, data["fi"], data["fm"], data["ni"])
            except ValueError as e:
                print(e)
                continue
            except BipDecompileError as e:
                print(e)
                continue

rename_known()
