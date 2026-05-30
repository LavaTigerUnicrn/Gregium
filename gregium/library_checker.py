"""
Ensures libraries exist before importing them
"""
import os
import subprocess
from .logger.basic_logs import *
import platform
from typing import Literal

def install_pip():
    """
    Ensures pip exists and is updated
    """
    
    # Run update / install command
    os.system("python3 -m ensurepip --upgrade")

# Install queue
PIP_MUST_INSTALL = {}

# Module list
MODULE_LIST = ""

# System
SYSTEM = platform.system()

# Possible systems
System = Literal["Linux","Windows","Java",None]

def get_version(library_pip:str):
    """
    Gets the version number of a library from pip
    """
    
    # Run pip show library
    process = subprocess.run(f"pip show {library_pip}",capture_output=True)
    
    # Split the output by lines
    stdout = process.stdout.split(b"\r\n")
    
    # Read each line
    for line in stdout:
        
        # Find version line
        if b"Version" in line:
            return str(line,"utf-8").replace("Version: ","")

def check_library(library_name:str,library_pip:str,version:str="",system:System=None,skip_import:bool=False):
    """
    Makes sure a library exists before importing
    
    **Run install_all to install checked libraries**
    
    Arguments:
        library_name:
            The directory name of the library (what you use to import it)
        library_pip:
            The pip name of the library
        version:
            The version of the library
        system:
            The system for the library to be present on (none means any)
        skip_import:
            Skips importing the library (for libraries that have dll like pygame)
    """
    global PIP_MUST_INSTALL,MODULE_LIST
    
    # Check if system is right
    if system is not None:
        if system != SYSTEM:
            info(f"System not required: {library_name}",__name__)
            return
    
    # Add to MODULE_LIST
    MODULE_LIST += f"{library_name}{":" if version != "" else ""} {version}\n"
    
    # Try to import
    try:
        
        # Check for library
        info(f"Checking presence: {library_name}",__name__)
        if not skip_import:
            __import__(library_name)
        if not get_exists(library_pip):
            raise ModuleNotFoundError("Library does not exist")
        info(f"Found: {library_name}",__name__)
        
        # Only check if version is specified in call
        if version != "":
            lib_version = get_version(library_pip)
            
            # Check if version is correct
            if lib_version != version:
                
                # Notify and add to queue
                warn(f"Version: {lib_version} (Incorrect)",__name__)
                PIP_MUST_INSTALL[library_pip] = version
            else:
                
                # Notify that version is corect
                info(f"Version: {lib_version} (Correct)",__name__)
        
    # On failure, queue download
    except ModuleNotFoundError:
        
        warn(f"Module: {library_name} not found pip: {library_pip}",__name__)
        PIP_MUST_INSTALL[library_pip] = version
    
    # Unknown error, queue download as well
    except Exception as e:
        
        error(f"Module version check failed: {e}")
        PIP_MUST_INSTALL[library_pip] = version

def get_exists(library_pip:str) -> bool:
    """
    Gets the library existence using pip (this is slow)
    """
    
    # Run pip show library
    process = subprocess.run(f"pip show {library_pip}",capture_output=True)
    
    # Split the output by lines
    stdout = process.stdout.split(b"\r\n")
    
    # Check if blank
    if stdout == [b""]:
        return False
        
    return True 
        
def install_all():
    """
    Clears the queue of libraries to install and installs them all
    """
    
    # Skip if everything is installed
    if len(PIP_MUST_INSTALL) == 0:
        
        info("No modules needed to download",__name__)
        
        # Print final message
        info(f"\n\nAll modules verified\n{MODULE_LIST}",__name__)
    
        return
    
    # Use confirmation
    confirm = input(f"You must install: \x1b[32;1m({", ".join([x+("==" if PIP_MUST_INSTALL[x] != "" else "")+PIP_MUST_INSTALL[x] for x in list(PIP_MUST_INSTALL.keys())])})\x1b[0m are you sure?\ny/n\n")
    if confirm.lower() != "y":
        print("Canceled install")
        return
        
    # Get packages formatted to install
    package_install:str = ""
    
    for package in PIP_MUST_INSTALL:
        
        #  Get package version
        version = PIP_MUST_INSTALL[package]
        
        # If version specified, download that version
        if version != "":
            
            package_install += f"{package}=={version} "
        
        # Otherwise install latest
        else:
            package_install += f"{package} "
    
    info(f"Installing {package_install}",__name__)
    
    # Run install command (Making sure it works either way)
    os.system(f"pip install {package_install} --break-system-packages")
    
    # Print final message
    info(f"\n\nAll modules verified\n{MODULE_LIST}",__name__)
    
def verify_lib():
    """
    Checks and downloads all libraries for gregium to function
    """
    
    # Log info message
    print("Checking libraries")
    info("Checking libraries",__name__)
    
    # Check libraries
    check_library("edge_tts","edge-tts","7.2.7")
    check_library("blessed","blessed","1.25.0","Windows")
    check_library("ollama","ollama","0.6.1")
    check_library("bs4","beautifulsoup4","4.14.3")
    check_library("PIL","pillow","11.3.0")
    check_library("pygame","pygame-ce","2.5.6",skip_import=True)
    check_library("RealtimeSTT","realtimestt","0.3.104",skip_import=True)
    check_library("RealtimeTTS","realtimetts","0.5.7",skip_import=True)
    check_library("requests","requests")
    check_library("dotenv","dotenv")
    
    # Download libraries
    install_all()