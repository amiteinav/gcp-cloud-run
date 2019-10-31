#!/usr/bin/python

import  random, os, sys, urllib2, json, random, getopt, base64, csv, datetime, subprocess
from PIL import Image

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


if __name__ == "__main__":
	script_name=sys.argv[0]
	arguments = len(sys.argv) - 1

	main(sys.argv[1:])