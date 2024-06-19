from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def clicked():
    print("clicked")


def window():
    #creating some of the windows for the program
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 1300, 760)
    win.setWindowTitle("RagnaCrox-MangaDownloader")

    #adding labels
    label = QtWidgets.QLabel(win)
    label.setText("FirstLabel")
    label.move(50,50)

    #adding buttons
    b1 = QtWidgets.QPushButton(win)
    b1.setText("cliqueame")
    b1.clicked.connect(clicked)


    win.show()
    sys.exit(app.exec_())

window()
