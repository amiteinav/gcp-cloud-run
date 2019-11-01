import os, shutil, requests, tempfile, random

from gevent.pywsgi import WSGIServer
from flask import Flask, after_this_request, render_template, request, send_file
from subprocess import call
from PIL import Image
from google.cloud import storage

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'bmp'])

app = Flask(__name__)

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

# Convert using Libre Office
def convert_file(output_dir, input_file):
    call('libreoffice --headless --convert-to pdf --outdir %s %s ' %
         (output_dir, input_file), shell=True)

def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image

    input_file is image_path
    saved_location is output_dir
    """

    # Converting image from png to jpg
    #im = Image.open(image_path)
    #rgb_im = im.convert('RGB')
    #rgb_im.save(image_path)

    #Image.open(image_path).convert('RGB').save(image_path)

    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])

def api():
    
    bucket_name='app-imm-bucket-out'
    upload_blob(bucket_name, 'amit-profile-pic.jpg', 'amit-profile-pic.jpg')

    exit

    work_dir = tempfile.TemporaryDirectory()
    file_name = 'document'
    input_file_path = os.path.join(work_dir.name, file_name)
    random_string=str(random.randint(1,9223372036854775807))
    output_file_path = os.path.join(work_dir.name, file_name + random_string + '.jpg')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file provided'
        file = request.files['file']
        if file.filename == '':
            return 'No file provided'
        if file and allowed_file(file.filename):
            file.save(input_file_path)

    if request.method == 'GET':

        url = request.args.get('url', type=str)
        if not url:
            return render_template('index.html')
        xmin = request.args.get('xmin', type=int)
        ymin = request.args.get('ymin', type=int)
        xmax = request.args.get('xmax', type=int)
        ymax = request.args.get('ymax', type=int)

        #coords=(float(xmin),float(ymin),float(xmax),float(ymax))

        # Download from URL
        response = requests.get(url, stream=True)

        with open(input_file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response

    

    #crop(input_file_path, coords, output_file_path)

    @after_this_request
    def cleanup(response):
        work_dir.cleanup()
        return response
 
    return send_file(output_file_path, mimetype='application/jpg')



if __name__ == "__main__":
    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    http_server.serve_forever()
