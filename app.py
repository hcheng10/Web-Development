from flask import Flask, render_template, request
from flask import redirect, url_for, abort, g

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle

import io
import base64
import web_helper

### stuff from last class
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        # if the user submits the form
        try:
            web_helper.insert_message(request)
            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.html', error=True)


@app.route('/view_messages/', methods=['POST', 'GET'])
def view_messages():
    if request.method == 'GET':
        return render_template('view_messages.html')
    else:
        try:
            out = web_helper.random_messages(request.form["number"]) # a format html script in string form
            return render_template('view_messages.html', output = out) 
        except:
            return render_template('view_messages.html', error = True)
