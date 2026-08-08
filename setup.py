import os
from pathlib import Path

from setuptools import setup

import gregium

pkgdata = {}

def prune(pkg: list, extension: str):
    rm = pkg.copy()

    for i, item in enumerate(pkg):
        if "." in item:
            if Path(item).suffix != ".py" and Path(item).suffix != ".pyc":
                if extension.replace("/", ".")[:-1] not in pkgdata:
                    pkgdata[extension.replace("/", ".")[:-1]] = []

                try:
                    if (
                        "*" + Path(item).suffix
                        not in pkgdata[extension.replace("/", ".")[:-1]]
                    ):
                        pkgdata[extension.replace("/", ".")[:-1]].append(
                            "*" + Path(item).suffix
                        )
                except Exception:
                    ...

            rm.remove(item)

    for i, item in enumerate(rm):
        rm[i] = extension + rm[i]

    return rm


tree = prune(os.listdir("./gregium"), "gregium/")

pkgs = ["gregium"]

while len(tree) > 0:
    tree_list = os.listdir(tree[0])
    if "__init__.py" in tree_list or any(".py" in x for x in tree_list):
        pkgs.append(tree[0].replace("/", "."))

    tree = tree + prune(os.listdir(tree[0]), tree[0] + "/")

    tree.pop(0)

with open("README.md", "r", encoding="utf-8") as r:
    longdesc = r.read()

ver = (
    gregium.VERSION
)
print(f"Gregium {ver}:\nPackages Found:{pkgs}\nPackage Data Found:{pkgdata}\n\n\n")

setup(
    name="gregium",
    version=ver,
    description="A package full of prebuilt modules for various common functions",
    long_description=longdesc,
    author="LavaTigerUnicrn",
    author_email="lavatigerunicrn@gmail.com",
    url="https://github.com/LavaTigerUnicrn/Gregium",
    packages=pkgs,
    package_data=pkgdata,
    install_requires=["pillow","requests","dotenv","pygame-ce"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    long_description_content_type="text/markdown",
    project_urls={
        "github": "https://github.com/LavaTigerUnicrn/Gregium",
        "issues": "https://github.com/LavaTigerUnicrn/Gregium/issues",
    },
)