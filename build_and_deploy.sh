#!/bin/sh

number=$RANDOM

echo "build"
docker build . -t gcr.io/app-immersion-2019-a4242/cropper:${number}

echo "push"
docker push gcr.io/app-immersion-2019-a4242/cropper:${number}

echo "deploy to cloud run"
gcloud beta run deploy cropper --image gcr.io/app-immersion-2019-a4242/cropper:${number} --platform managed --region us-central1 --project app-immersion-2019-a4242

gsutil rm gs://app-imm-bucket-out/amit-profile-pic-2.jpg

gsutil ls gs://app-imm-bucket-out

curl `gcloud beta run  services list --platform managed --project  app-immersion-2019-a4242 |grep cropper | awk '{print $4}'`

#curl "https://cropper-rjxrs4o6dq-uc.a.run.app?url=https://storage.googleapis.com/cloud-run-bucket/amit-profile-pic.jpg&xmin=10&ymin=10&&ymax=100"

sleep 1

gsutil ls gs://app-imm-bucket-out 

#gcloud logging read --project app-immersion-2019-a4242  "resource.type=cloud_run_revision AND resource.labels.service_name=cropper" --limit 3
