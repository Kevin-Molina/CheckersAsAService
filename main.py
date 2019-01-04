from Server.server import Server

SERVER_IP = 'localhost'
SERVER_PORT = 6789
LOGFILE = "log.txt"
Server = Server(SERVER_IP, SERVER_PORT, LOGFILE)
Server.listen()
