"""Main entry point for conda-pytorch"""
from argparse import ArgumentParser


def make_parser():
    p = ArgumentParser("conda-pytorch")
    cmd = p.add_subparsers("cmd", help="subcommand to execute")
    dev = cmd.add_parser("dev", help="develop tool for pytorch")
    return p


def dev(ns):
    from . import develop

    develop.install()


def main(args=None):
    p = make_parser()
    ns = p.parse_args(args)
    if ns.cmd == "dev":
        dev(ns)


if __name__ == "__main__":
    main()