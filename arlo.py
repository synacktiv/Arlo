#!/usr/bin/python
import argparse

from arlo.parser import update_one, update_all, extract
from arlo.data import Arlo

def update(args):
    """ update all or specific model """
    if args.model is not None:
        key, model = Arlo.find_model(args.model)
        if key is None or model is None:
            print("invalid model")
            return
        update_one(args.prefix, key, model, Arlo.model(key, model))
        print()
    else:
        update_all(args.prefix)

def parse(args):
    """ parse dump file """
    config = None
    if args.model is not None:
        key, model = Arlo.find_model(args.model)
        if key is None or model is None:
            print("invalid model")
            return
        config = Arlo.model(key, model)

    extract(args.prefix, args.dumpfile[0].read(), 0, config)

def list(args):
    """ list known models """
    for key in Arlo.device_types():
        print(f"- {key}")
        for cid, name in Arlo.list_models(key):
            print(f"  - {cid:8s}: {name}")

def main():
    """ parse arguments and run """
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", dest="prefix", nargs="?", type=str, default="./",
                        help="folder where files will be written")
    choices = []
    for key in Arlo.device_types():
        choices += Arlo.models[key].keys()
    parser.add_argument("-m", dest="model", nargs="?", default=None,
                        choices=choices, help="Treat file as this model dump."+
                                              " See list command")

    subparsers = parser.add_subparsers(title="commands", required=True,
                                       description="valid commands",
                                       help="commands specific help")
    update_parser = subparsers.add_parser("update", help="update help")
    update_parser.set_defaults(func=update)

    parse_parser = subparsers.add_parser("parse", help="parse help")
    parse_parser.add_argument("dumpfile", nargs=1, type=argparse.FileType('rb'),
                              help="FLASH dump file")
    parse_parser.set_defaults(func=parse)

    list_parser = subparsers.add_parser("list", help="list help")
    list_parser.set_defaults(func=list)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
