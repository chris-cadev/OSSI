import os
import json
import urllib.request


def wait():
    input("Press Enter to continue...")


def save_file(content: str, filename: str) -> str:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)
    return filename


def save_object(object, filename: str) -> str:
    content = json.dumps(object)
    return save_file(content, filename)


def save_url_picture(url: str, filename: str) -> str:
    urllib.request.urlretrieve(url, filename)
    return filename
