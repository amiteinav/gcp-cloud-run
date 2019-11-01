#!/usr/bin/python

import  random, os, sys, urllib2, json, random, getopt, base64, csv, datetime, subprocess
from PIL import Image
from google.cloud import storage


def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """

    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)

def main(argv):

    imgfilepath="amit-profile-pic.jpg"
    outfile="amit-profile-pic-cropped.jpg"
    xmin=10
    ymin=10
    xmax=100
    ymax=100

    try:
        #opts, args = getopt.getopt(argv,"x:e:d:",["xml-file=","xml-dir=","images-dir="])
        opts, args = getopt.getopt(argv,"i:o:w:x:y:z:",["input-file","output-file","xmax","xmin","ymax","ymin"])
    except getopt.GetoptError:
        sys.exit(42)
    for opt, arg in opts:
        if opt in ("-i", "--input-file"):
            imgfilepath = arg
        elif opt in ("-o","--output-file"):
            outfile=arg
        elif opt in ("-x", "--xmax"):
            xmax = arg
        elif opt in ("-y", "--ymax"):
            ymax = arg
        elif opt in ("-w","--xmin"):
            xmin = arg
        elif opt in ("-z","--ymin"):
            ymin = arg
        

    coords=(float(xmin),float(ymin),float(xmax),float(ymax))
    crop(imgfilepath, coords, outfile)

if __name__ == "__main__":
	script_name=sys.argv[0]
	arguments = len(sys.argv) - 1

	main(sys.argv[1:])