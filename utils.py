import os
import json
import urllib.request


def wait(message: str = None):
    input("Press Enter to continue..." if message is None else message)


def create_directories(filename: str):
    os.makedirs(os.path.dirname(
        os.path.abspath(filename)
    ), exist_ok=True)


def save_file(content: str, filename: str) -> str:
    create_directories(filename)
    with open(filename, "w") as f:
        f.write(f'{content}')
    return filename


def save_object(object, filename: str) -> str:
    content = json.dumps(object)
    return save_file(content, filename)


def save_url_picture(url: str, filename: str) -> str:
    create_directories(filename)
    urllib.request.urlretrieve(url, filename)
    return filename
