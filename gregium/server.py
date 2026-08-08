import logging
import socket
import threading
import time
from typing import Any

logger = logging.getLogger(__name__)

HOST_NAME: str = socket.gethostname()
HOST_ADDRESS: str = socket.gethostbyname(
    HOST_NAME
)  # Generally the 192 IP address is better than the 10 IP address here


def format_data(data: bytes) -> bytes:
    """
    Adds a header to bytes

    Returns formatted bytes
    """

    # Get data length converted to bytes
    data_len: int = len(data)
    data_len_bytes: bytes = data_len.to_bytes((data_len.bit_length() - 1) // 8 + 1)

    # Make header
    data_header: bytes = len(data_len_bytes).to_bytes() + data_len_bytes

    # Combine header
    return data_header + data


def send_data(socket: socket.socket, data: bytes) -> bytes:
    """
    Sends data across the socket using the Gregium format

    Returns the sent bytes
    """

    # Format data
    data_form: bytes = format_data(data)

    # Send data
    socket.send(data_form)
    return data_form


def recv_data(socket: socket.socket) -> bytes:
    """
    Receives a single packet of data across the socket

    **MUST USE FORMAT GIVEN BY SEND_DATA**

    Returns the received data
    """

    # Get data length length then data length then data
    return socket.recv(int.from_bytes(socket.recv(int.from_bytes(socket.recv(1)))))


class ClientInst:
    """
    An instantiated server client
    """

    data: Any = None
    _parent: "Server"
    __address: tuple[str, int]
    _sock: socket.socket
    _thread: threading.Thread
    _started: bool = False

    def __init__(self, conn: socket.socket, addr: tuple[str, int], parent: "Server"):
        """
        **THIS SHOULD NOT BE USED FOR MAKING CLIENTS**

        **THIS IS ONLY FOR SOCKET CONNECTIONS TO THE SERVER**
        """

        # Set values
        self._parent = parent
        self.__address = addr
        self._sock = conn

        # Create thread
        self._thread = threading.Thread(target=self._start)

        # Start thread
        self._thread.start()
        self._started = True

    def disconnect(self) -> None:
        """
        Disconnect the client from the server
        """
        self._sock.close()

    def _start(self) -> None:

        self._parent.START(self)

        while not self._parent._closed:

            try:
                self._parent.RUN(self, self.data)
            except OSError:
                logger.warning(
                    f"Client at {self.__address} disconnected ({self._parent.get_child_count() - 1} connected)"
                )
                self._parent.on_disconnect(self)

    @property
    def address(self) -> tuple[str, int]:
        """
        The address of the client
        """
        return self.__address

    def send(self, data: bytes) -> None:
        """
        Sends the given data to the client
        """

        send_data(self._sock, data)

    def recv(self) -> bytes:
        """
        Receives a single packet of data from the client

        Returns the bytes

        **Will block until data**
        """

        return recv_data(self._sock)


class Server:
    """
    Basic server to send bytes data across
    """

    __port: int
    __address: str
    _sock: socket.socket
    _closed: bool = False
    _children: list[ClientInst]

    def __init__(self, port: int, address: str = HOST_ADDRESS):
        """
        Creates a socket server
        Always uses AF_INET and SOCK_STREAM

        To start the sever run .serve()

        **Ensure the .START and .RUN methods have been defined**
        **Either define manually, with child class, or using @Server.event decorator**

        *The on_disconnect event may be redefined in the same way, but are not required*

        Arguments:
            port:
                The port to host on
            address:
                The IP address to host on (generally should always be the host address)

        Examples:
        ```python
            server = Server()

            # Runs a single time on instantiating client
            def START(self:Server,client:ClientInst):
                client.data = "HELLO!" # Data can be set at any time and will be the parameter in RUN
                # Generally data should be in an instantiated class or object
            server.START = START

            # Runs constantly
            @server.event
            def RUN(self:Server,client:ClientInst,data:str): # Note that data type is known to be a string from the START function
                print(client.recv())
                client.send(data.encode('utf-8')) # Will send "HELLO!"
        ```
        """

        # Set values
        self.__port = port
        self.__address = address
        self._allow_print = print

        # Make server socket
        sock = socket.socket()
        self._sock = sock
        logger.info(f"Created sever socket at: {port}, {address}")

        # Bind socket
        sock.bind((address, port))

        # Default values
        self._children = []

    @property
    def port(self) -> int:
        """
        The port the server is hosting on
        """
        return self.__port

    @property
    def address(self) -> str:
        """
        The IP address the server is hosting on
        """
        return self.__address

    def get_child_count(self) -> int:
        return len(self._children)

    def prune(self) -> None:
        """
        Removes all children that are no longer alive
        """

        i = 0
        while i < len(self._children):

            child = self._children[i]

            if child._started and not child._thread.is_alive():

                self._children.pop(i)

                i -= 1

            i += 1

    def _prune(self) -> None:

        while not self._closed:

            self.prune()

            time.sleep(0.01)

    def listen(self, backlog: int = 5) -> None:
        """
        Begins listening as the server
        """

        logger.info(f"Began listening on server (backlog: {backlog})")

        self._sock.listen(backlog)

    def accept(self) -> None:
        """
        Wait for and accept an incoming connection

        Generally using .serve() is better
        """

        # Accept connection
        conn, addr = self._sock.accept()
        logger.info(
            f"Client connected at {addr} ({self.get_child_count() + 1} connected)"
        )

        # Create and start child process
        child = ClientInst(conn, addr, self)

        # Register child
        self._children.append(child)

    def serve(self, backlog: int = 5) -> None:
        """
        Begin the server and begin blocking
        If you wish to prevent blocking, run on a thread (this is thread-safe)

        Will also create a thread to prune children (this thread will be killed on .close())

        Connected clients will be new created threads
        """

        self.listen(backlog)

        threading.Thread(target=self._prune).start()

        logger.info("Server accepting connections")
        while not self._closed:

            self.accept()

    def close(self) -> None:
        """
        Stop server and clients
        """

        logger.info("Server stopped")

        self._sock.close()

        self._closed = True

    def START(self, client: ClientInst) -> None:
        """
        This function is run on clients when they are instantiated
        """

        logger.error('No method has been set for "START" on the server')
        raise NotImplementedError('No method has been set for "START" on the server')

    def RUN(self, client: ClientInst, data: Any) -> None:
        """
        This function is run on clients after instantiating until they close
        """

        logger.error('No method has been set for "RUN" on the server')
        raise NotImplementedError('No method has been set for "RUN" on the server')

    def on_disconnect(self, client: ClientInst) -> None:
        """
        This function is run only when the connection to the client ends without logger.error

        Note that send and recv functions will not work on a closed connection
        """

    def event(self, func):
        """
        A decorator for setting RUN or START methods
        """

        # Add self argument
        def func_registered(*args, **kwargs):

            return func(self, *args, **kwargs)

        # Integrate function in correct location
        match func.__name__:
            case "START":
                self.START = func_registered
                logger.info('Registered "START" function')
            case "RUN":
                self.RUN = func_registered
                logger.info('Registered "RUN" function')
            case "on_disconnect":
                self.on_disconnect = func_registered
                logger.info('Registered "on_disconnect" function')
            case _:
                raise NameError(
                    f'Unknown function name "{func.__name__}" (should be of "START" or "RUN")'
                )

        return func


class Client:

    __port: int
    __address: str
    _sock: socket.socket

    def __init__(self, port: int, address: str):
        """
        Makes a socket client
        Always uses AF_INET and SOCK_STREAM

        To connect the client run .connect()

        Use .send() and .recv() to run the given actions

        Arguments:
            port:
                The port to connect to
            address:
                The IP address to connect to
        """

        # Set values
        self.__port = port
        self.__address = address

        # Make client socket
        self._sock = socket.socket()
        logger.info("Created client socket")

    def connect(self) -> None:
        """
        Attempt to connect the client to the server
        """

        # Get address
        port = self.__port
        address = self.__address

        # Connect socket
        self._sock.connect((address, port))
        logger.info(f"Connected connected to socket at: {port}, {address}")

    def disconnect(self) -> None:
        """
        Disconnect the client from the server
        """
        self._sock.close()

    def send(self, data: bytes) -> None:
        """
        Sends the given data to the server
        """

        send_data(self._sock, data)

    def recv(self) -> bytes:
        """
        Receives a single packet of data from the server

        Returns the bytes

        **Will block until data**
        """

        return recv_data(self._sock)

    @property
    def port(self) -> int:
        """
        The port the client is connected to
        """
        return self.__port

    @property
    def address(self) -> str:
        """
        The IP address the client is connected to
        """
        return self.__address
