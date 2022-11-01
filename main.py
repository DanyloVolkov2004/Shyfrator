from tkinter import filedialog as fd
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

def open_file_dialog():
    filename = fd.askopenfilename()
    print(filename)

# main window
eel.start("index.html", size=(800, 600))