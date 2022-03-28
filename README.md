# SKLean Model Orchestration
Basic Flask App that wraps sklearn model and log predictions into Superwise's platform


# Usage

- From GCP get the [GOOGLE_APPLICATION_CREDENTIALS](https://cloud.google.com/docs/authentication/getting-started#create-service-account-console) Keyfile, place it in resource directory under `creds.json`

- define:
  - `export GOOGLE_APPLICATION_CREDENTIALS=<path to resources/creds.json>`
  - REPOSITORY='GCP Artifactory Registry Repo Name'
  - PROJECT_ID='GCP Project Id'
  - REGION='GCP Region'
  - IMAGE='Image Name'

- Push the image to Google's Artifact Registry using `source build_push_image.sh`

# Local Check
- Build image:
  ```
  docker build --tag=local_predictor \
                  --build-arg MODEL_PATH='models/model_20220324223954.joblib'\
                  --build-arg SUPERWISE_CLIENT_ID="client id"\
                  --build-arg SUPERWISE_SECRET="client secret"\
                  --build-arg SUPERWISE_MODEL_ID=30\
                  --build-arg SUPERWISE_VERSION_ID=1\
                  --build-arg BUCKET_NAME='tmls-workshop-bucket' . 
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



