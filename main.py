import eel
import crypto.crypto as crypto

# initialyze program
eel.init("web")

# main funcions
@eel.expose
def get_proba():
    return "proba"

@eel.expose
def send_proba(msg):
    print(msg)

# main window
eel.start('index.html')