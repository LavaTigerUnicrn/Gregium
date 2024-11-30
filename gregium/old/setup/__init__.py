"""
Tools for setting up a new python project
"""
import gregium

def new(directory:str,name:str):

    """
    Make a new python file compatible with gregium at {direcory}\\{name}.py
    """

    # Copy exampleFile to new directory
    with open(gregium.PATH+"/setup/exampleFile.py","r") as example:

        with open(f"{directory}\\{name}.py","w") as newPy:
            newPy.write(example.read())
