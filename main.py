import connector
import eel

# main functions
@eel.expose
def get_encription_file_path():
    app.get_encription_file_path()

@eel.expose
def get_decription_file_path():
    app.get_decription_file_path()

@eel.expose
def save_file_to():
    app.save_file_to()
    
@eel.expose
def get_method(method:str):
    app.get_method(method)

@eel.expose
def get_password(password:str):
    app.get_password(password)

@eel.expose
def encode():
    app.encode()

@eel.expose
def decode():
    app.decode()

# start
if __name__ == "__main__":
    app = connector.Program(eel)
    try: app.run()
    except (SystemExit, MemoryError): app.clean()