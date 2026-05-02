#!/usr/bin/env python3

import os
import sys
import json
import hashlib
import mimetypes
from datetime import datetime

B = "\033[94m"
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
N = "\033[0m"


def banner():
    print(f"""{B}
███╗   ███╗███████╗████████╗ █████╗ ██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗
████╗ ████║██╔════╝╚══██╔══╝██╔══██╗╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
██╔████╔██║█████╗     ██║   ███████║ ╚███╔╝    ██║   ██████╔╝███████║██║        ██║
██║╚██╔╝██║██╔══╝     ██║   ██╔══██║ ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║
██║ ╚═╝ ██║███████╗   ██║   ██║  ██║██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║
╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝
{N}""")


def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def md5sum(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_strings(path):
    strings = []
    try:
        with open(path, "rb") as f:
            data = f.read()
            current = b""
            for b in data:
                if 32 <= b <= 126:
                    current += bytes([b])
                else:
                    if len(current) >= 6:
                        strings.append(current.decode(errors="ignore"))
                    current = b""
    except:
        pass
    return strings[:30]


def get_metadata(path):
    if not os.path.exists(path):
        print(f"{R}[!] File not found{N}")
        sys.exit(1)

    stat = os.stat(path)

    meta = {
        "file_name": os.path.basename(path),
        "full_path": os.path.abspath(path),
        "size_bytes": stat.st_size,
        "mime_type": mimetypes.guess_type(path)[0],
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "md5": md5sum(path),
        "sha256": sha256sum(path),
        "readable": os.access(path, os.R_OK),
        "writable": os.access(path, os.W_OK),
        "hidden_strings": extract_strings(path)
    }

    return meta


def main():
    banner()

    if len(sys.argv) != 2:
        print(f"{Y}Usage:{N} metaxtract <file>")
        sys.exit(1)

    target = sys.argv[1]
    data = get_metadata(target)

    print(f"{G}[+] Metadata Extracted:{N}\n")
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
