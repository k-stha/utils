#!/usr/bin/env python3

"""Automatically format Python 3 scripts."""

import argparse
import sys
from os.path import isdir, isfile
from subprocess import run


def error(message: str) -> None:
    """Print error message and send it to stderr."""
    try:
        print(message, file=sys.stderr)
    except IOError:
        pass


def get_args(argv: list[str]) -> argparse.Namespace:
    """Parse arguments and return them."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument(
        "input_file",
        type=str,
        action="extend",
        nargs="+"
        help="Input file(s) to format",
    )

    return parser.parse_intermixed_args(argv)


def check_path(path_list: list[str]) -> None:
    """Check if all the given paths are files and/or directories."""
    error_count = 0

    for path in path_list:
        if not (isfile(path) or isdir(path)):
            error("The path is not a file or a directory: " + path)
            error_count += 1

    if error_count > 0:
        sys.exit(1)


def return_isort_args(files: list[str]) -> list[str]:
    """Return isort arguments as list."""
    isort_exec = "isort"

    isort_args = [
        isort_exec,
        "-n",
        "-l",
        "88",
        "--wl",
        "88",
        "-m",
        "3",
        "--tc",
        "--fgw",
        "0",
        "--up",
        "--remove-redundant-aliases",
    ] + files

    return isort_args


def return_black_args(files: list[str]) -> list[str]:
    """Return black arguments as list."""
    black_exec = "black"

    black_args = [black_exec, "-q"] + files

    return black_args


def main(argv: list[str]) -> None:
    """Function to be called."""
    args: argparse.Namespace = get_args(argv)

    if args.input_file:
        files = args.input_file

    check_path(files)

    run(return_isort_args(files), check=True)
    run(return_black_args(files), check=True)


if __name__ == "__main__":
    main(sys.argv[1:])
