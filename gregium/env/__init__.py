"""
A simple module for loading an saving .grg (ENV) files
Call gregenv.load() first and then env data is stored in gregenv.ENV as a dict
"""

import os
import json
import warnings
from pathlib import Path

ENV = {"ENV NOT INITIALIZED":None}
    
def parseEnv(parse:str):
    """
    MODULE FUNCTION (DO NOT RUN)
    """
    parseDict = {}
    for n, l in enumerate(parse.split("\n")):
        if len(l) == 0:
            continue
        varNComp = ""
        valNComp = ""
        compMode = "var"
        skip = False
        foundSpace = 0
        lSpace = False
        hasWarned = False
        for ltr in l:
            if ltr == "#":
                skip = True
                break
            if compMode == "var":
                if ltr == "=":
                    compMode = "val"
                    if not lSpace and foundSpace > 0 and not hasWarned:
                        hasWarned = True
                        warnings.warn(f"Many spaces found in variable of line {n+1}, variable names will have spaces removed")
                    
                    if hasWarned:
                        print(f"Var name converted to: {varNComp}")
                    continue
                
                lSpace = False
                if ltr != " ":
                    varNComp += ltr
                else:
                    foundSpace += 1
                    lSpace = True
                if foundSpace > 1 and not hasWarned:
                    hasWarned = True
                    warnings.warn(f"Many spaces found in variable of line {n+1}, variable names will have spaces removed")
            else:
                valNComp += ltr
                
        if skip:
            continue
        
        if compMode == "var":
            raise Exception(f"Expected '=' in line {n+1}")
        val = json.loads(valNComp)
        parseDict[varNComp] = val
        
    return parseDict

def reparseEnv(parse:dict):
    """
    MODULE FUNCTION (DO NOT RUN)
    """
    parsed = ""
    for key in parse:
        parsed += f"{key}={json.dumps(parse[key])}\n"
    return parsed[:-1]
    
def load(fileName:str=None,loadAllEnv:bool=False,ignoreCWD:bool=False):
    """
    Loads ENV from file parent
    """
    global ENV
    ENV = {}
    
    if fileName != None:
        if ignoreCWD:
            with open(fileName,"r") as env:
                ENV = parseEnv(env.read())
        else:
            with open(os.getcwd()+"/"+fileName,"r") as env:
                ENV = parseEnv(env.read())
    else:
        posEnv = []
        for env in os.listdir(os.getcwd()):
            if ".grg" in env:
                posEnv.append(env)
                
        if len(posEnv) == 0:
            raise ValueError(".grg file not found, add (fileName) parameter to continue")
        elif len(posEnv) > 1 and not loadAllEnv:
            raise ValueError("multiple .grg files found, add (fileName) parameter to continue or set (loadAllEnv) to True")
        elif loadAllEnv:
            for envN in posEnv:
                with open(os.getcwd()+"/"+envN,"r") as env:
                    envA = parseEnv(env.read())
                    for envK in envA:
                        ENV[envK] = envA[envK]
        else:
            with open(os.getcwd()+"/"+posEnv[0],"r") as env:
                ENV = parseEnv(env.read())
                
def save(fileName:str=None):
    """
    Saves ENV to file parent file
    """
    
    if "ENV NOT INITIALIZED" in ENV:
        raise Exception("ENV NOT INITIALIZED")
        
    if fileName != None:
        with open(os.getcwd()+"/"+fileName,"w") as env:
            env.write(reparseEnv(ENV))
    else:
        posEnv = []
        for env in os.listdir(os.getcwd()):
            if ".grg" in env:
                posEnv.append(env)
                
        if len(posEnv) == 0:
            raise ValueError(".grg file not found, add (fileName) parameter to continue")
        elif len(posEnv) > 1:
            raise ValueError("multiple .grg files found, add (fileName) parameter to continue")
        else:
            with open(os.getcwd()+"/"+posEnv[0],"w") as env:
                env.write(reparseEnv(ENV))