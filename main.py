from tkinter import filedialog as fd
import crypto.crypto as crypto
import eel

# initialyze program
eel.init("web")

# main funcions
@eel.expose
def get_proba():
    return "proba"

@eel.expose
def send_proba(msg):
    print(msg)

@eel.expose
def open_file_dialog():
    filename = fd.askopenfilename()
    print(filename)

@eel.expose
def encode(method:str, password:str, source_file_path:str, destination_file_path:str):
    cr = crypto.Crypto(method, password)
    cr.encrypt_file(source_file_path, destination_file_path)

@eel.expose
def decode(method:str, password:str, source_file_path:str, destination_file_path:str):
    cr = crypto.Crypto(method, password)
    cr.encrypt_file(source_file_path, destination_file_path)

# main window
eel.start("index.html", size=(800, 600))