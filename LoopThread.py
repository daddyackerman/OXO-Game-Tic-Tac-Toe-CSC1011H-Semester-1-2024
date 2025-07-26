# Author: Radhiya Isaacs
# Project: OXO Game – CSC1011H Semester 1, 2024
# University: University of Cape Town (UCT)

# This code was written by me as part of a university assignment.
# It is NOT permitted to copy, reuse, or submit this code in any form, especially for academic purposes at UCT or any other institution.

# Unauthorized use or submission of this code may be considered academic misconduct and can result in disciplinary action.
# You are welcome to view and learn from this project, but please do not plagiarize.

from PyQt5.QtCore import *
from GameClient import *

class LoopThread(QThread,GameClient):

    # Define game_signal as a custom signal
    game_signal = pyqtSignal(str)
    connection_success = pyqtSignal(bool)  # New signal to indicate connection success
    def __init__(self):
        super(LoopThread, self).__init__()
        GameClient.__init__(self)
        self.board = [' '] * BOARD_SIZE

        
    def connect_server(self, server):
        while True:
            try:
                self.connect_to_server(server)
                self.connection_success.emit(True)  # Emit signal for successful connection
            except:
                t = 'Error connecting to server!'
                self.connection_success.emit(False)  # Emit False for connection failure
                self.game_signal.emit(str(t))
                break
                    
    def run(self):
        while True:
            try:
                message = self.receive_message()
                if len(message):
                    message_parts = message.split()
                    if message_parts[0] == 'play_again':
                        self.handle_play_again_message(message_parts)
                    else:
                        self.game_signal.emit(str(message))
                else:
                    break  # No more messages, break the loop
            except:
                t = 'Error'       
            

    def move(self, position): # method to send and recieve moves
        while True:
            try:
                self.send_message(str(position))
                break
            except Exception as e:
                self.game_signal.emit(f"Move failed: {e}")

    

    