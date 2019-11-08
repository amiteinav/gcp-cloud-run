#!/bin/bash

project=`gcloud config get-value project`
echo "using project $project"

trackingfile=/tmp/trackingfile$$
echo "Logging in $trackingfile..."

echo "CTRL+C to stop"

URL=`gcloud beta run  services list --platform managed --project ${project} | grep cropper | awk '{print $4}'`
URL=${URL}"?url=https://upload.wikimedia.org/wikipedia/commons/d/da/Guido-portrait-2014.jpg&top=300&right=1100&left=300&bottom=1100"

index=1000000

#curl -o /dev/null -s -w 'Total time: %{time_total}s\n' $URL >> $trackingfile &

function perf {
  curl -o /dev/null -s -w "%{time_connect} + %{time_starttransfer} = %{time_total}\n" "$1" >> $trackingfile &
}

while [ $index -gt 0 ] ; do

    perf $URL 


index=$((index-1))
done