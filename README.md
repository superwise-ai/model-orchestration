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

```
source build_push_image.sh

```



