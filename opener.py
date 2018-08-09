import sys, os, serial, threading
from PyQt5 import QtWidgets
from pynput.keyboard import Key, Listener

BASE_DIR = sys.path[0]
COM = None
CODE = None
DEVICE = None

config = open(os.path.join(BASE_DIR, 'info.conf'), 'r')
for line in config.read().split('\n'):
    if "PORT" in line.strip().upper():
        COM = line.strip()[line.strip().upper().find('COM'):].upper()
    if "CODES" in line.strip().upper():
        codes_list = eval(line.strip()[-17:])
        CODE = chr(codes_list[0])
        for code in codes_list[1:]:
            CODE += chr(code)
config.close()
CODE = str.encode(CODE)

def open_device(com_to_open = COM):
    global DEVICE
    try:
        DEVICE = serial.Serial(port = com_to_open)
    except Exception as e:
        print('Could not Open Device :', e)

def update_new_com(new_com = COM):
    config = open(os.path.join(BASE_DIR, 'info.conf'), 'r')
    config_content = config.read().split('\n')
    config.close()
    config = open(os.path.join(BASE_DIR, 'info.conf'), 'w')
    to_write = ''
    for index, line in enumerate(config_content):
        if "PORT" in line.upper():
            to_write += 'PORT = ' + new_com
        else:
            to_write += line
        if index < len(config_content)-1:
            to_write += '\n'

    config.write(to_write)
    config.close()

def open_cash_drawer():
    global COM
    try:
        if COM != window.com_input.text().strip():
            COM = window.com_input.text().strip()
            update_new_com(COM)
        open_device(COM)
        DEVICE.write(CODE)
        DEVICE.close()
    except Exception as e: 
        print(e)
        

class Window(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.button = QtWidgets.QPushButton('Open')
        self.button.clicked.connect(open_cash_drawer)
        self.com_input = QtWidgets.QLineEdit(self)
        self.com_input.setText(COM)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.com_input)
        layout.addWidget(self.button)

        ## minimize to tray
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))
        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)
        hide_action = QtWidgets.QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


def on_press(key):
    if key == Key.f12:
        open_cash_drawer()

def on_release(key):
    None

def create_listener():
    with Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()

### Execution
if __name__ == '__main__':
    key_thread = threading.Thread(target = create_listener, daemon = True)
    key_thread.start()

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('Cash Drawer Opener')
    window.setFixedSize(200,100)
    window.show()
    sys.exit(app.exec_())


