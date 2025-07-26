# DO NOT MODIFY THIS FILE
# This file was provided by the University of Cape Town (UCT) as part of the CSC1011H coursework.
# I do not claim authorship of this code.
# Any modifications (if any) made to this file are noted below.

# Course: CSC1011H – Semester 1, 2024
# Provided for use in the OXO Game project.

from datetime import *
from socket import *
from GameIni import *

# Basic networking and log(logfile) functionality

class GameClient:
    
    def __init__(self):
        self.log_file = open(GAME_NAME + 'GameClient.log','w')
        self.log_file.close()
        self.log(GAME_NAME + ' Game Client Started: ' + str(datetime.now()))
        self.socket = socket(AF_INET, SOCK_STREAM)
        
    def connect_to_server(self,host):
        self.socket.connect((host, PORT))
        self.log('Connected To Server: ' + str(host))
        
    def send_message(self,msg):
        self.socket.send(BUFFER_STR.format(msg).encode())
        self.log('Sent Message: ' + msg)
    
    def receive_message(self):
        msg = self.socket.recv(BUFFER_SIZE).decode().strip()
        self.log('Received Message: ' + msg)
        return msg 
        
    def log(self,msg):
        self.log_file = open(GAME_NAME + 'GameClient.log','a')
        self.log_file.write(msg + '\n')
        self.log_file.close()
        
    def __del__(self):
        self.socket.close()
        self.log(GAME_NAME + ' Game Client Ended: ' + str(datetime.now()))
