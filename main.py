import sys
import os

from PyQt5.uic import loadUi
from PyQt5.QtCore import QObject, QThread, Qt
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QIcon

import pyautogui
import keyboard

pyautogui.FAILSAFE = False
# Helper function to send folder file's path when the .exe is built
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Worker class that runs scroller loop and will run on a background thread
class Worker(QObject):

    def __init__(self, key1, key2, parent=None):
        QObject.__init__(self, parent=parent)
        self.key1 = key1
        self.key2 = key2
        self.active = True

    def do_work(self):
        speed = 0 #Scolls up if the value in positive and down if value is negative

        while self.active:
            if keyboard.is_pressed(self.key1):
                speed += 2
            elif keyboard.is_pressed(self.key2):
                speed -= 2

            pyautogui.scroll(speed)

    def stop(self):
        self.active = False

class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi(resource_path("main.ui"), self)

        self.setFixedSize(200, 200)
        self.setWindowIcon(QIcon(resource_path('icon.png')))
        self.setWindowTitle('Key Scroller')
        self.initUI()
        
        self.isRunning = False # Bool that will work as a on/off switch
        self.key1 = ''
        self.key2 = ''

    def initUI(self):
        # Setup window flags
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        # Setup input fields
        self.field1.setMaxLength(1)
        self.field2.setMaxLength(1)
        self.field1.textEdited.connect(self.checkFields)
        self.field2.textEdited.connect(self.checkFields)

        # Disable button if input fields are empty
        self.btn.setDisabled(True)

    def checkFields(self):
        # Checks if both input fields are not empty and not the same
        self.key1 = str(self.field1.text())
        self.key2 = str(self.field2.text())
        notEqual = self.key1 != self.key2

        if self.key1 and self.key2 and notEqual:
            self.btn.setDisabled(False)
            self.btn.clicked.connect(self.updateButtonState)
        else:
            self.btn.setDisabled(True)

    def updateButtonState(self):
        # When button is clicked starts/stops thread and change button text.
        if not self.isRunning:
            self.isRunning = True
            self.updateFields()    
            self.btn.setText('PAUSE')

            self.startThread()
        else:
            self.isRunning = False
            self.updateFields()
            self.btn.setText('START')
            
            self.stopThread()

    def updateFields(self):
        # Disable fields when thread is started
        if self.isRunning:
            self.field1.setDisabled(True)
            self.field2.setDisabled(True)
        else:
            self.field1.setDisabled(False)
            self.field2.setDisabled(False)

    def startThread(self):
        self.thread = QThread()
        self.worker = Worker(self.key1, self.key2)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.do_work)
        self.thread.start()
    
    def stopThread(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainScreen()

    main.show()

    sys.exit(app.exec_())