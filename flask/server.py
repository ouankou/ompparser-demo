import flask
from flask import Flask, request, render_template, jsonify
from subprocess import PIPE, run
import requests
import subprocess
import os
import json
import time
from werkzeug.utils import secure_filename
import threading

UPLOAD_FOLDER = '/tmp'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html', val="")


@app.route("/uploader", methods=['GET', 'POST'])
def uploader():
    try:
        os.makedirs(UPLOAD_FOLDER)
    except FileExistsError:
        pass
    name = ""
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                return render_template('index.html',
                                       val={"Please insert the file"})
                name = ""
            else:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = filename
        else:
            name = ""
        print(name)
        res = name
        print(res)
        return render_template('index.html', val=res)


@app.route('/test', methods=['GET', 'POST'])
def test():
    try:
        os.makedirs(UPLOAD_FOLDER)
    except FileExistsError:
        pass
    name = ""
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                name = ""
            else:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = f.filename
        else:
            name = ""


        cmd_list = [
            "clang-archer " + os.path.join(app.config['UPLOAD_FOLDER'], name) +
            " -o " + os.path.join(app.config['UPLOAD_FOLDER'], "myApp") +
            " -larcher",
            os.path.join(app.config['UPLOAD_FOLDER'], "myApp")
        ]
        for cmd in cmd_list:
            arr = cmd.split()
            with open(
                    os.path.join(app.config['UPLOAD_FOLDER'],
                                 "archeroutput.txt"), "w") as file:
                run(arr, stdout=file, stderr=file, universal_newlines=True)

        res_path = "python3 ArchoutputParser.py " + os.path.join(
            app.config['UPLOAD_FOLDER'], "archeroutput.txt")
        result = run(res_path.split(),
                     stdout=PIPE,
                     stderr=subprocess.STDOUT,
                     universal_newlines=True)
        if (result.returncode == 1):
            str = result.stderr
        else:
            str = result.stdout
        if not str:
            str = '{}'
        print(str)
        print(type(str))
        if request.args.get('type') == 'json':
            return flask.make_response(
                flask.jsonify({'archer': json.loads(str)}), 200)
        else:
            return render_template('index.html', val=str.split('\n'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
