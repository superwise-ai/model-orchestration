# SKLearn Model Orchestration
Basic Flask App that demonstrates how to deploy sklearn model and log predictions into Superwise's platform

***

<p align="center" width="100%">
<b>🚧 THIS IS FOR DEMONSTRATION PURPOSE ONLY 🚧</b>
<p align="center" width="100%">
<b>🚧 DO NOT USE IT IN PRODUCTION 🚧</b>

***
# Usage

- From GCP get the [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/docs/authentication/getting-started#create-service-account-console) Keyfile, place it in resources directory under `creds.json`

- define local\environment variables in shell:
  - `GOOGLE_APPLICATION_CREDENTIALS=<path to resources/creds.json>`
  - `REPOSITORY='GCP Artifactory Registry Repo Name'`
  - `PROJECT_ID='GCP Project Id'`
  - `REGION='GCP Region'`
  - `IMAGE='Image Name'`

- Push the image to Google's Artifact Registry using `source build_push_image.sh`

***

# Local Check
- Build image:
  ```
  docker build --tag=local_predictor \
                  --build-arg MODEL_PATH='models/model_20220324223954.joblib' \
                  --build-arg SUPERWISE_CLIENT_ID=<client_id> \
                  --build-arg SUPERWISE_SECRET=<client_secret> \
                  --build-arg SUPERWISE_MODEL_ID=<model_id> \
                  --build-arg SUPERWISE_VERSION_ID=<version_id> \
                  --build-arg BUCKET_NAME=<GCS_Bucket> . 
  ```

- Run Container:
  ```
  docker run -d -p 5050:5050  --name=local_predictor_container local_predictor
  ```
- Health check: `curl -X GET -H "Content-Type: application/json" http://localhost:5050/diamonds/v1`
- Prediction: (INPUT_DATA_FILE is path to json file)
  ```
  curl \
  -X POST \
  -H "Content-Type: application/json" \
  http://localhost:5050/diamonds/v1/predict \
  -d "@${INPUT_DATA_FILE}"
  ```



