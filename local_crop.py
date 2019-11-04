#!/usr/bin/python

import  random, os, sys, json, random, getopt, base64, csv, datetime, subprocess
from PIL import Image
from google.cloud import storage

"""
Example:

python local_crop.py -l 320 -t 392 -r 960 -b 1117

"""

def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2) - left, upper, right, lower
    @param saved_location: Path to save the cropped image
    """

    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)

def main(argv):

    imgfilepath="amit-profile-pic.jpg"
    outfile="amit-profile-pic-cropped.jpg"

    # this is to be used when no parameters are sent
    original = Image.open(imgfilepath)
    width, height = original.size   # Get dimensions
    left = width/4
    top = height/4
    right = 3 * width/4
    bottom = 3 * height/4

    try:
        #opts, args = getopt.getopt(argv,"x:e:d:",["xml-file=","xml-dir=","images-dir="])
        opts, args = getopt.getopt(argv,"i:o:l:r:t:b:",["input-file=","output-file=","left=", "right=", "top=", "bottom="])
    except getopt.GetoptError:
        sys.exit(42)
    for opt, arg in opts:
        if opt in ("-i", "--input-file"):
            imgfilepath = arg
        elif opt in ("-o","--output-file"):
            outfile = arg
        elif opt in ("-l", "--left"):
            left = float(arg)
        elif opt in ("-r", "--right"):
            right = float(arg)
        elif opt in ("-u","--top"):
            top = float(arg)
        elif opt in ("-w","--bottom"):
            bottom = float(arg)
    

    coords=(float(left), float(top), float(right), float(bottom))
    print (coords)
    crop(imgfilepath, coords, outfile)

if __name__ == "__main__":
	script_name=sys.argv[0]
	arguments = len(sys.argv) - 1

	main(sys.argv[1:])