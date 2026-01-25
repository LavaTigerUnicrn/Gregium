"""
The root of Gregium

Holds some import values
"""
import os

if "temp" not in os.listdir():
    
    os.mkdir("temp")

VERSION = "2.0.1"