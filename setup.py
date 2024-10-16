from setuptools import setup

with open("README.md","r",encoding="utf-8") as r:
    longdesc = r.read()
setup(name="gregium",version="0.1.6",
                 description="A simple package with easy features for using pygame",
                 long_description=longdesc,
                 author="LavaTigerUnicrn",
                 author_email="nolanlance711@gmail.com",
                 url="https://github.com/LavaTigerUnicrn/Gregium",
                 download_url="https://github.com/LavaTigerUnicrn/Gregium/archive/refs/tags/v0.1.6.tar.gz",
                 packages=["gregium","gregium.env","gregium.editor"],
                 package_data={"gregium.editor": ["*.grg","*.ttf"], "gregium": ["*png"]},
                install_requires=
                ["pygame-ce","pynput"],
                classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3'],
    long_description_content_type="text/markdown"
    )