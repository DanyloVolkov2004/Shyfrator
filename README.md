# CipherTool

## Table of contents
* [Installation](#installation)
* [Launch the program](#launch-the-program)
* [Tree](#tree)

## Installation:
```
git clone https://github.com/DanyloVolkov2004/Shyfrator.git
```

```
cd Shyfrator
```

```
pip install -r requirements.txt
```

## Launch the program:
```
python main.py
```

## Tree:
```bash
CipherTool
├── .gitignore                         # git ignore file
├── crypto                             # chiper scripts...
│   ├── ciphers.py
│   ├── crypto.py
│   ├── exceptions.py
│   └── __init__.py
│   
├── main.py                             # main file, in which we write all general functions for backend and connect backend with frontend
├── README.md
├── requirements.txt
├── tmp                                 # folder for temporary files
└── web
    ├── css
    │   └── style.css                   # file, in which we write our styles for main page
    ├── img                             # folder for images
    │   ├── back_btn.png
    │   ├── folder.png
    │   ├── gear.png
    │   ├── livo.png
    │   └── pravo.png
    ├── index.html                      # main page, in which we show contetn of program
    ├── js
    │   └── scripts.js                  # file, in which we write frontend code and connect frontend with backend
    └── test.html                       # just test html file   
```
