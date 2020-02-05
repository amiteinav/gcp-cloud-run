# Cloud Run

## There are actually two kinds
1. Cloud Run as a Managed Service - as a Managed service
2. Cloud Run on your own GKE cluster

## Preperation for the Demo
* Install git, and clone this repository 
```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install git
git clone https://github.com/amiteinav/gcp-infra-stuff.git
```

## 1. Cloud Run as a Managed Service
* Let's build an app - the docx-to-pdf service
```
cd gsp-infra-stuff/gke/cloud-run/pdf
```
* Instead of building the image as always, with docker build, and then push to the registry, let's use Tekton!
* Authenticate the GKE cluster
```
bash ../../gke/auth_cluster.sh
```

### Installing tekton
* Check if you should be added as a cluster-admin
```
kubectl describe clusterrolebinding cluster-admin-binding
```
* Set yourself as a cluster-admin
```
kubectl create clusterrolebinding cluster-admin-binding \
--clusterrole=cluster-admin \
--user=$(gcloud config get-value core/account)
```
* Install/update tekton
```
kubectl apply --filename https://storage.googleapis.com/tekton-releases/latest/release.yaml
```
* Check the latest namespace added 
```
kubectl get pods --namespace tekton-pipelines
```
* You can install the Tekton CLI - https://github.com/tektoncd/cli/releases/

### Building an image (Using Tekton) and pushing to Google Contrainer Registry
* This task has one step that uses the kaniko project to build a docker image from source and push it to a registry.
```
kubectl create -f gcp-infra-stuff/gke/tekton/taskrun.yaml
```

### Deploying to Cloud Run
* Since this is a manged service, use the gcloud to deploy 
```
gcloud beta run deploy pdf-tekton-svc \
--image gcr.io/`gcloud config get-value project`/pdf-tekton \
--platform managed \
--region us-central1 \
 --allow-unauthenticated
```
* review the deployment
```
gcloud beta run routes describe pdf-tekton-svc --platform=managed --region us-central1
```

## 2. Cloud Run on your own GKE cluster
* Create a cluster
```
export PROJECT_ID=`gcloud config get-value project`

gcloud beta container clusters create cloud-run-gke \
--addons=HorizontalPodAutoscaling,HttpLoadBalancing,Istio,CloudRun \
--machine-type=n1-standard-2 \
--cluster-version=latest --zone=us-central1-b \
--enable-stackdriver-kubernetes \
--scopes cloud-platform

```
* To use a manged service, use the gcloud to deploy 
```
gcloud config set run/cluster_location us-central1-b

gcloud beta run deploy pdf-tekton-svc-gke \
--platform=gke \
--image gcr.io/`gcloud config get-value project`/pdf-tekton  \
--cluster cloud-run-gke   --cluster-location us-central1-b \
--connectivity=external 
```

## Changing GKE default domain to one usable for testing 
* By default, Cloud Run on GKE uses example.com as the base domain, where the fully qualified domain name for a service is formatted as http://{route}.{namespace}.example.com. This default domain doesn't work "out of the box" as a URL you can send requests to.
* you can go to this URL if the below doesn't work for you https://cloud.google.com/run/docs/gke/default-domain
* The instructions show the use of free DNS wildcard sites so you don't have to purchase a custom domain for testing. 
* When you are developing and testing, you change the default domain to use one of the free wildcard DNS test sites - such as nip.io, xip.io, sslip.io
* Get the external IP address
```
kubectl get service istio-ingressgateway --namespace istio-system
```
```
export EXTERNAL_IP=`kubectl get service istio-ingressgateway --namespace istio-system | tail -1 | awk '{print $4}'`

kubectl patch configmap config-domain --namespace knative-serving --patch \
  '{"data": {"example.com": null, "[EXTERNAL_IP].xip.io": ""}}'
```

## Testing Load
* For that we will use Locust
* use the file set-up-locust to set-up 
* get the ingress IP for locust and use the browser to start a tests
 
## Debugging Cloud Run
### starting point
https://cloud.google.com/run/docs/troubleshooting
https://cloud.google.com/run/docs/testing/local

### Debugging locally
* Run this:
```
export IMAGE_NAME=rest-api
export PROJECT_ID=$(gcloud config get-value project)
export PORT=8080
docker run -p 9090:${PORT} -e PORT=${PORT} gcr.io/${PROJECT_ID}/${IMAGE_NAME}
```
* Check if it is working
Open http://localhost:9090 
