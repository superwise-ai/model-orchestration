#!/bin/zsh

REPOSITORY='diamonds-predictor-repo'
PROJECT_ID='workshop-347112'
REGION='us-central1'
IMAGE='diamonds_predictor'

docker build --tag=${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE} .
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE}
