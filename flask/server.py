from flask import Flask, request, render_template, jsonify, session, g
from subprocess import PIPE, run
import requests
import subprocess
import os
import time
from werkzeug.utils import secure_filename
import threading
from waitress import serve
from flask_cors import CORS

UPLOAD_FOLDER = '/tmp'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    #return render_template('index.html', val="")
    return "HELLO ONLINE COMPILER! Now we have /task POST and GET."

@app.route("/task", methods=['GET','POST'])
def task():
    taskID = ''
    taskFolder = ''
    filename = ''

    try:
        os.makedirs(UPLOAD_FOLDER)
    except FileExistsError:
        pass
    name = ''
    
    if request.method == 'POST':
        if 'file' in request.files:
            f = request.files['file']
            if not f:
                print("file is empty")
                return render_template('index.html', val={"Please insert the file"})
                name = ""
            else:
                filename = secure_filename(f.filename)
                taskID = str(time.time())
                taskFolder = app.config['UPLOAD_FOLDER'] + '/' + taskID
                try:
                    os.makedirs(taskFolder)
                except FileExistsError:
                    pass
                f.save(os.path.join(taskFolder, filename))
                name = filename
        else:
            name = ""
        print(name)
        
        process(filename, taskFolder)

        # /tmp/taskID/<input_filename>.pragmas is the list of directives
        pragmaDict = {}
        # /tmp/taskID/<input_filename>.DIRECTIVE_INDEX.dot/svg/png is the graph, such as foo.c.parallel_3.dot
        # prepare for info.file.response @ReactJS
        return taskID

    elif request.method == 'GET':
        # get data path, by passing parameters
        content = request.args.get('content')
        taskID = request.args.get('tid')
        fileName = request.args.get('fn')
        filePath = "/tmp/" + taskID + "/" + fileName
        # get file content
        if content == 'pragmas':
            result = open(filePath + '.pragmas').read()
        # returning list
            return jsonify(result)


def process(filename, taskFolder):
    # call ompparser to generate a term list of OpenMP directives
    cmd_list = [
        "./check.sh " + taskFolder + '/' + filename,
    ]
    for cmd in cmd_list:
        arr = cmd.split()
        with open(os.path.join(taskFolder, "raw_output.txt"), "w") as file:
            run(arr, stdout=file, stderr=file, universal_newlines=True)

    # call ompparser to generate a list of DOT graph files

    # return True if success, otherwise False
    return True


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
