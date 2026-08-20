import logging
import mimetypes
import socket
import ssl
from threading import Thread

from .connector import HTTPChild, HTTPResponse, HTTPReturn, HTTPServer, Returns

logger = logging.getLogger(__name__)

HostName = socket.gethostname()

# Scan for IP
IP_10: str = ""
"The IP address prefixed by 10, 10.X.X.X"
IP_192: str = ""
"The IP address prefixed by 192, 192.168.X.X"
for addr in socket.getaddrinfo(HostName, None):

    # Find the first address that has 10. and 192. prefix
    ip: str = addr[4][0]  # type: ignore

    if ip.startswith("10.") and IP_10 == "":

        IP_10 = ip

    if ip.startswith("192.") and IP_192 == "":

        IP_192 = ip


class Server:

    """
    Creates a server on the port
    
    **Methods you should overwrite**
    
    * .GET

    * .POST
    
    **Additional supported methods**
    
    * .HEAD 1

    * .TRACE 2

    * .PUT

    * .PATCH

    * .OPTIONS

    * .DELETE
    
    1. HEAD uses the same method as GET since HEAD is the same as GET without a body
    2. TRACE is run automatically
    
    *more coming soon*
    
    Use the .serve() method to begin serving
    
    :param port: The port to host on
    :type port: int
        The port to host on
        
        For localhost any port is generally fine
        
        For hosting a machine IP, generally
        80 is for HTTP connection
        443 is for HTTPS connection **Use Server_Secure for HTTPS protocol**
    :param icon: The path of the icon (or None for no icon)
    :type icon: str, optional
    :param ip: The IP address (127.0.0.1 is for localhost)

        To get the machine IP use ghttp.IP_10 for 10. IP, use ghttp.IP_192 for 192. IP
    :type ip: str, optional
    """

    _server: HTTPServer
    icon: bytes | None = None
    icon_type: str | None = None
    close: bool = False
    children: list[HTTPChild]

    def __init__(self, port: int, icon: str | None = None, ip: str = "127.0.0.1"):
        

        # Make server
        self._server = HTTPServer(port, ip)

        # Load icon
        if icon is not None:
            logger.info("Using icon: " + icon)

            # Get icon data
            with open(icon, "rb") as r:

                self.icon = r.read()

            self.icon_type = mimetypes.guess_type(icon)[0]

        self.children = []

    def force_close(self):
        """
        Attempt to force close the server and all clients
        """
        logger.info("Serving closing")
        self.close = True

    def _get(self, response: HTTPResponse) -> HTTPReturn:
        """
        The base GET method

        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """

        logger.debug(f"GET at redirect: '{response.redirect}'")

        try:
            http_return = self.GET(response.redirect)
        except Exception:
            logger.exception("Error during GET method")
            return Returns.error500()

        if http_return is None:
            return Returns.error404()

        logger.debug(
            f"GET at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}"
        )

        return http_return

    def _post(self, response: HTTPResponse) -> HTTPReturn:
        """
        The base POST method
        
        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """

        logger.debug("POST at redirect: '" + response.redirect + "'")

        try:
            http_return = self.POST(response.redirect, response.content)
        except Exception:
            logger.exception("Error during POST method")
            return Returns.error500()

        if http_return is None:
            return Returns.error404()

        logger.debug(
            f"POST at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",
            __name__,
        )

        return http_return

    def _put(self, response: HTTPResponse) -> HTTPReturn:
        """
        The base PUT method
        
        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """

        logger.debug("PUT at redirect: '" + response.redirect + "'")

        try:
            http_return = self.PUT(response.redirect, response.content)
        except Exception:
            logger.exception("Error during PUT method")
            return Returns.error500()

        if http_return is None:
            return Returns.error404()

        logger.debug(
            f"PUT at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",
            __name__,
        )

        return http_return

    def _patch(self, response: HTTPResponse) -> HTTPReturn:
        """
        The base PATCH method
        
        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """

        logger.debug("PATCH at redirect: '" + response.redirect + "'")

        try:
            http_return = self.PATCH(response.redirect, response.content)
        except Exception:
            logger.exception("Error during PATCH method")
            return Returns.error500()

        if http_return is None:
            return Returns.error404()

        logger.debug(
            f"PATCH at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",
            __name__,
        )

        return http_return

    def _options(self, response: HTTPResponse) -> HTTPReturn:
        """
        The base OPTIONS method
        
        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """

        logger.debug("OPTIONS at redirect: '" + response.redirect + "'")

        try:
            http_return = self.OPTIONS(response.redirect, response.content)
        except Exception:
            logger.exception("Error during OPTIONS method")
            return Returns.error500()

        if http_return is None:
            return Returns.error404()

        logger.debug(
            f"OPTIONS at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",
            __name__,
        )

        return http_return

    def _delete(self, response: HTTPResponse) -> HTTPReturn:
        """
        The base DELETE method
        
        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """

        logger.debug(f"DELETE at redirect: '{response.redirect}'")

        try:
            http_return = self.DELETE(response.redirect)
        except Exception:
            logger.exception("Error during DELETE method")
            return Returns.error500()

        if http_return is None:
            return Returns.error404()

        logger.debug(
            f"DELETE at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}"
        )

        return http_return

    def _head(self, response: HTTPResponse) -> HTTPReturn:
        """
        The base HEAD method
        
        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """

        logger.debug("HEAD at redirect: '" + response.redirect + "'")

        try:
            http_return = self.GET(response.redirect)

            # Remove body
            http_return._content = b""
        except Exception:
            logger.exception("Error during HEAD (GET) method")
            return Returns.error500()

        if http_return is None:
            return Returns.error404()

        logger.debug(
            f"HEAD at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",
            __name__,
        )

        return http_return

    def _trace(self, response:HTTPResponse) -> HTTPReturn:
        """
        The base TRACE method
        
        :param response: The response from the client
        :type response: HTTPResponse
        
        :return: The return from the server
        :rtype: HTTPReturn
        """
        
        logger.debug("TRACE at redirect: '" + response.redirect + "'")
        
        try:
            http_return = HTTPReturn(response.data[:-4],content_type="message/http")
        except Exception:
            logger.exception("Error during TRACE method")
            return Returns.error500()
        
        if http_return is None:
            return Returns.error404()
        
        logger.debug(
            f"TRACE at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",
            __name__,
        )
        
        return http_return

    def GET(self, redirect: str) -> HTTPReturn:
        """
        HTTP GET method

        :param redirect: The redirect location (or a blank string for no redirects)

            For example: hyperlink/location/test/foo/baz/bar
        :type redirect: str

        :return: The response (see connector.Returns for easy responses)
        :rtype: HTTPReturn
        """

        raise NotImplementedError(
            "Server GET method has not been defined\nDefine a GET method for this server for it to work"
        )

    def POST(self, redirect: str, content: bytes) -> HTTPReturn:
        """
        HTTP POST method

        :param redirect: The redirect location (or a blank string for no redirects)

            For example: hyperlink/location/test/foo/baz/bar
        :type redirect: str
        :param content: The content sent
        :type content: bytes

        :return: The response (see connector.Returns for easy responses)
        :rtype: HTTPReturn
        """

        raise NotImplementedError(
            "Server POST method has not been defined\nDefine a POST method for this server for it to work"
        )

    def PUT(self, redirect: str, content: bytes) -> HTTPReturn:
        """
        HTTP PUT method

        :param redirect: The redirect location (or a blank string for no redirects)

            For example: hyperlink/location/test/foo/baz/bar
        :type redirect: str
        :param content: The content sent
        :type content: bytes

        :return: The response (see connector.Returns for easy responses)
        :rtype: HTTPReturn
        """

        raise NotImplementedError(
            "Server PUT method has not been defined\nDefine a PUT method for this server for it to work"
        )

    def OPTIONS(self, redirect: str, content: bytes) -> HTTPReturn:
        """
        HTTP OPTIONS method

        :param redirect: The redirect location (or a blank string for no redirects)

            For example: hyperlink/location/test/foo/baz/bar
        :type redirect: str
        :param content: The content sent
        :type content: bytes

        :return: The response (see connector.Returns for easy responses)
        :rtype: HTTPReturn
        """

        raise NotImplementedError(
            "Server OPTIONS method has not been defined\nDefine a OPTIONS method for this server for it to work"
        )

    def PATCH(self, redirect: str, content: bytes) -> HTTPReturn:
        """
        HTTP PATCH method

        :param redirect: The redirect location (or a blank string for no redirects)

            For example: hyperlink/location/test/foo/baz/bar
        :type redirect: str
        :param content: The content sent
        :type content: bytes

        :return: The response (see connector.Returns for easy responses)
        :rtype: HTTPReturn
        """

        raise NotImplementedError(
            "Server PATCH method has not been defined\nDefine a PATCH method for this server for it to work"
        )

    def DELETE(self, redirect: str) -> HTTPReturn:
        """
        HTTP DELETE method

        :param redirect: The redirect location (or a blank string for no redirects)

            For example: hyperlink/location/test/foo/baz/bar
        :type redirect: str

        :return: The response (see connector.Returns for easy responses)
        :rtype: HTTPReturn
        """

        raise NotImplementedError(
            "Server DELETE method has not been defined\nDefine a DELETE method for this server for it to work"
        )

    def serve(self, backlog: int = 5) -> None:
        """
        Begin the server and begin blocking
        If you wish to prevent blocking, run on a thread (this is thread-safe)

        Connected clients will be new created threads

        To close the server run .close_force() and all connected clients will attempt to close as well

        :param backlog: Maximum number of queued connections before refusing more

            Higher numbers use more resources
        :type backlog: int, optional
        """

        # Listen
        logger.info(f"Server starting at port {self._server.address}")
        self._server.listen(backlog)

        # Get clients
        while not self.close:
            logger.debug("Waiting for connection")
            new_child = self._server.accept()

            self.children.append(new_child)

            logger.debug(f"New child connected {new_child.client_address}")

            i = 0
            while i < len(self.children):

                child = self.children[i]

                if child.close:

                    self.children.pop(i)
                    i -= 1

                i += 1

            Thread(target=self.client, args=(new_child,)).start()

        # Close all
        for child in self.children:

            child.close_force()

    def client(self, instance: HTTPChild) -> None:
        """
        The threaded code that is run for each connected client

        This should not be overwritten
        """

        # Begin serving
        while not instance.close:

            # Get data or stop server
            try:
                response = instance.recv()

            except ConnectionError:

                break

            try:

                match response.type:

                    case "GET":

                        # Check for icon request and return auto
                        if response.redirect == "favicon.ico":
                            logger.debug(
                                f"GET at redirect favicon.ico\n({instance.client_address}) Responding with favicon of type: '{self.icon_type}'"
                            )

                            if self.icon is not None and self.icon_type is not None:
                                output = HTTPReturn(
                                    self.icon, content_type=self.icon_type
                                )
                            else:
                                output = HTTPReturn(b"", content_type="text/plain")

                        else:

                            output = self._get(response)

                    case "POST":

                        output = self._post(response)

                    case "HEAD":

                        output = self._head(response)

                    case "PUT":

                        output = self._put(response)

                    case "OPTIONS":

                        output = self._options(response)

                    case "DELETE":

                        output = self._delete(response)

                    case "PATCH":

                        output = self._patch(response)

                    case _:

                        raise ValueError(
                            f"({instance.client_address}) Unknown data type: '{response.type}'"
                        )

                instance.send(output)

            except Exception:
                logger.exception("Error during processing")
                instance.send(Returns.error500())

        logger.debug(f"Child {instance.client_address} closed")

class Server_Secure(Server):

    """
    Creates a server on the port
    
    Make sure to have a certificate and key
    
    Can be self-signed using 
    `openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -nodes -days 365 -subj "/CN=localhost"`
    
    *Almost all browsers will reject self-signed certificates*
    
    **Methods you should overwrite**

    * .GET

    * .POST
    
    **Additional supported methods**
    
    * .HEAD 1

    * .TRACE 2

    * .PUT

    * .PATCH

    * .OPTIONS

    * .DELETE
    
    1. HEAD uses the same method as GET since HEAD is the same as GET without a body
    2. TRACE is run automatically
    
    *more coming soon*
    
    Use the .serve() method to begin serving
    
    :param port: The port to host on
    :type port: int
        The port to host on
    
        For localhost any port is generally fine
    
        For hosting a machine IP, generally
        80 is for HTTP connection
        443 is for HTTPS connection **Use Server_Secure for HTTPS protocol**
    :param cert_path: The path to the certificate (should be a .pem file)
    :type cert_path: str
    :param key_path: The path to the key (should be a .pem file)
    :type key_path: str
    :param password: The password for the certification (only if it is specified)
    :type password: str, optional
    :param icon: The path of the icon (or None for no icon)
    :type icon: str, optional
    :param ip: The IP address (127.0.0.1 is for localhost)

        To get the machine IP use ghttp.IP_10 for 10. IP, use ghttp.IP_192 for 192. IP
    :type ip: str, optional
    """

    def __init__(self, port: int, cert_path:str, key_path:str, password:str|None=None, icon: str | None = None, ip: str = "127.0.0.1"):

        # Make context
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        # Add key and cert
        self.context.load_cert_chain(cert_path,key_path,password)

        # Generate base server
        super().__init__(port,icon,ip)

    def _accept(self) -> HTTPChild|None:
        """
        Accept the client connection
    
        Returns none on ssl failure
        """
    
        _self = self._server
    
        # Connect
        conn, client_address = _self.server.accept()
    
        # Wrap
        try:
            conn = self.context.wrap_socket(conn,True)
        except ssl.SSLError:
    
            logger.exception("Error while wrapping connection (Likely invalid certificate)")
            return None
    
        # Make a child
        return HTTPChild(conn,client_address)

    def serve(self, backlog: int = 5) -> None:
        """
        Begin the server and begin blocking
        If you wish to prevent blocking, run on a thread (this is thread-safe)
    
        Connected clients will be new created threads
    
        To close the server run .close_force() and all connected clients will attempt to close as well

        :param backlog: Maximum number of queued connections before refusing more
        
            Higher numbers use more resources
        :type backlog: int, optional
        """

        # Listen
        logger.info(f"Server starting at port {self._server.address}")
        self._server.listen(backlog)

        # Get clients
        while not self.close:
            logger.debug("Waiting for connection")
            new_child = self._accept()

            if new_child is None:

                continue

            self.children.append(new_child)

            logger.debug(f"New child connected {new_child.client_address}")

            i = 0
            while i < len(self.children):

                child = self.children[i]

                if child.close:

                    self.children.pop(i)
                    i -= 1

                i += 1

            Thread(target=self.client, args=(new_child,)).start()

        # Close all
        for child in self.children:

            child.close_force()
