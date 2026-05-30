from .connector import HTTPResponse,HTTPReturn,HTTPServer,HTTPChild,Returns
from ..logger.basic_logs import *
from threading import Thread
import os
import traceback

image_mappings = {"png":"image/png","jpeg":"image/jpeg","jpg":"image/jpeg","ico":"image/x-icon"}

class Server:
    
    _server:HTTPServer
    icon:bytes|None = None
    icon_type:str|None = None
    close:bool = False
    children:list[HTTPChild] = []
    
    def __init__(self,port:int,icon:str|None = None,icon_type:str|None=None,/,ip:str="127.0.0.1"):
        """
        Creates a server on the port
        
        **Methods you should overwrite**
        - .GET
        - .POST
        
        *more coming soon*
        
        Use the .serve() method to begin serving
        
        Arguments:
            port:
                The port to host on
                
                For localhost any port is generally fine
                
                For hosting a machine IP
                80 is for HTTP connection
                443 is for HTTPS connection **HTTPS does not work with this due to protocols**
            icon:
                The path of the icon (or none for no icon)
            icon_type:
                The format of the icon file (none will try to auto assume)
                
                For example:
                image/png
                image/jpeg
                image/x-icon
                ...
            ip:
                The IP address (127.0.0.1 is for localhost)
                To get the machine IP use socket.gethostbyname(socket.gethostname())
        """
        
        # Make server
        self._server = HTTPServer(port,ip)
        
        # Load icon
        if icon is not None:
            info("Using icon: "+icon,__name__) 
            
            # Get icon data
            with open(icon,"rb") as r:
                
                self.icon = r.read()
                
            # Get icon type
            if icon_type is None:
                file_type = os.path.basename(icon).split(".")[-1]
                
                try:
                    icon_type = image_mappings[file_type]
                except Exception:
                    raise IndexError(f"Could not find format for file of type '{file_type}'\nUse icon_type to manually specify")
                
            self.icon_type = icon_type
            
    def force_close(self):
        """
        Attempt to force close the server and all clients
        """
        info("Serving closing",__name__)
        self.close = True
    
    def _get(self,response:HTTPResponse) -> HTTPReturn:
        """
        The base GET method
        
        Arguments:
            response:
                The response from the client
                
        Return:
            The return from the server
        """
        
        info(f"GET at redirect: '{response.redirect}'",__name__)
        
        try:
            http_return = self.GET(response.redirect)
        except Exception:
            print(traceback.format_exc())
            return Returns.error500()
        
        if http_return is None:
            return Returns.error404()
        
        info(f"GET at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",__name__)
        
        return http_return
    
    def _post(self,response:HTTPResponse) -> HTTPReturn:
        """
        The base POST method
           
        Arguments:
            response:
                The response from the client
                
        Return:
            The return from the server
        """
        
        info("POST at redirect: '"+response.redirect+"'",__name__)
        
        try:
            http_return = self.POST(response.redirect,response.content)
        except Exception:
            print(traceback.format_exc())
            return Returns.error500()
        
        if http_return is None:
            return Returns.error404()
        
        info(f"POST at redirect: '{response.redirect}' RESPONSE: {http_return.headers["Content-Type"]}",__name__)
        
        return http_return

    def GET(self,redirect:str) -> HTTPReturn:
        """
        HTTP GET method
        
        Arguments:
            redirect:
                The redirect location (or a blank string for no redirects)
                
                For example: hyperlink/location/test/foo/baz/bar
                
        Return:
            The HTML response
        """
        
        raise NotImplementedError("Server GET method has not been defined\nDefine a GET method for this server for it to work")
    
    def POST(self,redirect:str,content:str) -> HTTPReturn:
        """
        HTTP POST method
        
        Arguments:
            redirect:
                The redirect location (or a blank string for no redirects)
                
                For example: hyperlink/location/test/foo/baz/bar
            content:
                The content sent
                
        Return:
            The HTTPResponse instance
        """
        
        raise NotImplementedError("Server POST method has not been defined\nDefine a POST method for this server for it to work")    
    
    def serve(self,backlog:int=5) -> None:
        """
        Begin the server and begin blocking
        If you wish to prevent blocking, run on a thread (this is thread-safe)
        
        Connected clients will be new created threads
        
        To close the server run .close_force() and all connected clients will attempt to close as well
        
        Arguments:
            backlog:
                Maximum number of queued connections before refusing more
        """
        
        # Listen
        info(f"Server starting at port {self._server.address}",__name__)
        self._server.listen(backlog)
        
        # Get clients
        while not self.close:
            info("Waiting for connection",__name__)
            new_child = self._server.accept()
            
            self.children.append(new_child)
            
            info(f"New child connected {new_child.client_address}",__name__)
            
            i = 0
            while i < len(self.children):
                
                child = self.children[i]
                
                if child.close:
                    
                    self.children.pop(i)
                    i -= 1
                    
                i += 1   
                
            Thread(target=self.client,args=(new_child,)).start()  
            
        # Close all
        for child in self.children:
            
            child.close_force()
            
    def client(self,instance:HTTPChild) -> None:
        
        # Begin serving
        while not instance.close:
            
            # Get data or stop server
            try:
                response = instance.recv()
                
            except ConnectionError:
                
                break
            
            match response.type:
                
                case "GET":
                    
                    # Check for icon request and return auto
                    if response.redirect == "favicon.ico":
                        info(f"GET at redirect favicon.ico\n({instance.client_address}) Responding with favicon of type: '{self.icon_type}'",__name__)
                        
                        if self.icon is not None:
                            output = HTTPReturn(self.icon,content_type=self.icon_type)
                        else:
                            output = HTTPReturn(b"",content_type="text/plain")
                    
                    else:
                        
                        output = self._get(response)
                
                case "POST":
                    
                    output = self._post(response)
                
                case _:
                    
                    raise ValueError(f"({instance.client_address}) Unknown data type: '{response.type}'")
                
            try:
                instance.send(output)
            except Exception:
                print(traceback.format_exc())
                instance.send(Returns.error500())
            
        info(f"Child {instance.client_address} closed",__name__)