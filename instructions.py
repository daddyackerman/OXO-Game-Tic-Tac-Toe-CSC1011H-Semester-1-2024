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

class Instructions(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("How to play OXO")
        self.instruct()
        self.setMaximumSize(600, 800)

    def instruct(self):
        self.setStyleSheet("background-color: pink;")

        pixmap = QPixmap("htp") 
        logo_label = QLabel()
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)  # Align the logo to the center

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 20, 20)  # Set margins around the layout

        # Fonts
        font_heading = QFont("Montserrat", 14, weight=QFont.Bold)
        font_description = QFont("Montserrat", 10)

        # Connecting
        con_label = QLabel("Connecting:")
        con_label.setFont(font_heading)
        con_description = QLabel("If you are the host: the server code is 'localhost'.\nIf you are not the host: the server code is the host IP address.\nThen press connect.")
        con_description.setFont(font_description)

        # Playing
        play_label = QLabel("Playing")
        play_label.setFont(font_heading)
        play_description = QLabel("If it is your turn simply click on the block where you wish to play.")
        play_description.setFont(font_description)

        # Winning
        win_label = QLabel("Winning")
        win_label.setFont(font_heading)
        win_description = QLabel("The winner will be declared when a player has 3 of their shapes in a row (vertically, horizontally, or diagonally).")
        win_description.setFont(font_description)

        # New Game
        newgame_label = QLabel("New Game")
        newgame_label.setFont(font_heading)
        newgame_description = QLabel("To play a new game, simply press the 'New Game' button.")
        newgame_description.setFont(font_description)

        # Other Tips
        tips_label = QLabel("Other Tips")
        tips_label.setFont(font_heading)
        tips_description = QLabel("Scores and match history are displayed on the right-hand side.")
        tips_description.setFont(font_description)

        # Add widgets to layout
        layout.addWidget(logo_label)
        layout.addWidget(con_label)
        layout.addWidget(con_description)
        layout.addWidget(play_label)
        layout.addWidget(play_description)
        layout.addWidget(win_label)
        layout.addWidget(win_description)
        layout.addWidget(newgame_label)
        layout.addWidget(newgame_description)
        layout.addWidget(tips_label)
        layout.addWidget(tips_description)
        layout.addSpacing(35)

        # Close Button
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: white;border-radius: 10px;padding: 8px;")
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.close_button.clicked.connect(self.close_clicked)

    def close_clicked(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    Instructions_window = Instructions()
    Instructions_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
