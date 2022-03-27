#!/bin/zsh

REPOSITORY='<GCP Artifactory Registry Repo Name>'
PROJECT_ID='<GCP Project Id>'
REGION='<GCP Region>'
IMAGE='<Image Name>'

docker build --tag=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE} .
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}
