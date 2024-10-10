from setuptools import setup
setup(name="gregium",version="0.1",
                 description="A simple package with easy features for using pygame",
                 author="LavaTigerUnicrn",
                 author_email="nolanlance711@gmail.com",
                 url="https://github.com/LavaTigerUnicrn/Gregium",
                 packages=["gregium","gregium.env","gregium.editor"],
                 package_dir={"": "gregium"},
                 package_data={"gregium/editor": ["*.grg"], "gregium/editor/Space_Mono": ["*ttf"]},
                install_requires=
                ["pygame"])