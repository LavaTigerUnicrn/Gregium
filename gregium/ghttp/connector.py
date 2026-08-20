import datetime
import json
import logging
import mimetypes
import re
import socket
from typing import Any, Literal

logger = logging.getLogger(__name__)

ENCODING = "utf-8"

class HTTPResponse:
    """
    A generic HTTP response

    This comes from the *client* side

    :param data: Raw receive data
    :type data: bytes
    :param parent: The server parent in case more data must be gotten
    :type parent: HTTPChild
    """

    data:bytes
    "The raw data"
    type:str
    "HTTP type"
    version:str
    "HTTP Version"
    headers:dict[str,str]
    "The raw loaded headers"
    redirect:str
    "The redirect"
    content:bytes = b""
    "The content data"
    cookie:dict[str,str]|None = None
    "Loaded cookies, or none if none are found"

    def __init__(self,data:bytes,parent:"HTTPChild"):

        # Save data
        self.data = data
        data_decode = data.decode(ENCODING)

        # Begin decoding
        pattern = re.compile("([A-Z]+?) \\/(.*?) HTTP\\/(.+)")

        matcher = pattern.match(data_decode)

        if matcher is None:
            raise ValueError(f"No group could be found to load data\n{data}")

        self.type = matcher.group(1)
        self.redirect = matcher.group(2)
        self.version = matcher.group(3)

        # Decode header
        pattern_header = re.compile("^(.*?): (.*?)$")

        self.headers = {}
        data_lines = data_decode.splitlines()
        i = 0
        for line in data_lines:
            i += 1
            if line == "":
                break
            if ":" not in line:
                continue
            matcher = pattern_header.match(line)

            if matcher is None:
                raise ValueError(f"No group could be found to load data\n{data}")

            self.headers[matcher.group(1)] = matcher.group(2)

        if "Cookie" in self.headers:

            # Load cookies
            cookie = self.headers["Cookie"]

            self.cookie = load_cookies(cookie)

        if "Content-Length" not in self.headers:
            return

        expect_size = int(self.headers["Content-Length"])

        if expect_size == 0:
            return

        content = b""

        while len(content) < expect_size: 
            sub_content = parent._recv(expect_size)
            content += sub_content
            if len(sub_content) == 0:
                logger.critical(f"Packet content collision detected (Differ by {expect_size-len(content)}); data corrupted\n\n\n{self.data+content}")
                return

            if expect_size > len(content):

                logger.debug(f"Large packet (Tot Size: {len(content)} Expect: {expect_size} Sub: {len(sub_content)})")

        self.data += content

        self.content = content

    def __str__(self):

        return self.data.decode(ENCODING,errors="ignore")

class HTTPReturn:
    """
    A generic HTTP Return
     
    This comes from the *server* side
    """
    
    version:str
    "HTTP Version"
    headers:dict[str,str]
    "The raw loaded headers"
    code:str
    "The completion code (such as 200 OK)"
    
    def __init__(self,content:bytes,code:str="200 OK",content_type:str=f"text/html; charset={ENCODING}",connection:Literal["keep-alive","close"]="keep-alive",**kwargs:str):
        """
        Makes a HTTP return for the server
        
        :param content: The return data
        :type content: bytes
        :param code: The return code (such as 200 OK)
        :type code: str, optional
        :param content_type: The type of the content to return

            text/html
            application/json
            image/png
            ...
        :type content_type: str
        :param connection: A header if to keep the connection open (generally should be true)
        :type connection: str,optional
        :kwargs: Any additional headers (underscores will be replaced with hyphens)
        :type kwargs: str
        """
        
        # Add header
        self.headers = {}
        for kwarg,kwarg_val in kwargs.items():
            
            self.headers[kwarg.replace("_","-")] = kwarg_val
        
        # Add additional data
        self.headers["Content-Type"] = content_type
        
        self.headers["Connection"] = connection
                
        self._content = content
        
        self.headers["Content-Length"] = str(len(self._content))
        
        self.code = code
        
        self.version = "1.1" # Always the same

    def disable_cache(self) -> None:
        """
        Adds headers to disable caching for this HTTP request
        """

        self.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        self.headers["Pragma"] = "no-cache"
        self.headers["Expires"] = "0"
        
    @property
    def content(self) -> bytes:
        """
        The payload
        """
        return self._content
    
    @content.setter
    def content(self,value:bytes) -> None:
        """
        The payload
        """
        
        self._content = value
        self.headers["Content-Length"] = str(len(self._content))
        
    def set_header(self,header_name:str,header_value:str) -> None:
        """
        Sets a specific header
        
        :param header_name: The name of the header (such as 'Connection')
        :type header_name: str
        :param header_value: The value of the header (such as 'keep-alive')
        :type header_value: str
        """
        
        self.headers[header_name] = header_value
        
    def remove_header(self,header_name:str):
        """
        Removes a specific header
        
        :param header_name: The name of the header (such as 'Connection')
        """
        
        self.headers.pop(header_name)
        
    def generate(self) -> bytes:
        """
        Generates the completed HTTP with headers
        """
        
        # Set date header only upon generating
        self.headers["Date"] = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        # Make code
        out = f"HTTP/{self.version} {self.code}\n"
        
        # Add headers
        for header in self.headers:
            
            out += header + ": "+self.headers[header]+"\n"
        
        return out.encode(ENCODING)+b"\n"+self.content
    
    
    def __str__(self):
        
        return self.generate().decode(ENCODING)

class HTTPChild:
    """
    A HTTP Child that can recv and send connections

    :param conn: The socket connection
    :type conn: socket.socket
    :param address: The address connected to

        (IP,port)
    :type address: tuple[str,int]
    """

    close:bool = False
    
    # Connected address and socket
    client_address:tuple[str,int]
    _conn:socket.socket

    def __init__(self,conn:socket.socket,address:tuple[str,int]):
        
        self._conn = conn
        self.client_address = address

    def _send(self,content:bytes) -> None:
        """
        Sends over content to the client
        
        :param content: The content to send
        :type content: bytes
        """
        
        # Send data
        self.conn.send(content)
        
    def _recv(self,bufsize:int=2048) -> bytes:
        """
        Receives data from the client
        
        :param bufsize: The size of the buffer
        :type bufsize: int

        :return: The data
        :rtype: bytes
        """
        
        # Get data
        data = self.conn.recv(bufsize)
        
        return data
    
    def _recv_until_break(self) -> bytes:
        """
        Receives data from the client
        
        Only gets data until a double newline (\\n\\n) which represents the end of headers
        """
        
        # Prepare output
        out:bytes = b""
        lastGot = b""
        currGotR = b""
        currGot = b""

        while lastGot != b"\n" or currGot != b"\n":
            
            lastGot = currGotR
            currGot = self.conn.recv(1)
            
            # Prevent \r from blocking \n
            if currGot != b"\r":
                currGotR = currGot
            
            out += currGot
        
        return out
    
    def recv(self) -> HTTPResponse:
        """
        Receive data as a HTTP Response
        """
        data = self._recv_until_break()
        
        # Error on blank data
        if data == b"":
            raise ConnectionError("Connection ended")
        
        response = HTTPResponse(data,self)
        
        if "Connection" in response.headers and response.headers["Connection"] == "close":
            self.close = True
        
        return response
    
    def send(self,data:HTTPReturn) -> None:
        """
        Sends over content to the client
        
        :param data: The data to send as a HTTPReturn
        :type data: HTTPReturn
        """
        
        # Close if needed
        if self.close:
            data.set_header("Connection","close")
        
        # Send data
        self.conn.send(data.generate())
    
        # Close if close tag
        if data.headers["Connection"] == "close":
            self.conn.close()
            self.close = True
    
    @property
    def conn(self) -> socket.socket:
        """
        Connected client socket
        """
        if self._conn is None:
            raise ValueError("Connection has not been created yet, use .accept() to create a connection")
        
        return self._conn
    
    def close_force(self):
        """
        Attempt to close the child as soon as possible
        """
        self.close = True

class HTTPServer:
    """
    A socket server
    
    :param port: The port to connect to
    :type port: int
    :param ip: The IP address (127.0.0.1 is for localhost) 
    :type ip: str
    """

    # Self address and socket
    address:tuple[str,int]
    server:socket.socket
    
        
    def __init__(self,port:int,ip:str="127.0.0.1"):
        
        # Update address
        self.address = (ip,port)
        
        # Create socket
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(self.address)
    
    def listen(self,backlog:int=5) -> None:
        """
        Begins listening as the server
        """
        
        self.server.listen(backlog)
    
    def accept(self) -> HTTPChild:
        """
        Accept the client connection
        """
        
        # Connect
        conn, client_address = self.server.accept()
        
        # Make a child
        return HTTPChild(conn,client_address)

class Returns:
    """
    Stubs for easy server returns
    
    **The easiest method is to use .file and supply a file location, if the data is already loaded use any of the given below**
    
    *Also note that some common errors and stubs for redirects are given as well*
    """

    @staticmethod
    def js(content:str):
        """
        Stub for automatically generating JS responses
        """
        content = str(content)
        return HTTPReturn(content=content.encode(ENCODING),content_type=f"text/js; charset={ENCODING}")

    @staticmethod
    def json(content:Any):
        """
        Stub for automatically generating JSON responses
        """
        return HTTPReturn(content=json.dumps(content).encode(ENCODING),content_type=f"application/json; charset={ENCODING}")

    @staticmethod
    def html(content:str):
        """
        Stub for automatically generating HTML responses
        """
        content = str(content)
        return HTTPReturn(content=content.encode(ENCODING),content_type=f"text/html; charset={ENCODING}")

    @staticmethod
    def text(content:str):
        """
        Stub for automatically generating plaintext responses
        """
        content = str(content)
        return HTTPReturn(content=content.encode(ENCODING),content_type=f"text/plain; charset={ENCODING}")

    @staticmethod
    def byte(content:bytes):
        """
        Stub for automatically generating raw byte responses
        """

        return HTTPReturn(content=content,content_type="text/plain")

    @staticmethod
    def css(content:str):
        """
        Stub for automatically generating CSS responses
        """
        content = str(content)
        return HTTPReturn(content=content.encode(ENCODING),content_type=f"text/css; charset={ENCODING}")

    @staticmethod
    def jpeg(content:bytes):
        """
        Stub for automatically generating JPEG responses
        """
        return HTTPReturn(content=content,content_type="image/jpeg")

    @staticmethod
    def png(content:bytes):
        """
        Stub for automatically generating PNG responses
        """
        return HTTPReturn(content=content,content_type="image/png")

    @staticmethod
    def ico(content:bytes):
        """
        Stub for automatically generating X-ICON responses
        """
        return HTTPReturn(content=content,content_type="image/x-icon")

    @staticmethod
    def error404():
        """
        Stub for file not found errors
        """
        return HTTPReturn(b"",code="404 Not Found",content_type="text/plain")

    @staticmethod
    def error500(err:bytes=b""):
        """
        Stub for internal server errors
        """
        return HTTPReturn(err,code="500 Internal Server Error",content_type="text/plain")

    @staticmethod
    def error(code:str):
        """
        More generic error message
        """
        return HTTPReturn(b"",code=code,content_type="text/plain")

    @staticmethod
    def redirect(url:str):
        """
        Stub for redirecting to a given location
        
        Args:
            url:
                The url location to redirect to
        """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="refresh" content="0; url='{url}'" />
        </head>
        <body>
        <p>Redirecting...</p>
        </body>
        </html>
        """

        return_obj = HTTPReturn(html.encode(ENCODING), code="308 Temporary Redirect")
        return_obj.disable_cache()

        return return_obj

    @staticmethod
    def ok():
        """
        200 OK
        """

        return HTTPReturn(b"")

    @staticmethod
    def file(path:str):
        """
        Stub for automatically sending a single file
        
        Will try to guess the encoding and file type of the given file
        
        Args:
            path:
                The file location
        """

        content_type, encoding = mimetypes.guess_type(path)

        with open(path,"rb") as stream:

            data = stream.read()

        if encoding is not None:

            logger.warning(f"Unhandled encoding \"{encoding}\" (This means that a zipped file has been compressed)")

        if content_type is None:

            logger.error(f"Content type for file at path\"{path}\" could not be guessed")

            return HTTPReturn(data,content_type="test/plain")

        return HTTPReturn(data,content_type=content_type)

from .decoder import load_cookies
