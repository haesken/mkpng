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
from schema import Schema, And, Or, Use, Optional, SchemaError
from os import path, extsep
from sh import optipng, convert

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
        exit(0)


if __name__ == '__main__':
    try:
        args = docopt(__doc__)

        schema = Schema({
            "FILE": Use(open, error="That file doesn't exist!"),
            "--level": Or(None,
                          And(Use(int), lambda n: 1 < n < 7),
                          error="LEVEL should be between 1 and 7"),
            Optional("--help"): Or(True, False),
            })

        try:
            schema.validate(args)
        except SchemaError as e:
            exit(e)

        main(args)
    except KeyboardInterrupt:
        exit(0)
