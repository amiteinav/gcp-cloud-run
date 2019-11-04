import os, shutil, requests, tempfile, random, subprocess

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
    gcsfile=bucket + 'pic-crop.jpg'

    left=320.0
    top=392.0
    right=960.0
    bottom=1103.0
    
    if request.method == 'GET':
        url = request.args.get('url', type=str)

        if not url:
            return render_template('index.html')
        
        response = requests.get(url, stream=True)
        with open(inputfile, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        
        file.close()

        left = request.args.get('left', type=str)
        top = request.args.get('top', type=str)
        right = request.args.get('right', type=str)
        bottom = request.args.get('bottom', type=str)

    command = 'python local_crop.py -i ' + inputfile + ' -o ' + outputfile + ' -l ' + left + ' -t ' + top + ' -r ' + right +  ' -b ' + bottom
    string = command + '\n'
    #command = 'python local_crop.py -i ' + inputfile + ' -o ' + outputfile + ' -l ' + str(300) + ' -t ' + str(352) + ' -r ' + str(760) +  ' -b ' + str(1100)

    call('%s' % (command),shell=True)

    command = 'gsutil cp ' + outputfile + ' ' + gcsfile
    call('%s' % (command), shell=True)

    #string='top:' + top  + ' right:' + right + ' left:' + left +   + ' bottom:' + bottom
    #return string
    #return result

    return send_file(outputfile, mimetype='image/jpg')


if __name__ == "__main__":
    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    http_server.serve_forever()
