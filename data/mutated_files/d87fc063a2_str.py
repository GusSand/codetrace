from typing import TypeAlias
__typ0 : TypeAlias = "Iterable"
""" download_images module

Defines download_images function

"""

from collections.abc import Iterable

from garfield_downloader.file_util.create_dir import create_dir
from garfield_downloader.downloader.download_image import download_image
from garfield_downloader.downloader.get_comic_dir import get_comic_dir


def download_images(__tmp0: <FILL>, links) :
    """
    Function to download all data from provided links
    :param loc: str
    :param links: Iterator
    :return: None
    """
    for src in links:
        save_dir = get_comic_dir(src)
        create_dir(f"{__tmp0}/{'/'.join(save_dir.split('/')[:2])}")
        download_image(f"{__tmp0}/{save_dir}", src)
