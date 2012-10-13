#!/usr/bin/env python
# encoding: utf-8

""" mkpng.py

Convert a file to png and optimize it.
Requires imagemagick and optipng.

Usage:
    mkpng.py [-h] [-l LEVEL] FILE

Options:
    -h, --help         Show help
    -l LEVEL, --level  Optimization level (1-7) [default: 2]

"""

from docopt import docopt
from os import path, extsep
from sh import optipng, convert
import sys

def main(args):
    path_input_file, level = args["FILE"], args["--level"]
    path_tmp_png = path.splitext(path_input_file)[0] + ".png"

    if path.exists(path_input_file):
        if not path.splitext(path_input_file)[-1][1:] == "png":
            convert(path_input_file, path_tmp_png)
            print("Converting file to png...")

        print("Crushing png...")
        optipng("-o" + level, path_tmp_png)
        print("Done!")
        sys.exit()
    else:
        print("That file doesn't exist!")
        sys.exit()


if __name__ == '__main__':
    try:
        main(docopt(__doc__))
    except KeyboardInterrupt:
        sys.exit()
