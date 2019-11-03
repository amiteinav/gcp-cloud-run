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
    inputfile='amit-profile-pic.jpg'
    outputfile='amit-profile-pic-crop.jpg'
    gcsfile=bucket + outputfile

    xmax=0.0
    xmin=5.0
    ymax=10.0
    ymin=15.0

    print ('now cropping')

    command = 'python local_crop.py -i ' + inputfile + ' -o ' + outputfile + ' -l ' +str(xmax) + ' -r ' + str(xmin) + ' -u ' + str(ymax) +  ' -w ' + str(ymin)
    call('%s' % (command),shell=True)

    print ('now uploading')
    command = 'gsutil cp ' + outputfile + ' ' + gcsfile
    call('%s' % (command), shell=True)

    return "\ndone\n"
    
if __name__ == "__main__":
    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    http_server.serve_forever()
