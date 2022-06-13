#!/usr/bin/env python3

"""Automatically format Python 3 scripts."""

import argparse
import sys
from os.path import isdir, isfile
from subprocess import run


def error(message: str) -> None:
    """Print error message and send it to stderr."""
    print(message, file=sys.stderr)


def get_args(argv: list[str]) -> argparse.Namespace:
    """Parse arguments and return them."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser()

    parser.add_argument(
        "input_path",
        type=str,
        action="extend",
        nargs="+",
        help="Input path(s) to format",
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


def return_isort_args(paths: list[str]) -> list[str]:
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
    ] + paths

    return isort_args


def return_black_args(paths: list[str]) -> list[str]:
    """Return black arguments as list."""
    black_exec = "black"

    black_args = [black_exec, "-q"] + paths

    return black_args


def run_formatters(paths: list[str]) -> None:
    """"""
    check_path(paths)

    run(return_isort_args(paths), check=True)
    run(return_black_args(paths), check=True)


def main(argv: list[str]) -> None:
    """Function to be called."""
    args: argparse.Namespace = get_args(argv)

    if args.input_path:
        paths: list[str] = args.input_path

    run_formatters(paths)


if __name__ == "__main__":
    main(sys.argv[1:])
