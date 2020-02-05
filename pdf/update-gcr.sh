#!/bin/bash

echo "docker build . -t gcr.io/amiteinav-sandbox/pdf-app-immersion"
docker build . -t gcr.io/amiteinav-sandbox/pdf-app-immersion

echo "docker push gcr.io/amiteinav-sandbox/pdf-app-immersion"
docker push gcr.io/amiteinav-sandbox/pdf-app-immersion