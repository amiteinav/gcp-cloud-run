#!/bin/sh


echo "build"
docker build . -t gcr.io/app-immersion-2019-a4242/cropper

echo "push"
docker push gcr.io/app-immersion-2019-a4242/cropper

echo "deploy to cloud run"
gcloud beta run deploy cropper --image gcr.io/app-immersion-2019-a4242/cropper:latest --platform managed --region us-central1 --project app-immersion-2019-a4242

curl "https://cropper-rjxrs4o6dq-uc.a.run.app?url=https://storage.googleapis.com/cloud-run-bucket/amit-profile-pic.jpg&xmin=10&ymin=10&&ymax=100"

sleep 7

gcloud logging read --project app-immersion-2019-a4242  "resource.type=cloud_run_revision AND resource.labels.service_name=cropper" --limit 4
