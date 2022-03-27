import os
from tempfile import TemporaryFile

import joblib
import pandas as pd
from google.cloud import storage
from superwise import Superwise


CLIENT_ID = os.getenv("SUPERWISE_CLIENT_ID")
SECRET = os.getenv("SUPERWISE_SECRET")
SUPERWISE_MODEL_ID = os.getenv("SUPERWISE_MODEL_ID")
SUPERWISE_VERSION_ID = os.getenv("SUPERWISE_VERSION_ID")


class DiamondPricePredictor(object):
    def __init__(self, model_gcs_path):
        self._model = self._set_model(model_gcs_path)

    def _send_monitor_data(self, predictions):
        sw = Superwise(
            client_id=os.getenv("SUPERWISE_CLIENT_ID"),
            secret=os.getenv("SUPERWISE_SECRET"),
        )
        transaction_id = sw.transaction.log_records(
            model_id=os.getenv("SUPERWISE_MODEL_ID"),
            version_id=os.getenv("SUPERWISE_VERSION_ID"),
            records=predictions,
        )
        return transaction_id

    def predict(self, instances, **kwargs):
        input_df = pd.DataFrame(instances)
        # Add timestamp to prediction
        input_df["predictions"] = self._model.predict(input_df)
        input_df["ts"] = pd.Timestamp.now()
        # Send data to Superwise
        transaction_id = self._send_monitor_data(input_df)
        api_output = {
            "transaction_id": transaction_id,
            "predicted_prices": input_df["predictions"].values.tolist(),
        }
        return api_output

    def _set_model(self, model_gcs_path):
        storage_client = storage.Client()
        bucket_name = os.environ["BUCKET_NAME"]
        print(f"Loading from bucket {bucket_name} model {model_gcs_path}")
        bucket = storage_client.get_bucket(bucket_name)
        # select bucket file
        blob = bucket.blob(model_gcs_path)
        with TemporaryFile() as temp_file:
            # download blob into temp file
            blob.download_to_file(temp_file)
            temp_file.seek(0)
            # load into joblib
            model = joblib.load(temp_file)

        return model
