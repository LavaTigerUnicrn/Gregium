from setuptools import setup
import sys,os
from pathlib import Path
sys.dont_write_bytecode = True 

import gregium

pkgdata = {}

def prune(l:list,extension:str):

    rm = l.copy()

    for i,item in enumerate(l):
        
        if "." in item:

            if Path(item).suffix != ".py":
                if not extension.replace("/",".")[:-1] in pkgdata:

                    pkgdata[extension.replace("/",".")[:-1]] = []

                try:
                    if not "*" + Path(item).suffix in pkgdata[extension.replace("/",".")[:-1]]:

                        pkgdata[extension.replace("/",".")[:-1]].append("*" + Path(item).suffix)
                except:...

            rm.remove(item)

    for i,item in enumerate(rm):

        rm[i] = extension+rm[i]

    return rm

tree = prune(os.listdir("./gregium"),"gregium/")

pkgs = ["gregium"]

while len(tree) > 0:

    if "__init__.py" in os.listdir(tree[0]):

        pkgs.append(tree[0].replace("/","."))

    tree = tree + prune(os.listdir(tree[0]),tree[0]+"/")

    tree.pop(0)

with open("README.md","r",encoding="utf-8") as r:
    longdesc = r.read()

ver = f"{gregium.VERSION["major"]}.{gregium.VERSION["minor"]}.{gregium.VERSION["patch"]}"
print(f"Gregium V{ver}:\nPackages Found:{pkgs}\nPackage Data Found:{pkgdata}\n\n\n")

setup(name="gregium",version=ver,
                 description="A simple package with easy features for using pygame",
                 long_description=longdesc,
                 author="LavaTigerUnicrn",
                 author_email="nolanlance711@gmail.com",
                 url="https://github.com/LavaTigerUnicrn/Gregium",
                 packages=pkgs,
                 package_data=pkgdata,
                install_requires=
                ["pygame-ce","pynput","pyglet","colorama"],
                classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3'],
    long_description_content_type="text/markdown",
    project_urls={
        "github":"https://github.com/LavaTigerUnicrn/Gregium",
        "issues":"https://github.com/LavaTigerUnicrn/Gregium/issues"
    }
    )