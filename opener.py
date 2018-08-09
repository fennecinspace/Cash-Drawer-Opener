import sys, os, serial, threading
from PyQt5 import QtWidgets
from pynput.keyboard import Key, Listener

BASE_DIR = sys.path[0]
COMBINATION = (Key.shift, Key.ctrl)
COM = None
CODE = None
DEVICE = None
config = open(os.path.join(BASE_DIR, 'info.conf'), 'r')

for line in config.read().split('\n'):
    if "PORT" in line.strip().upper():
        COM = line.strip()[-4:]
    if "CODES" in line.strip().upper():
        codes_list = eval(line.strip()[-17:])
        CODE = chr(codes_list[0])
        for code in codes_list[1:]:
            CODE += chr(code)

try:
    DEVICE = serial.Serial(port = COM)
except:
    print('Could not Open Device')

def open_cash_drawer():
    try:
        DEVICE.write(CODE)
    except: 
        print('Error')

class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.button = QtWidgets.QPushButton('Open')
        self.button.clicked.connect(open_cash_drawer)
        self.label = QtWidgets.QLabel()
        self.label.setText('Port : ' + COM) 
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)


def on_press(key):
    if key in COMBINATION:
        pressed.add(key)
        if all(k in pressed for k in COMBINATION):
            open_cash_drawer()

def on_release(key):
    try:
        pressed.clear()
    except KeyError:
        pass


def create_listener():
    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()

### Execution
if __name__ == '__main__':
    pressed = set()
    key_thread = threading.Thread(target = create_listener, daemon = True)
    key_thread.start()

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('Cash Drawer Opener')
    window.setFixedSize(200,70)
    window.show()
    sys.exit(app.exec_())




