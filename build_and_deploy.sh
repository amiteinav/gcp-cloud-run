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

echo "gsutil rm gs://${bucket}/amit-profile-pic-crop.jpg"
gsutil rm gs://${bucket}/amit-profile-pic-crop.jpg

echo "gsutil ls gs://${bucket}"
gsutil ls gs://${bucket}

URL=`gcloud beta run  services list --platform managed --project ${project} | grep cropper | awk '{print $4}'`
echo "curl $URL"

curl $URL

#curl "https://cropper-rjxrs4o6dq-uc.a.run.app?url=https://storage.googleapis.com/cloud-run-bucket/amit-profile-pic.jpg&xmin=10&ymin=10&&ymax=100"

sleep 1

gsutil ls gs://${bucket} 

#gcloud logging read --project ${project}  "resource.type=cloud_run_revision AND resource.labels.service_name=cropper" --limit 3
