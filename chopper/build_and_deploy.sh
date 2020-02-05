#!/bin/sh

number=$RANDOM
project=`gcloud config get-value project`
bucket=app-imm-bucket-out

echo "project is $project"

echo "build . -t gcr.io/${project}/cropper:${number}"
docker build . -t gcr.io/${project}/cropper:${number}

echo "docker push gcr.io/${project}/cropper:${number}"
docker push gcr.io/${project}/cropper:${number}

echo "gcloud beta run deploy cropper --image gcr.io/${project}/cropper:${number} --platform managed --allow-unauthenticated --region us-central1 --project ${project}"
gcloud beta run deploy cropper --image gcr.io/${project}/cropper:${number} --platform managed --allow-unauthenticated --region us-central1 --project ${project}

URL=`gcloud beta run  services list --platform managed --project ${project} | grep cropper | awk '{print $4}'`

#URL=${URL}"?url=https://storage.googleapis.com/app-imm-bucket-in/amit-profile-pic.jpg&top=352&right=760&left=300&bottom=1101"
URL=${URL}"?url=https://upload.wikimedia.org/wikipedia/commons/d/da/Guido-portrait-2014.jpg&top=300&right=1100&left=300&bottom=1100"

echo "curl $URL"
curl $URL

gsutil ls -l gs://${bucket} 
