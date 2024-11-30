from setuptools import setup
import gregium

with open("README.md","r",encoding="utf-8") as r:
    longdesc = r.read()
setup(name="gregium",version=f"{gregium.VERSION["major"]}.{gregium.VERSION["minor"]}.{gregium.VERSION["patch"]}",
                 description="A simple package with easy features for using pygame",
                 long_description=longdesc,
                 author="LavaTigerUnicrn",
                 author_email="nolanlance711@gmail.com",
                 url="https://github.com/LavaTigerUnicrn/Gregium",
                 packages=["gregium","gregium.buttons","gregium.camera","gregium.commandSystem","gregium.gamblecore","gregium.env","gregium.terminalLogging","gregium.old","gregium.old.env","gregium.old.editor","gregium.old.gv","gregium.old.setup","gregium.old.env"],
                 package_data={"gregium.old.editor": ["*.grg","*.ttf"], "gregium.old": ["*png"]},
                install_requires=
                ["pygame-ce","pynput"],
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