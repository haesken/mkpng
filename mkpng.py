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
from os import path, remove
from sh import optipng, convert


def validate_args(args):
    """ Validate arguments. """
    schema = Schema({
        "FILE": Use(open,
                    error="FILE doesn't exist or isn't readable!"),

        "--level": Or(None,
                        And(Use(int), lambda n: 1 <= n <= 7),
                        error="LEVEL should be between 1 and 7"),

        Optional("--help"): Or(True, False),
        })

    try:
        # Don't return the validated args here, just make sure they are valid.
        # Schema will return an object containing an open file object,
        # when we just wanted to make sure the file was readable.
        schema.validate(args)
        return args

    except SchemaError as e:
        exit(e)


def main(args):
    """ Convert an image to png if needed, then optimize it. """

    path_input_file, level = args["FILE"], args["--level"]
    path_tmp_png = path.splitext(path_input_file)[0] + ".png"
    input_file_ext = path.splitext(path_input_file)[-1][1:]

    if path.exists(path_input_file):
        if not input_file_ext == "png":
            if input_file_ext in ["bmp", "tiff", "raw"]:
                print("Converting file to png...")

                if path.exists(path_tmp_png):
                    remove(path_tmp_png)

                convert(path_input_file, path_tmp_png)
            else:
                print("Image is in a lossy format, aborting!")

        print("Optimizing png...")
        # Will overwrite path_tmp_png with its output.
        optipng("-o" + level, path_tmp_png)
        print("Done!")

        print("Output file at {out_path}".format(
            out_path=path.abspath(path_tmp_png)))

        exit(0)


if __name__ == '__main__':
    try:
        main(validate_args(docopt(__doc__)))
    except KeyboardInterrupt:
        exit(0)
