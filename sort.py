import argparse
import logging
import re

from pathlib import Path
from shutil import copyfile
from threading import Thread
from typing import Any

"""
  Commands   |                 Description
===========================================================
 --source -s | 
             | it is required.
 --output -0 | the path of the output folder.
             | It is optional. default value "dist".
===========================================================
"""

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument(
    '--source', '-s', metavar='', help='The path of the source folder. it is required.', required=True)
parser.add_argument(
    '--output', '-o', metavar='', help='The path of the output folder. It is optional. Default value "dist".', default='dist')

args = vars(parser.parse_args())

source = args.get('source')
output = args.get('output')

folders = []


def grab_folders(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grab_folders(el)


def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as err:
                logging.error(err)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR,
                        format="%(treadName)s %(message)s")
    base_folder = Path(source)
    output_folder = Path(output)
    folders.append(base_folder)
    grab_folders(base_folder)

    threads = []

    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print("Now you may delete the old folders!")
