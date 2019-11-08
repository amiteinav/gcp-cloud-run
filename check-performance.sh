#!/bin/bash

project=`gcloud config get-value project`
echo "using project $project"

echo "CTRL+C to stop"

URL=`gcloud beta run  services list --platform managed --project ${project} | grep cropper | awk '{print $4}'`
URL=${URL}"?url=https://upload.wikimedia.org/wikipedia/commons/d/da/Guido-portrait-2014.jpg&top=300&right=1100&left=300&bottom=1100"


while [ 0 ] ; do
    curl $URL > /dev/null &
done