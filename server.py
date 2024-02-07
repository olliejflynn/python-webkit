import management_console as MC
import socket, signal, threading, sys

config =  {
            "HOST_NAME" : "127.0.0.1",
            "BIND_PORT" : 4000,
            "MAX_REQUEST_LEN" : 1024,
            "CONNECTION_TIMEOUT" : 5,
            "CACHE_SIZE" : 10
          }

class Server():

    def __init__(self):

        self.MC = MC.ManagementConsole()

        # shutdown server on ^C input
        signal.signal(signal.SIGINT, self.handleKill)

        # Default TCP socket using ip adress family (AF_INET) and set as a streaming socket (tcp)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Setting options for socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to configured port
        self.serverSocket.bind((config["HOST_NAME"], config["BIND_PORT"]))

        # Start the server socket listening (max 10 connections)
        self.serverSocket.listen(10) 
        self.__clients = {}

        self.choice = 0


    def begin(self):

        self.MC.start()
        self.handleKill(0,0)

        #waiting for client to connect
        while True:

            # get the clients socket and IP
            (clientSocket, client_address) = self.serverSocket.accept() 

            #start a thread which runs the server_thread function 
            t = threading.Thread(name=client_address, 
                    target = self.server_thread, args=(clientSocket, client_address))
            t.setDaemon(True)
            t.start()

        self.shutdown(0,0)
    
    def server_thread(self, client_sock, client_address):

        # Get the request from browser
        forward_request = client_sock.recv(config['MAX_REQUEST_LEN'])
        request = forward_request.decode('utf-8')

        print(request)

        # Check if theres a response in the cache for the specified request 
        # cachedResponse = self.cache.cache(request)

        # split the request into sections
        lines = request.split('\r\n')

        # determine whether HTTPS or HTTP
        secure = False
        if lines[0].startswith("CONNECT"):
            secure = True

        for i in range(0,len(lines)):
            if lines[i][:4] == "Host" :
                index = i
                break
        
        host = lines[index][6:]
        first_line = lines[0]

        # get the url
        try :
            url = first_line.split(' ')[1]
        except IndexError :
            url = ""

        # find pos of ://
        http_pos = url.find("://")
        if (http_pos==-1):
            temp = url
        else:
            # get the main url
            temp = url[(http_pos+3):]

        port_pos = temp.find(":") # find the port pos (if any)

        # find end of web server before routes
        server_pos = temp.find("/")
        if server_pos == -1 and port_pos == -1:
            server_pos = len(temp)
        elif server_pos == -1 and port_pos != -1:
            server_pos = port_pos

        server = ""
        port = -1
        if ((port_pos==-1 or server_pos < port_pos) and not(secure)): 

            # set default port 
            port = 80 
            server = temp[:server_pos] 

        elif ((port_pos==-1 or server_pos < port_pos) and secure): 

            # set default port 
            port = 443 
            server = temp[:server_pos] 

        else: 
        
            # specified port 
            port = int(temp[(port_pos+1):])
            server = temp[:port_pos]

        if secure:
            connection = self.forward(client_sock, client_address, port, server, forward_request, host)
        else:
            connection = self.forward(client_sock, client_address, port, server, forward_request, host)


    def forward(self, client_sock, client_address, port, server, fr, host):

        try:
            try:
                # Create a default TCP socket with set timeout
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(config['CONNECTION_TIMEOUT'])
                
                # Connect to the server
                s.connect((server, port))

                # Forward the request to the websever
                s.sendall(fr)
                while 1:
                    rep = s.recv(config['MAX_REQUEST_LEN'])
                    if(len(rep) <= 0):
                        break
                    client_sock.sendall(rep)
                s.close()
                client_sock.close()

            except socket.error as error_msg:
                if s:
                    s.close()
                if client_sock:
                    client_sock.close()
        except KeyboardInterrupt:
            if s:
                s.close()
            if client_sock:
                client_sock.close()

    def handleKill(self, signum, frame):
        choice = self.MC.getChoice()
        if choice == "1":
            yes = self.MC.ensure()
            if yes == "Y" or yes == "y":
                self.shutdown()

    def shutdown(self):
        #handle the shutdonw of the server
        self.MC.end()
        self.serverSocket.close()
        sys.exit(0)

if __name__ == '__main__':
    myServer = Server()
    myServer.begin()