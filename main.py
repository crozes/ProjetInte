#!/usr/bin/env python2.7

from flask import Flask, request
from flask_cors import CORS
import random
import json

app = Flask(__name__)
app.debug = True
CORS(app)

@app.route("/")
def getHelloWord():
    print("hello word")
    return "hello word"

if __name__ == "__main__":
    app.run()