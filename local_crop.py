#!/usr/bin/python

import  random, os, sys, urllib2, json, random, getopt, base64, csv, datetime, subprocess
import xml.etree.ElementTree as ET

#pip install Pillow
from PIL import Image

#python /Users/amiteinav/Documents/GitHub/image-processing/cut_images_based_on_xml.py -e ${XML_PATH} -d ${IMG_PATH} -t ${TAGS}

def message(msg, level="Info"):
  logfile = '/tmp/cut_images_based_on_xml.log'
  now = datetime.datetime.now()
  time =  now.isoformat()
  str = level + "|" + time + "|" + msg + "\n"
  with open(logfile, "a") as myfile:
    myfile.write(str)
    myfile.close()
  if (level == "Error"):
    print (str)
  elif (level == "Usage"):
    print (msg)

def iterate_through_xml_dir(xmldir,imagedir,tags_dir,start_with_file_no=0):
	file_no=0
	message ('skipping {} files'.format(start_with_file_no))
	for root, dirs, files in os.walk(xmldir):  
		for file in files:
			file_no+=1
			if (file.endswith('.xml')):
				if (file_no > int(start_with_file_no)):
					message ('Now handling xml file {} number: {}'.format(file,file_no))
					xmlpath=xmldir+'/'+file
					iterate_through_xml(xmlpath,imagedir,tags_dir)

def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    print ('crop')

    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    #cropped_image.show()


def crop_image(infile,x,y,h,w,outfile):

	message('croping {} into {}'.format(infile,outfile))
	img = cv2.imread(infile)

	crop_img = img[y:y+w, x:x+h]


	message('outfile: {}'.format(outfile))
	cv2.imwrite(outfile, crop_img)

def create_dir(dir):
	if not os.path.exists(dir):
		message ('creating a new folder {}'.format(dir))
		os.makedirs(dir)


def iterate_through_xml(xmlfile,imagedir,tags_dir):

	
	ready_to_crop = False

	tree = ET.parse(xmlfile)

	for elem in tree.iter():
		message ('now dealing with {} and value {}'.format(elem.tag, elem.text.encode('utf-8')))

		if (elem.tag == 'name'):
			object_name=elem.text
		elif (elem.tag == 'xmin'):
			xmin=elem.text
		elif  (elem.tag == 'ymin'):
			ymin=elem.text
		elif  (elem.tag == 'xmax'):
			xmax=elem.text
		elif (elem.tag == 'filename'):
			imgfilename=elem.text.encode('utf-8')
			imgfilepath = imagedir + '/' + imgfilename
			message ('image path is {}'.format(imgfilepath))
			if not os.path.isfile(imgfilepath):
				message ('file {} is missing'.format(imgfilepath))

		elif  (elem.tag == 'ymax'):
			ymax=elem.text
			ready_to_crop = True

		if (ready_to_crop):
			
			random_string=str(random.randint(1,9223372036854775807))
			outdir = tags_dir + '/' + object_name 
			outfile= outdir + '/' + random_string + '.jpg' 
			create_dir(outdir)
			coords=(float(xmin),float(ymin),float(xmax),float(ymax))
			if os.path.isfile(imgfilepath):
				message ('Now cropping imagefile {} at {}, {}, {}, {} into {}'.format(imgfilepath,xmin,ymin,xmax,ymax,outfile))
				crop(imgfilepath, coords, outfile)
			ready_to_crop = False



def main(argv):

    print ('starting')

    imgfilepath="amit-profile-pic.jpg"
    outfile="amit-profile-pic-cropped.jpg"
    xmin=10
    ymin=10
    xmax=100
    ymax=100
    coords=(float(xmin),float(ymin),float(xmax),float(ymax))
    print (coords)
    crop(imgfilepath, coords, outfile)
	#iterate_through_xml_dir(xmldir,imagedir,tags_dir,skip_files)

if __name__ == "__main__":
	script_name=sys.argv[0]
	arguments = len(sys.argv) - 1

	if (arguments == 0):
		sys.exit(42)

	main(sys.argv[1:])