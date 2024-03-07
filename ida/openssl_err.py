import re
from glob import glob
from os.path import isfile

def _define_to_dict(lines, regexp):
    ret = {}

    r = re.compile(regexp)
    for line in lines:
        m = r.match(line)
        if m is not None:
            g = m.groups()
            ret[int(g[1])] = g[0].lower()

    return ret

def get_libs(path):
    lines = ()

    with open(path, 'r') as f:
        lines = list(f)

    return _define_to_dict(lines, r'#\s*define\s+ERR_LIB_(\w+)\s+(\d+)')

def get_funcs(libname):
    lines = ()

    for path in glob(f'{libname}*err.h'):
        with open(path, 'r') as f:
            lines = lines + tuple(list(f))

    return _define_to_dict(lines, f'#\s*define\s+{libname.upper()}_F_(\w+)\s+(\d+)')

def main():
    info = {}

    libs = get_libs('err.h')
    for i in libs:
        funcs = get_funcs(libs[i])
        if len(funcs) > 0:
            info[i] = funcs
        else:
            print(f'{libs[i]} err not found')
            info[i] = {}

    print(info)

if __name__ == '__main__':
    main()
