""" download_images module

Defines download_images function

"""

from collections.abc import Iterable

from garfield_downloader.file_util.create_dir import create_dir
from garfield_downloader.downloader.download_image import download_image
from garfield_downloader.downloader.get_comic_dir import get_comic_dir


def __tmp2(__tmp1, __tmp0: <FILL>) -> None:
    """
    Function to download all data from provided links
    :param loc: str
    :param links: Iterator
    :return: None
    """
    for src in __tmp0:
        save_dir = get_comic_dir(src)
        create_dir(f"{__tmp1}/{'/'.join(save_dir.split('/')[:2])}")
        download_image(f"{__tmp1}/{save_dir}", src)
