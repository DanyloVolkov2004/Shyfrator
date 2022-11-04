from tkinter import filedialog as fd
import crypto.crypto as crypto
import shutil
import eel
import os

# global variables
tmp_path = os.path.join(os.getcwd(), "tmp/")
tmp_destination_file_path = None
source_file_path = ()
source_file_path_to_save = ()
method = None
password = None

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
def get_file_path():
    global source_file_path
    source_file_path = fd.askopenfilename()

@eel.expose
def save_file_to():
    global source_file_path_to_save
    source_file_path_to_save = fd.asksaveasfilename()

    print(tmp_destination_file_path, source_file_path_to_save)
    # stop function if source file to save is not exists
    if not os.path.exists(str(source_file_path_to_save)):
        return 0
    print(tmp_destination_file_path, source_file_path_to_save)

    # stop function if encoded file is not exists
    if not os.path.exists(tmp_destination_file_path):
        return 0
    shutil.copy(tmp_destination_file_path, source_file_path_to_save)
    print(tmp_destination_file_path, source_file_path_to_save)
    

@eel.expose
def get_method(method_from_js:str):
    global method
    if method_from_js == "Null":
        method = None
    else:
        method = method_from_js

@eel.expose
def get_password(password_from_js:str):
    global password
    if len(password_from_js) < 8:
        password = None
    else:
        password = password_from_js

@eel.expose
def encode():
    global tmp_path
    global tmp_destination_file_path
    # stop function if method is None
    if method == None:
        return 0

    # stop function if password is < than 8
    if password == None:
        return 0

    # stop function if source file is not exists
    if not os.path.exists(str(source_file_path)):
        return 0
    filename = os.path.basename(source_file_path)

    # create tmp folder if not exists
    if not os.path.exists(tmp_path):
        tmp_path = os.mkdir(os.path.join(os.getcwd(), "tmp/"))
    tmp_destination_file_path = os.path.join(tmp_path, filename)

    # start encoding
    cr = crypto.Crypto(method, password)
    cr.encrypt_file(source_file_path, tmp_destination_file_path)

@eel.expose
def decode():
    filename = os.path.basename(source_file_path)
    destination_file_path = "tmp/" + filename
    cr = crypto.Crypto(method, password)
    cr.decrypt_file(source_file_path, destination_file_path)

# main window
eel.start("index.html", size=(800, 600))

# show another window
# eel.show("test.html")