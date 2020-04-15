import os
import json
import random
import string
from pathlib import Path

import numpy
from PIL import Image
from PIL.ImageFile import ImageFile

import subprocess
import shlex

from werkzeug.utils import secure_filename

from configuration import MyShopConfig

def url(filename, subdir: str) -> str:
    """Get url file

    Args:
        filename: filename
        subdir: subdirectory

    Returns:
        str url
    """
    if not filename:
        return ""

    static_url = MyShopConfig.STATIC_URL
    if subdir:
        static_url = static_url + "/" + subdir

    return static_url + "/" + filename


def save(file, subdir: str, filename: str = None, close_after=True) -> str:
    """Save file

    Args:
        file: save able file ex: (FileStorage, ImageFile)
        subdir: sub directory
        filename: filename of file
        close_after: Close file after done ?
    
    Return:
        str filename
    """
    upload_dir = Path(MyShopConfig.STORAGE_PATH)
    if subdir:
        upload_dir = upload_dir / subdir

    # make sure upload directory exists
    if not upload_dir.is_dir():
        upload_dir.mkdir(parents=True)

    # make sure filename is safe and no collision
    filename = safe_filename(filename)
    while (upload_dir / filename).is_file():
        filename = safe_filename(file.filename)

    if isinstance(file, Image.Image):
        if file.mode in ("RGBA", "LA", "1", "P"):
            file = file.convert("RGB")

        size = (984, 1312)
        if file.size[0] > size[0] or file.size[1] > size[1]:
            file.thumbnail(size, Image.ANTIALIAS)
            file.save(str(upload_dir / filename), quality=90)
        else:
            file.save(str(upload_dir / filename), quality=90)

    if close_after:
        file.close()

    return filename


def safe_filename(filename, maxchar=40):
    """Secure filename and add random string

    Args:
        filename: filename
        maxchar: maximum character

    Example: Result:
    [name_file]_randomgstring - inifilecermin_awkwardscz.jpg
    """
    name, ext = os.path.splitext(filename)

    random_str = "_" + ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(10)
    )

    name_max = maxchar - len(ext) - len(random_str)
    if len(name) > name_max:
        name = name[:name_max]

    name = "%s%s%s" % (name, random_str, ext)

    return secure_filename(name)