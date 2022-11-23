from tkinter import filedialog as fd
from tkinter import Tk
import crypto
import shutil
import os

class Program:
    def __init__(self, eel):
        self.eel = eel
        self.tmp_path = os.path.join(os.getcwd(), "tmp/")
        self.tmp_destination_file_path = None
        self.encription_file_path = ()
        self.decription_file_path = ()
        self.source_file_path_to_save = ()
        self.method = None
        self.password = None
        self.fd_parent_window = Tk()
        self.fd_parent_window.wm_attributes('-topmost', 1)
        self.fd_parent_window.withdraw()

    def run(self):
        self.eel.init("web")
        self.eel.start("index.html", size=(800, 600))

    def clean(self):
        # create tmp folder if not exists
        if not os.path.exists(self.tmp_path): self.tmp_path = os.mkdir(os.path.join(os.getcwd(), "tmp/"))
        folder = "tmp/"

        # remove all files from tmp folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path): os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
    
    def get_self(self):
        return self

    def get_encription_file_path(self):
        self.encription_file_path = fd.askopenfilename(parent=self.fd_parent_window)

    def get_decription_file_path(self):
        self.decription_file_path = fd.askopenfilename(parent=self.fd_parent_window)

    def save_file_to(self):
        self.source_file_path_to_save = fd.asksaveasfilename(parent=self.fd_parent_window)

        # stop function if source file to save is not exists
        if type(self.source_file_path_to_save) == type(()): return 0

        # stop function if encoded file is not exists
        if not os.path.exists(self.tmp_destination_file_path): return 0

        shutil.copy(self.tmp_destination_file_path, self.source_file_path_to_save)
        
    def get_method(self, method:str):
        # self.method = None if (method == "Null") else method
        if method == "Null": self.method = None
        else: self.method = method

    def get_password(self, password:str):
        # self.len = None if (len(password) < 8) else password
        if len(password) < 8: self.password = None
        else: self.password = password

    def encode(self):
        # stop function if method is None
        if self.method == None: return 0

        # stop function if password is < than 8
        if self.password == None: return 0

        # stop function if source file is not exists
        if not os.path.exists(str(self.encription_file_path)): return 0
        filename = "encoded_" + os.path.basename(self.encription_file_path)

        # create tmp folder if not exists
        if not os.path.exists(self.tmp_path): self.tmp_path = os.mkdir(os.path.join(os.getcwd(), "tmp/"))
        self.tmp_destination_file_path = os.path.join(self.tmp_path, filename)

        # start encoding
        cr = crypto.Crypto(self.method, self.password)
        cr.encrypt_file(self.encription_file_path, self.tmp_destination_file_path)

    def decode(self):
        # stop function if method is None
        if self.method == None: return 0

        # stop function if password is < than 8
        if self.password == None: return 0

        # stop function if source file is not exists
        if not os.path.exists(str(self.decription_file_path)): return 0
        filename = "decoded_" + os.path.basename(self.encription_file_path)

        # create tmp folder if not exists
        if not os.path.exists(self.tmp_path): self.tmp_path = os.mkdir(os.path.join(os.getcwd(), "tmp/"))
        self.tmp_destination_file_path = os.path.join(self.tmp_path, filename)

        # start decoding
        cr = crypto.Crypto(self.method, self.password)
        cr.decrypt_file(self.decription_file_path, self.tmp_destination_file_path)