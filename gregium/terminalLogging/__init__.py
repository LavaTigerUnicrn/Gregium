"""
An easy terminal logger capable of also saving to a file and timestamping
"""

import sys
import _io
import time

WHITE = "\x1b[37m"
YELLOW = "\x1b[33m"
RED = "\x1b[31m"

class Logger:

    def __init__(self,filepath:str=None,enabled_print:bool=True,enabled_file:bool=True,timestamp:bool=True):
        """
        Generates a basic terminal logger
        
        Args:
            filepath:
                An optional filepath to save logs to
            enabled_print:
                Enables logger to log to terminal
            enabled_file:
                Enables logger to log to file (if specified)
            timestamp:
                Puts timestamps on each log

        """
        self._enabled_print:bool = enabled_print
        self._enabled_file:bool = enabled_file
        self._filepath:str = filepath
        if filepath:
            self._filepathInstance:_io.TextIOWrapper = open(filepath,"w")
        else:
            self._filepathInstance:_io.TextIOWrapper=None
        self._timestamp:bool = timestamp

    @property
    def filepath(self):
        return self._filepath
    
    @filepath.setter
    def filepath(self,value:str):
        assert self._filepath is None, f"To overwrite current filepath ({self._filepath}) instead use force_filepath_change()"

        self._filepath = value
        if value:
            self._filepathInstance = open(value,"w")

    def force_filepath_change(self,filepath:str):
        """
        Will change the current filepath even if one is already loaded"""

        if self._filepath is not None:
            self._filepathInstance.close()

        self._filepath = filepath

        if filepath:
            self._filepathInstance = open(filepath,"w")

    def base_log(self,type:str,message:str,source:str,flush:bool=True,colorKey:str=""):
        """
        Logs type 'type' to terminal and file if allow_log is true

        Args:
            message:
                The message to push
            source:
                A source for where the log is coming from
            flush:
                If sys.stdout should be flushed once message is given
            colorKey:
                ANSI color key
        """

        if self._enabled_print or self._enabled_file:
            formattedMessage = f"[{type} : ({time.strftime("%m/%d/%Y %H:%M:%S",time.localtime())}) : {source}] {message}\n" if self._timestamp else f"[{type} : {source}] {message}\n"

            if self._enabled_print:
                sys.stdout.write(colorKey+formattedMessage+WHITE)

            if flush:
                sys.stdout.flush()
        
            if self._enabled_file:

                if self._filepath is not None:
                    self._filepathInstance.write(formattedMessage)
                    self._filepathInstance.flush()

    def info(self,message:str,source:str,flush:bool=True):
        """
        Logs type 'INFO' to terminal and file if allow_log is true

        Args:
            message:
                The message to push
            source:
                A source for where the log is coming from
            flush:
                If sys.stdout should be flushed once message is given
        """

        self.base_log('INFO',message=message,source=source,flush=flush,colorKey=WHITE)

    def warn(self,message:str,source:str,flush:bool=True):
        """
        Logs type 'WARN' to terminal and file if allow_log is true

        Args:
            message:
                The message to push
            source:
                A source for where the log is coming from
            flush:
                If sys.stdout should be flushed once message is given
        """

        self.base_log('WARN',message=message,source=source,flush=flush,colorKey=YELLOW)

    def error(self,message:str,source:str,flush:bool=True):
        """
        Logs type 'ERROR' to terminal and file if allow_log is true

        Args:
            message:
                The message to push
            source:
                A source for where the log is coming from
            flush:
                If sys.stdout should be flushed once message is given
        """

        self.base_log('ERROR',message=message,source=source,flush=flush,colorKey=RED)

PRIMARY = Logger()