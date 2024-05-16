# Tasky
Task management app in Python

## Installation

- Install backend dependencies,
```sh
$ git checkout backend
$ pip install -r requirements.txt
```

- Install frontend dependencies,
```sh
$ git checkout front
$ pip install -r requirements.txt
```

## Usage

In one terminal tab, execute the server 
```sh
$ git checkout backend
$ uvicorn main:app
```

In another tab, execute the gui,
```sh
$ git checkout frontend
$ python3 app.py
```
