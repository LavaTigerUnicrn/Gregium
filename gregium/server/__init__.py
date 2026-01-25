import socket
from ..logger.basic_logs import *
from .. import VERSION
from typing import Any,Literal
import zipfile

HOST_NAME = socket.gethostname()
HOST_PORT = socket.gethostbyname(HOST_NAME)

MAXIMUM_RECV_DATA = None

DataType = Literal["data_NORM","data_FILE","data_ZFIL"]

class FileList(list):
    """
    Contains a list of files
    """
class File(str):
    """
    Contains a file
    """

def send_data(socket:socket.socket,data:bytes,data_type:DataType="data_NORM") -> None:
    """
    Sends data across a socket using Gregium format
    
    Arguments:
        socket:
            The socket to send across
        data:
            The data to send
    """
    
    # Format data
    data_length = len(data)
    data_header = "Gregium "+str(data_length)+" "+data_type
    data_header = (chr(len(data_header)) + data_header).encode("utf-8")
    data_formatted = data_header+data
    
    # Send data
    socket.send(data_formatted)
    
def recv_data(socket:socket.socket) -> tuple[bytes,str]:
    """
    Recv data from a socket using Gregium format
    
    Use `decrypt_recv` to run appropriate action on data
    
    Arguments:
        socket:
            The socket to recv from
            
    Returns (tuple): A tuple containing (data,data_type)
    """
    
    # Get data header start
    try:
        data_header_length = socket.recv(1)[0]
    except:
        critical("Socket returned empty data (socket likely stopped)",__name__)
        raise ConnectionError("Socket returned empty data (socket likely stopped)")
    
    # Get data header
    data_header = socket.recv(data_header_length).decode("utf-8")
    
    # Get data header
    try:
        header = data_header.split(" ")
        data_length = int(header[1])
    except:
        critical("Malformed data header",__name__)
        raise ConnectionError("Malformed data header")
    
    # Check if remaining data is valid
    if MAXIMUM_RECV_DATA is not None:
        if data_length > MAXIMUM_RECV_DATA:
            critical(f"Data length: {data_length} exceeds MAXIMUM_RECV_DATA: {MAXIMUM_RECV_DATA}",__name__)
            raise ConnectionError(f"Data length: {data_length} exceeds MAXIMUM_RECV_DATA: {MAXIMUM_RECV_DATA}")
    
    # Append remaining data
    if data_length > 0:
        data = socket.recv(data_length)
    
    # Clear header and return
    return (data,header[2])

def decrypt_recv(data:tuple[bytes,str]):
    """
    Decrypts the recv data (directly from `recv_data` function)
    """
    
    data_b,data_type = data
    
    match data_type:
        
        case "data_NORM":
            
            return data_b.decode("utf-8")
        
        case "data_ZFIL":
            
            return FileList(load_zip(data_b))
        
        case "data_FILE":
            
            return File(load_file(data_b))
        
        case _:
            
            critical(f"Unknown data type '{data_type}'",__name__)
            raise Exception(f"Unknown data type '{data_type}'")

def load_file(data:bytes) -> str:
    """
    Loads the file into temp directory
    
    Argument:
        data:
            The data contained in the file
            
    Return (str): The name of the file (found in temp)
    """
    
    # Get file name
    name_length = data[0]
    file_name = data[1:name_length+1].decode("utf-8")
    data = data[1+name_length:]
    
    # Write data
    with open("temp/"+file_name,"wb") as fp:
        
        fp.write(data)
        
    return file_name

def load_zip(data:bytes) -> list[str]:
    """
    Loads all the files in a zip path into the temp directory
    
    Arguments:
        data:
            The data contained in the zip
            
    Returns (list): The names of each of the files (found in temp)
    """
    
    # Write zip data
    with open("temp/zip_load.zip","wb") as fp:
        
        fp.write(data)
        
    # Read files from zip and write
    with zipfile.ZipFile("temp/zip_load.zip","r") as zp:
        
        files = [x.filename for x in zp.filelist]
        
        # Read each file
        for file in files:
            
            file_data = zp.read(file)
            
            # Write into temp
            with open("temp/"+file,"wb") as fp:
                
                fp.write(file_data)
            
    return files

class Server:
    """
    An easy way to interact with python sockets using Gregium format
    
    This works best with a single client but does partially support multiple
    (It is better to manually interact with the server socket for multiple clients)
    
    Use `.socket_inst` to interact with the root socket (at your own risk)
    
    Use `.client_inst` to interact with clients.
    Has format of [(client_socket, client_address, {client_info_key:client_info_value})]
    
    Use `.client` to interact with main client (this will be the most recently connected client or manually set by `.bind_client`)
    """
    socket_inst:socket.socket
    client_inst:list[tuple[socket.socket,tuple[str,int],dict[str,Any]]]
    client:socket.socket
    
    def __init__(self,port:int=9000,family:socket.AddressFamily=socket.AF_INET,type:socket.SocketKind=socket.SOCK_STREAM):
        """
        Generates a new Server
        
        This works best with a single client but does partially support multiple
        (It is better to manually interact with the server socket for multiple clients)
        
        Use `.socket_inst` to interact with the root socket (at your own risk)
        
        Use `.client_inst` to interact with clients.
        Has format of [(client_socket, client_address, {client_info_key:client_info_value})]
        
        Use `.client` to interact with main client (this will be the most recently connected client or manually set by `.bind_client`)
        
        Argument:
            port:
                The port the server should host on (must sync with client)
            family:
                The address family the server should host on (must sync with client)
            type:
                The type the server should host on (must sync with server)
        """
        # Set values
        self._port = port
        self._family = family
        self._type = type
        
        # Make socket
        info("Generated new server socket",__name__)
        self.socket_inst = socket.socket(family=family,type=type)
        
        # Make clients
        self.client_inst = []
        self.client = None
        
    @property
    def port(self):
        """
        The port the server is hosting on
        """
        
        return self._port
    
    @property
    def family(self):
        """
        The address family the server is hosting on
        """
        
        return self._family

    @property
    def type(self):
        """
        The type the server is hosting on
        """
        
        return self._type
    
    def host(self,address:None|str=None,port:int|None=None) -> None:
        """
        Allows for clients to connect to the server
        
        Arguments:
            address:
                The address to host on (otherwise will be system port)
            port:
                The port to host on (otherwise will use port set in `__init__`)
        """
        
        # Set missing port        
        if port is None:
            port = self.port
            
        # Set missing address
        if address is None:
            address = HOST_PORT
            
        # Accept connections
        socket_inst = self.socket_inst
        
        socket_inst.bind((address,port))
        socket_inst.listen()
        info(f"Waiting for connection on server address: {address} port: {port}",__name__)
        
        conn,addr = socket_inst.accept()
        self.client = conn
        info(f"Connected to address: {addr[0]}, port: {addr[1]}",__name__)
        
        self.client_inst.append((conn,addr))
        
        # Send started info
        self.send(f"Gregium V{VERSION}")
    
    def bind_client(self,client_index:int) -> None:
        """
        Binds the main client on the server
        
        Argument:
            client_index:
                The index of the client as found in `.client_inst`
        """
        
        # Set client
        self.client = self.client_inst[client_index][0]
        
    def send(self,data:str,index:int|None=None) -> None:
        """
        Sends data over to the main client using Gregium format
        
        Arguments:
            data:
                The data to send
            index:
                The index to send data across (otherwise uses main)
        """
        
        # Get client
        if index is None:
            client = self.client
        else:
            client = self.client_inst[index][0]
        
        # Send data across main
        send_data(client,data.encode("utf-8"))
    
    def recv_raw(self,index:int|None=None) -> bytes:
        """
        Waits for data over from the main client using Gregium format
        
        Arguments:
            index:
                The index to wait for data across (otherwise uses main)
        """
        
        # Get client
        if index is None:
            client = self.client
        else:
            client = self.client_inst[index][0]
            
        # Get data
        return recv_data(client)
    
    def recv(self,index:int|None=None) -> bytes:
        """
        Waits for data over from the main client using Gregium format
        
        Automatically decrypts the data
        
        Arguments:
            index:
                The index to wait for data across (otherwise uses main)
        """
        
        return decrypt_recv(self.recv_raw(index))
    
class Client:
    """
    An easy way to interact with servers using Gregium format
    
    Use `.socket_inst` to interact with the root socket (at your own risk)
    """
    
    def __init__(self,port:int=9000,family:socket.AddressFamily=socket.AF_INET,type:socket.SocketKind=socket.SOCK_STREAM):
        """
        Generates a new Client
        
        Use `.socket_inst` to interact with the root socket (at your own risk)
        
        Argument:
            port:
                The port the client should connect on (must sync with server)
            family:
                The address family the client should connect on (must sync with server)
            type:
                The type the client should connect on (must sync with server)
        """
        # Set values
        self._port = port
        self._family = family
        self._type = type
        
        # Make socket
        info("Generated new client socket",__name__)
        self.socket_inst = socket.socket(family=family,type=type)
        
    @property
    def port(self):
        """
        The port the client is connecting on
        """
        
        return self._port
    
    @property
    def family(self):
        """
        The address family the client is connecting on
        """
        
        return self._family

    @property
    def type(self):
        """
        The type the client is connecting on
        """
        
        return self._type

    def connect(self,address:None|str=None,port:int|None=None):
        """
        Allows for the client to connect to a server
        
        Arguments:
            address:
                The address to host on (otherwise will be system port)
            port:
                The port to host on (otherwise will use port set in `__init__`)
        """
        
        # Set missing port        
        if port is None:
            port = self.port
            
        # Set missing address
        if address is None:
            address = HOST_PORT
            
        # Connect client
        socket_inst = self.socket_inst
        
        info(f"Client waiting for connecting on server address: {address} port: {port}",__name__)
        socket_inst.connect((address,port))

        info(f"Connected to address: {address}, port: {port}",__name__)
        
        # Send started info
        self.send(f"Gregium V{VERSION}")
        
    def send(self,data:str):
        """
        Sends data over to the server using Gregium format
        
        Arguments:
            data:
                The data to send
        """
        
        # Send data across server
        send_data(self.socket_inst,data.encode("utf-8"))
        
    def send_file(self,path:str):
        """
        Sends a file over to the server using Gregium format
        
        This is better for smaller files (for larger use `.send_file_zipped`)
        
        Arguments:
            path:
                The path of the file to send
        """
        
        # Read file
        with open(path,"rb") as fp:
            data = fp.read()
        
        # Format path
        path_base = os.path.basename(path)
        path_formatted = (chr(len(path_base))+path_base).encode("utf-8")
        
        # Send data
        send_data(self.socket_inst,path_formatted+data,"data_FILE")
        
    def send_file_zipped(self,path:str):
        """
        Sends a file zipped over to the server using Gregium format
        
        This is better for larger files (for smaller use `.send_file`)
        
        Arguments:
            path:
                The path of the file to send
        """
        
        # Zip file
        zip_path = "./temp/"+os.path.basename(path)+".zip"
        with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=5) as zp:
            
            zp.write(path,os.path.basename(path))
            
        # Read file
        with open(zip_path,"rb") as fp:
            data = fp.read()
        
        # Send data
        send_data(self.socket_inst,data,"data_ZFIL")
        
    def recv_raw(self) -> bytes:
        """
        Waits for data from the server using Gregium format
        """
            
        # Get data
        return recv_data(self.socket_inst)
    
    def recv(self):
        """
        Waits for data from the server using Gregium format
        
        Automatically decrypts the data
        """
        
        # Get and decrypt data
        return decrypt_recv(self.recv_raw())