# Author: Radhiya Isaacs
# Project: OXO Game – CSC1011H Semester 1, 2024
# University: University of Cape Town (UCT)

# This code was written by me as part of a university assignment.
# It is NOT permitted to copy, reuse, or submit this code in any form, especially for academic purposes at UCT or any other institution.

# Unauthorized use or submission of this code may be considered academic misconduct and can result in disciplinary action.
# You are welcome to view and learn from this project, but please do not plagiarize.


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from LoopThread import LoopThread
from PyQt5.QtGui import QPixmap, QIcon


class PlayAgain(QWidget):
    play_again_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Play Again?")
        self.setMaximumSize(200, 100)
        
        self.ask = QLabel("Would you like to play agin?")
        # Create buttons
        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")

        # Connect button signals
        self.yes_button.clicked.connect(self.on_yes_clicked)
        self.no_button.clicked.connect(self.on_no_clicked)

       # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.ask)
        layout.addWidget(self.yes_button)
        layout.addWidget(self.no_button)
        self.setLayout(layout)

    def on_yes_clicked(self):
        try:
            self.play_again_signal.emit("y")
        except Exception as e:
            print("Error emitting 'yes' signal:", e)
        finally:
            self.close()

    def on_no_clicked(self):
        try:
            self.play_again_signal.emit("n")
        except Exception as e:
            print("Error emitting 'no' signal:", e)
        finally:
            self.close()


class Instructions(QWidget):  # Instructions window
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("How to play OXO")
        self.instruct()
        self.setMaximumSize(600, 800)

    def instruct(self):
        self.setStyleSheet("background-color: pink;")
        pixmap = QPixmap("htp.png") 
        htp_label = QLabel()
        htp_label.setPixmap(pixmap)
        htp_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 20, 20)

        font_heading = QFont("Montserrat", 14, weight=QFont.Bold)
        font_description = QFont("Montserrat", 10)

        con_label = QLabel("Connecting:")
        con_label.setFont(font_heading)
        con_description = QLabel("If you are the host: the server code is 'localhost'.\nIf you are not the host: the server code is the host IP address.\nThen press connect.")
        con_description.setFont(font_description)

        play_label = QLabel("Playing")
        play_label.setFont(font_heading)
        play_description = QLabel("If it is your turn simply click on the block where you wish to play.")
        play_description.setFont(font_description)

        pixmap = QPixmap("map.png") 
        map_label = QLabel()
        map_label.setPixmap(pixmap)

        win_label = QLabel("Winning")
        win_label.setFont(font_heading)
        win_description = QLabel("The winner will be declared when a player has 3 of their player_icons in a row (vertically, horizontally, or diagonally).")
        win_description.setFont(font_description)

        newgame_label = QLabel("New Game")
        newgame_label.setFont(font_heading)
        newgame_description = QLabel("To play a new game, simply press the 'New Game' button.")
        newgame_description.setFont(font_description)

        tips_label = QLabel("Other Tips")
        tips_label.setFont(font_heading)
        tips_description = QLabel("Scores and match history are displayed on the right-hand side.")
        tips_description.setFont(font_description)


        layout.addWidget(htp_label)
        layout.addWidget(con_label)
        layout.addWidget(con_description)
        layout.addWidget(play_label)
        layout.addWidget(map_label)
        layout.addWidget(play_description)
        layout.addWidget(win_label)
        layout.addWidget(win_description)
        layout.addWidget(newgame_label)
        layout.addWidget(newgame_description)
        layout.addWidget(tips_label)
        layout.addWidget(tips_description)
        layout.addSpacing(35)

        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: white;border-radius: 10px;padding: 8px;")
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.close_button.clicked.connect(self.close_clicked)

    def close_clicked(self):
        self.close()

class OXO(QWidget):
    def __init__(self,parent = None):
        QWidget.__init__(self,parent)
        self.setWindowTitle("OXO Game")
        self.setGeometry(100, 100, 640, 480)

        self.play_again_window = PlayAgain()  # Initialize PlayAgain
        self.play_again_window.play_again_signal.connect(self.on_play_again_signal)
        self.play_again_window.hide()  # Hide initially

        self.player_icons = [QIcon("x.png"), QIcon("o.png")]
        # Player shape
        self.player_icon = None
        
        self.background_label = QLabel(self) 
        self.background_label.setGeometry(0, 0, 640, 480)  

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 640, 480)
        self.setBackgroundImage("bg.png")
        self.thread = LoopThread()
        self.thread.connection_success.connect(self.on_connection_success)
        
        
        # Setting game logo
        pixmap = QPixmap("logo") 
        logo_label = QLabel()
        logo_label.setPixmap(pixmap) 
        
        # Connection Bar
        connection_layout = QHBoxLayout()
        self.server_label = QLabel("Server code:")
        self.server_label.setStyleSheet("color: white;background-color: #602060;padding: 8px;") 
        self.server_lineedit = QLineEdit()
        self.server_lineedit.setPlaceholderText("localhost")
        self.server_lineedit.setStyleSheet("padding: 8px;")
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet("color: white;background-color: #602060;padding: 11px;")
        
        
        self.connect_btn.clicked.connect(self.connect)
        self.thread.game_signal.connect(self.LoopThread_thing_msg)

        self.enable_signal()


        connection_layout.addWidget(self.server_label)
        connection_layout.addWidget(self.server_lineedit)
        connection_layout.addWidget(self.connect_btn)        
        connection_layout.setSpacing(0) 
        
        # Creating Game board
        gridboard_widget = QWidget()
        self.gridboard = QGridLayout(gridboard_widget)
        self.gridboard.setSpacing(0)

        # Creaating buttons for board
        self.button_0 = QPushButton()
        self.button_1 = QPushButton()
        self.button_2 = QPushButton()
        self.button_3 = QPushButton()
        self.button_4 = QPushButton()
        self.button_5 = QPushButton()
        self.button_6 = QPushButton()
        self.button_7 = QPushButton()
        self.button_8 = QPushButton()
        
        # Set button sizes
        self.button_0.setFixedSize(100, 100)
        self.button_1.setFixedSize(100, 100)
        self.button_2.setFixedSize(100, 100)
        self.button_3.setFixedSize(100, 100)
        self.button_4.setFixedSize(100, 100)
        self.button_5.setFixedSize(100, 100)
        self.button_6.setFixedSize(100, 100)
        self.button_7.setFixedSize(100, 100)
        self.button_8.setFixedSize(100, 100)

        # Placing buttons 
        self.board_grid = QGridLayout()
        self.board_grid.addWidget(self.button_0,0,0)
        self.board_grid.addWidget(self.button_1,0,1)
        self.board_grid.addWidget(self.button_2,0,2)
        self.board_grid.addWidget(self.button_3,1,0)
        self.board_grid.addWidget(self.button_4,1,1)
        self.board_grid.addWidget(self.button_5,1,2)
        self.board_grid.addWidget(self.button_6,2,0)
        self.board_grid.addWidget(self.button_7,2,1)
        self.board_grid.addWidget(self.button_8,2,2)
        self.board_grid_widget = QWidget()
        self.board_grid_widget.setLayout(self.board_grid)

        # connect board buttons to slot
        self.button_0.clicked.connect(self.button_0_clicked)
        self.button_1.clicked.connect(self.button_1_clicked)
        self.button_2.clicked.connect(self.button_2_clicked)
        self.button_3.clicked.connect(self.button_3_clicked)
        self.button_4.clicked.connect(self.button_4_clicked)
        self.button_5.clicked.connect(self.button_5_clicked)
        self.button_6.clicked.connect(self.button_6_clicked)
        self.button_7.clicked.connect(self.button_7_clicked)
        self.button_8.clicked.connect(self.button_8_clicked)  


        # Creating Instructions button
        instr_layout = QHBoxLayout()    
        self.instructions = QPushButton("Instructions")
        self.instructions.clicked.connect(self.how_to_play)
        self.instructions.setStyleSheet("font-family:'Arial Black';font-size:13px;color: white;background-color: #602060;padding: 11px;")
        instr_layout.addWidget(self.instructions)
       
        # Creating Players information section
        self.players_label = QLabel("Players")
        self.players_label.setStyleSheet("font-size: 30px;color: white;font-family:Arial Black;")  # Adjust 12pt to your desired font size
   
        self.player1_label = QLabel(" "*15 +"Your shape is :")
        self.player1_label.setStyleSheet("font-size: 14px;color: white;")  # Adjust 12pt to your desired font size
      
        self.player1_player_icon = QLabel('')
        self.player1_player_icon.setFixedSize(30, 30)  # Adjust the size of player icon
        self.player1_player_icon.setScaledContents(True)  # Allow the icon to scale
        self.player2_label = QLabel(" "*15 + "Opponent shape is :")
        self.player2_label.setStyleSheet("color: white;font-size:14px;")
        self.player2_player_icon = QLabel('')
        self.player2_player_icon.setFixedSize(30, 30)  # Adjust the size of player icon
        self.player2_player_icon.setScaledContents(True)  # Allow the icon to scale
        
        # Creating new game button
        self.new_game_btn = QPushButton(" "+"Play again"+" ")
        self.new_game_btn.setStyleSheet("font-family:'Arial Black';font-size:13px;color: white;background-color: #602060;padding: 9px;")
        self.new_game_btn.clicked.connect(self.new_game) 
        
        # Creating exit button
        self.exit_button = QPushButton(" "*12+"Exit"+" "*12)
        self.exit_button.setStyleSheet("font-family:'Arial Black';font-size:13px;color: white;background-color: #602060;padding: 9px;")
        self.exit_button.clicked.connect(self.quit)
        
        # Creating History section to view server messages 
        self.history_label = QLabel("History")
        self.history_label.setStyleSheet("font-size: 30px;color: white;font-family:Arial Black;") 
        self.history = QTextEdit()
        self.history.setReadOnly(True)  
        self.history.setWordWrapMode(QTextOption.WordWrap)  
        self.history.setMinimumSize(500, 250)  
        font1 = self.history.font()
        font1.setPointSize(12)
        self.history.setFont(font1)
        
        grid = QGridLayout()
        grid.addWidget(self.players_label, 0,1)  
        grid.addWidget(self.player1_label, 1, 0)
        grid.addWidget(self.player1_player_icon, 1, 1)
        grid.addWidget(self.player2_label, 2, 0)
        grid.addWidget(self.player2_player_icon, 2, 1)
        grid.addWidget(self.history_label, 3,1,1,1) 
        grid.addWidget(self.history, 4,0,1,3)  

        vertical_spacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vertical_spacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid.addItem(vertical_spacer1, 5, 0)
        grid.addItem(vertical_spacer2, 6, 0)
        grid.addWidget(self.new_game_btn, 10, 0)
        grid.addWidget(self.exit_button, 10, 2)
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(logo_label)
        left_layout.addLayout(connection_layout)
        left_layout.addWidget(self.board_grid_widget) 
        left_layout.addSpacing(5)
        left_layout.addLayout(instr_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  
        right_layout.setSpacing(10)  
        right_layout.addLayout(grid)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout) 
        main_layout.addSpacing(50)  
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.resizeEvent = self.onResize
        
    
    def LoopThread_thing_msg(self,message):
        # Recieve signal from the thread
        try:
            self.handle_game_signal(message)
        except Exception as e :
            print (e)
    
    def enable_signal(self):
        try:
            self.thread = LoopThread()
            self.thread.game_signal.connect(self.LoopThread_thing_msg)  # connect signals to slots    
            self.thread.start() 
        except Exception as e:
            print(e)

    # Methods to handle buttons being pressed
    def button_0_clicked(self): 
        self.thread.move(0)
        self.thread.start()
        
    def button_1_clicked(self): 
  
        self.thread.move(1)
        self.thread.start()
        
    def button_2_clicked(self): 
     
        self.thread.move(2)
        self.thread.start()
        
    def button_3_clicked(self): 

        self.thread.move(3)
        self.thread.start()
        
    def button_4_clicked(self): 
     
        self.thread.move(4)
        self.thread.start()
        
    def button_5_clicked(self): 
    
        self.thread.move(5)
        self.thread.start()
        
    def button_6_clicked(self): 

        self.thread.move(6)
        self.thread.start()
        
    def button_7_clicked(self): 
       
        self.thread.move(7)
        self.thread.start() 
    
    def button_8_clicked(self): 
    
        self.thread.move(8)
        self.thread.start()    
    

    def connect(self):
        try:
            self.server = self.server_lineedit.text().strip()
            if not self.server:
                raise ValueError("Server address cannot be empty.")
            self.thread.connect_server(self.server)
            self.thread.start()
        except Exception as e:
            print("Connection error:", e)
            QMessageBox.critical(self, "Connection Error", str(e))

    
    def on_connection_success(self, success):
        if success:
            self.connect_btn.setStyleSheet("color: white;background-color: green;padding: 11px;")
            self.connect_btn.setText("Connected")
        else:
            self.connect_btn.setStyleSheet("color: white;background-color: red;padding: 11px;")
            self.connect_btn.setText("Connection Error")

    def handle_game_signal(self, message): # Method to handle server messagees
        message_parts = message.split()

        if  message_parts[0] == 'new':
            self.history.append("----New Game has started---- ")
            self.player_icon = message_parts[-1][-1]

            if self.player_icon == "X":
                self.player_icon = self.player_icons[0]  # Assigning the icon based on the player's shape
                self.history.append("Your shape is X")
                self.player1_player_icon.setPixmap(QPixmap("x.png"))
                self.opponent_icon = "O"
                self.player2_label.setText(" " * 15 + "Opponent shape is : ")
                self.player2_player_icon.setPixmap(QPixmap("o.png"))
    
            else :
                self.player_icon = self.player_icons[1]  # Assigning the icon based on the player's shape
                self.history.append("Your shape is O")
                self.player1_player_icon.setPixmap(QPixmap("o.png"))
                self.opponent_icon = "X"
                self.player2_label.setText(" " * 15 + "Opponent shape is : ")
                self.player2_player_icon.setPixmap(QPixmap("x.png"))
           

        elif message_parts [0] =="your" :
            # enable the player to play when its their turn
            self.connect_btn.setEnabled(False)
            self.history.append(message)
            self.button_0.setEnabled(True)
            self.button_1.setEnabled(True)
            self.button_2.setEnabled(True)
            self.button_3.setEnabled(True)
            self.button_4.setEnabled(True)
            self.button_5.setEnabled(True)
            self.button_6.setEnabled(True)
            self.button_7.setEnabled(True)
            self.button_8.setEnabled(True)
    

        elif message_parts[0] == "opponents": 
            # disabled uttons if its not their turn
            self.connect_btn.setEnabled(False)
            self.history.append(message)
            self.button_0.setEnabled(False)
            self.button_1.setEnabled(False)
            self.button_2.setEnabled(False)
            self.button_3.setEnabled(False)
            self.button_4.setEnabled(False)
            self.button_5.setEnabled(False)
            self.button_6.setEnabled(False)
            self.button_7.setEnabled(False)
            self.button_8.setEnabled(False)
            
        if message_parts[0] == 'valid':  # check valid move 
            self.connect_btn.setEnabled(False)
            position = int(message_parts[-1][-1])
            player_icon = message_parts[-1][-3]

            # Map player_icon ('X' or 'O') to index (0 or 1)
            player_index = 0 if player_icon == 'X' else 1
                # Update button with player's icon
            if position == 0:
                self.button_0.setIcon(self.player_icons[player_index])
            elif position == 1:
                self.button_1.setIcon(self.player_icons[player_index])
            elif position == 2:
                self.button_2.setIcon(self.player_icons[player_index])
            elif position == 3:
                self.button_3.setIcon(self.player_icons[player_index])
            elif position == 4:
                self.button_4.setIcon(self.player_icons[player_index])
            elif position == 5:
                self.button_5.setIcon(self.player_icons[player_index])
            elif position == 6:
                self.button_6.setIcon(self.player_icons[player_index])
            elif position == 7:
                self.button_7.setIcon(self.player_icons[player_index])
            elif position == 8:
                self.button_8.setIcon(self.player_icons[player_index])

            # Set the icon size
            icon_size = QSize(100, 100)
            self.button_0.setIconSize(icon_size)
            self.button_1.setIconSize(icon_size)
            self.button_2.setIconSize(icon_size)
            self.button_3.setIconSize(icon_size)
            self.button_4.setIconSize(icon_size)
            self.button_5.setIconSize(icon_size)
            self.button_6.setIconSize(icon_size)
            self.button_7.setIconSize(icon_size)
            self.button_8.setIconSize(icon_size)

            # Append the player's icon and a message indicating a valid move to the history
            if player_icon == 'X':
                self.history.append("X played at position " + str(position) + " - Valid move")
            elif player_icon == 'O':
                self.history.append("O played at position " + str(position) + " - Valid move")         
                

        elif message_parts[0] == "invalid":  # invalid and write invalid move
            self.connect_btn.setEnabled(False)
            self.history.append(message)

        elif message_parts[0] == "game":  # check game over
            
            if message_parts[-1][-1] == 'X':
                self.history.append('Game over, the winner is X')
                
            elif message_parts [-1][-1] == 'O':
                self.history.append('Game over, the winner is O')
            else:
                self.history.append("Game over, It's a tie!")

        elif message_parts[0] == 'play':
            self.connect_btn.setEnabled(False)
            self.history.append('Would you like to play another game?')
            self.play_again_window.show()
            
        elif message_parts[0] == 'Connected':
            self.history.append(message)

    def setBackgroundImage(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap.scaled(self.size()))

    def onResize(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.setBackgroundImage("bg.png")
        self.resizeGridButtons()
        return super().resizeEvent(event) 
    
    def resizeGridButtons(self):
        bsize = min(self.width(), self.height()) // 5
        button_list = [self.button_0, self.button_1, self.button_2,
                        self.button_3, self.button_4, self.button_5,
                        self.button_6, self.button_7, self.button_8]
            
    def how_to_play(self):
        self.intruct_window =Instructions()
        self.intruct_window.show()
            
    
    def clear_board(self):
        icon =QIcon()
        icon.addPixmap(QPixmap('blank.png'))
        self.button_0.setIcon(icon)
        self.button_1.setIcon(icon)
        self.button_2.setIcon(icon)
        self.button_3.setIcon(icon)
        self.button_4.setIcon(icon)
        self.button_5.setIcon(icon)
        self.button_6.setIcon(icon)
        self.button_7.setIcon(icon)
        self.button_8.setIcon(icon)


    def on_play_again_signal(self, response):
        try:
            if response == "y":
                self.thread.send_message(response)
                self.clear_board()
        except Exception as e:
            print("Error:", e)

    def new_game(self,winner =None):
        self.play_again_window.show()
        # Clear the board buttons for a new game
        self.clear_board()

        # Enable the Connect button
        self.connect_btn.setEnabled(False)
        self.enable_signal()
    
    def quit(self): 
        self.close()


def main():

    app = QApplication(sys.argv)
    game = OXO()
    game.show()
    sys.exit(app.exec_())

main()