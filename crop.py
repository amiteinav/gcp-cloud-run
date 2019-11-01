import os, shutil, requests, tempfile, random

from gevent.pywsgi import WSGIServer
from flask import Flask, after_this_request, render_template, request, send_file
from subprocess import call
from PIL import Image
from google.cloud import storage

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'bmp'])

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def api():
    
    gcsfile='gs://app-imm-bucket-out/amit-profile-pic-2.jpg'
    file_name='amit-profile-pic.jpg'

    call('gsutil cp %s %s' % (file_name, gcsfile), shell=True)

    #upload_blob(bucket_name, 'amit-profile-pic.jpg', 'amit-profile-pic.jpg')
    
    #crop(input_file_path, coords, output_file_path)

    return "done"
    
if __name__ == "__main__":
    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    http_server.serve_forever()
