from setuptools import setup
setup(name="gregium",version="0.1.3",
                 description="A simple package with easy features for using pygame",
                 author="LavaTigerUnicrn",
                 author_email="nolanlance711@gmail.com",
                 url="https://github.com/LavaTigerUnicrn/Gregium",
                 download_url="https://github.com/LavaTigerUnicrn/Gregium/archive/refs/tags/v0.1.3.tar.gz",
                 packages=["gregium","gregium.env","gregium.editor"],
                 package_data={"gregium/editor": ["*.grg"], "gregium/editor/Space_Mono": ["*ttf"]},
                install_requires=
                ["pygame-ce","pynput"],
                classifiers=[
    'Development Status :: 3 - Alpha',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',]
    )