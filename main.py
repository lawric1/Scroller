import sys

from PyQt5.uic import loadUi
from PyQt5.QtCore import QObject, QThread, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QIcon

import pyautogui
import keyboard

# Worker class that runs scroller loop and will run on a background thread
class Worker(QObject):

    def __init__(self, key1="z", key2="x", parent=None):
        QObject.__init__(self, parent=parent)
        self.key1 = key1
        self.key2 = key2

    def do_work(self):
        speed = 0 #Scolls up if the value in positie and down if value is negative

        while True:
            if keyboard.is_pressed(self.key1):
                speed += 3
            elif keyboard.is_pressed(self.key2):
                speed -= 3
                
            pyautogui.scroll(speed)

    # def stop(self):
    #     print("stopped")
    #     self.deleteLater()

class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("main.ui", self)
        

        self.initUI()

    def initUI(self):
        # Setup window flags
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        # Setup input fields
        self.field1.setMaxLength(1)
        self.field2.setMaxLength(1)
        # updateButton function will enable the start button
        self.field1.textEdited.connect(self.updateButton)
        self.field2.textEdited.connect(self.updateButton)

        self.startBtn.setDisabled(True)

    def updateButton(self):
        # Checks if both input fields are not empty
        f1 = str(self.field1.text())
        f2 = str(self.field2.text())

        if f1 and f2:
            self.startBtn.setDisabled(False)
            self.connect_to_thread(f1, f2) # Create and connect background thread to start button
        else:
            self.startBtn.setDisabled(True)

    def connect_to_thread(self, key1, key2):
        self.thread = QThread()
        self.worker = Worker(key1, key2)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.do_work)
        # self.thread.finished.connect(self.worker.stop)

        self.startBtn.clicked.connect(self.thread.start)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainScreen()
    main.setFixedSize(200, 200)
    main.setWindowIcon(QIcon('icon.png'))
    main.setWindowTitle('Key Scroller')
    main.show()

    sys.exit(app.exec_())