"""
A simple module for loading an saving .grg (ENV) files
Call gregenv.load() first and then env data is stored in gregenv.ENV as a dict
"""

# Importing necessary libraries
import os
import json
import warnings
from pathlib import Path

# Set up the ENV variable for storing .grg file data
ENV = {"ENV NOT INITIALIZED":None}

def parseEnv(parse:str):
    """
    MODULE FUNCTION (DO NOT RUN)
    """
    parseDict = {}

    # Loop through the input to be parsed
    for n, l in enumerate(parse.split("\n")):

        # Skip the current iteration if it is empty
        if len(l) == 0:
            continue
            
        # Initialize function variables
        varNComp = ""
        valNComp = ""
        compMode = "var"
        skip = False
        foundSpace = 0
        lSpace = False
        hasWarned = False

        # Loop through each character of each section of the input
        for ltr in l:

            # Skip the current line if a comment is present
            if ltr == "#":
                skip = True
                break

            # Checks if the current line represents a variable assignment
            if compMode == "var":
                if ltr == "=":
                    compMode = "val"

                    # If there are spaces in the variable, warn the user
                    if not lSpace and foundSpace > 0 and not hasWarned:
                        hasWarned = True
                        warnings.warn(f"Many spaces found in variable of line {n+1}, variable names will have spaces removed")
                    
                    # Informs the user that the variable name was changed
                    if hasWarned:
                        print(f"Var name converted to: {varNComp}")
                    continue
                
                lSpace = False

                # If a space is not detected, add the character to the name of the variable
                if ltr != " ":
                    varNComp += ltr

                # If spaces are detected, warn the user
                else:
                    foundSpace += 1
                    lSpace = True
                if foundSpace > 1 and not hasWarned:
                    hasWarned = True
                    warnings.warn(f"Many spaces found in variable of line {n+1}, variable names will have spaces removed")
            else:
                # If the variable assignment reaches the right side of the
                # equation, add the current character to the variable value
                valNComp += ltr

        # Skip the current line if needed  
        if skip:
            continue
        
        # If an = is missing in a variable assignment, throw an error
        if compMode == "var":
            raise Exception(f"Expected '=' in line {n+1}")
        
        # Convert the variable and value into a python object
        val = json.loads(valNComp)
        parseDict[varNComp] = val
        
    return parseDict

def reparseEnv(parse:dict):
    """
    MODULE FUNCTION (DO NOT RUN)
    """
    parsed = ""

    # Stringify the given python object, converting it to what would be its form before parsing
    for key in parse:
        parsed += f"{key}={json.dumps(parse[key])}\n"
    return parsed[:-1]
    
def load(fileName:str=None,loadAllEnv:bool=False,ignoreCWD:bool=False):
    """
    Loads ENV from .grg file using a path
    """
    global ENV
    ENV = {}
    
    if fileName != None:

        # Set global variable ENV to the parsed data in the file specified by only the path given
        if ignoreCWD:
            with open(fileName,"r") as env:
                ENV = parseEnv(env.read())

        # Set global variable ENV to the parsed data in the file specified by the
        # current working directory plus the path given
        else:
            with open(os.getcwd()+"/"+fileName,"r") as env:
                ENV = parseEnv(env.read())
    
    # If a file path is not given, try to find a .grg in the current working directory
    else:
        posEnv = []
        for env in os.listdir(os.getcwd()):
            if ".grg" in env:
                posEnv.append(env)
                
        # Raise an error if no .grg file is found in the current working directory
        if len(posEnv) == 0:
            raise ValueError(".grg file not found, add (fileName) parameter to continue")
        
        # Raise an error if many .grg files are found in the current working directory
        # and the user does not specify that they want multiple files loaded
        elif len(posEnv) > 1 and not loadAllEnv:
            raise ValueError("multiple .grg files found, add (fileName) parameter to continue or set (loadAllEnv) to True")
        
        # If the user wishes to load multiple .grg files, 
        # load all of the .grg files in the current working directory
        elif loadAllEnv:
            for envN in posEnv:
                with open(os.getcwd()+"/"+envN,"r") as env:
                    envA = parseEnv(env.read())
                    for envK in envA:
                        ENV[envK] = envA[envK]

        # If there is only one .grg file in the current working directory,
        # set ENV to its parsed contents
        else:
            with open(os.getcwd()+"/"+posEnv[0],"r") as env:
                ENV = parseEnv(env.read())
                
def save(fileName:str=None):
    """
    Saves ENV to file parent file
    """
    
    # Throw an error if ENV is in its default value (i.e. nothing is in ENV)
    if "ENV NOT INITIALIZED" in ENV:
        raise Exception("ENV NOT INITIALIZED")
    
    # If a valid file name is given, write a serialized version of ENV in that file
    # NOALN ?????????? moment i think error handling moment, what if user sends invalid file?
    if fileName != None:
        with open(os.getcwd()+"/"+fileName,"w") as env:
            env.write(reparseEnv(ENV))

    # If no file is given, look for .grg files in the current working directory
    else:
        posEnv = []
        for env in os.listdir(os.getcwd()):
            if ".grg" in env:
                posEnv.append(env)
                
        # Raise en error if no .grg file is present
        if len(posEnv) == 0:
            raise ValueError(".grg file not found, add (fileName) parameter to continue")
        
        # Raise en error if many .grg files are present
        elif len(posEnv) > 1:
            raise ValueError("multiple .grg files found, add (fileName) parameter to continue")
        
        # If there is only one .grg file in the current working directory,
        # write a serialized version of ENV in that file
        else:
            with open(os.getcwd()+"/"+posEnv[0],"w") as env:
                env.write(reparseEnv(ENV))