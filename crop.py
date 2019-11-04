import os, shutil, requests, tempfile, random

from gevent.pywsgi import WSGIServer
from flask import Flask, after_this_request, render_template, request, send_file
from subprocess import call
from PIL import Image
from google.cloud import storage

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def api():
    
    bucket='gs://app-imm-bucket-out/'
    inputfile='/tmp/pic.jpg'
    outputfile='/tmp/pic-crop.jpg'
    gcsfile=bucket + outputfile

    left=320.0
    top=392.0
    right=960.0
    bottom=117.0
    
    if request.method == 'GET':
        url = request.args.get('url', type=str)

        if not url:
            return render_template('index.html')
        
        response = requests.get(url, stream=True)
        with open(inputfile, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        
        
        left = request.args.get('left', type=int)
        top = request.args.get('top', type=int)
        right = request.args.get('right', type=int)
        bottom = request.args.get('bottom', type=int)

    #command ='ls -l /tmp/'
    #result=call('%s' % (command),shell=True)

    command = 'python local_crop.py -i ' + inputfile + ' -o ' + outputfile + ' -l ' +str(left) + ' -t ' + str(top) + ' -r ' + str(right) +  ' -b ' + str(bottom)
    call('%s' % (command),shell=True)

    command = 'gsutil cp ' + outputfile + ' ' + gcsfile
    call('%s' % (command), shell=True)

    return "\ndone\n"
    #return result

if __name__ == "__main__":
    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    http_server.serve_forever()
