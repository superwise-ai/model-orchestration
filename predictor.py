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
        self._sw = Superwise(
            client_id=os.getenv("SUPERWISE_CLIENT_ID"),
            secret=os.getenv("SUPERWISE_SECRET")
        )

    def _send_monitor_data(self, predictions):
        """
        send predictions and input data to Superwise

        :param pd.Serie prediction
        :return str transaction_id
        """
        transaction_id = self._sw.transaction.log_records(
            model_id=int(os.getenv("SUPERWISE_MODEL_ID")),
            version_id=int(os.getenv("SUPERWISE_VERSION_ID")),
            records=predictions
        )
        return transaction_id

    def predict(self, instances):
        """
        apply predictions on instances and log predictions to Superwise

        :param list instances: [{record1}, {record2} ... {record-N}]
        :return dict api_output: {[predicted_prices: prediction, transaction_id: str]}
        """
        input_df = pd.DataFrame(instances)
        # Add timestamp to prediction
        input_df["predictions"] = self._model.predict(input_df)
        # Send data to Superwise
        transaction_id = self._send_monitor_data(input_df)
        api_output = {
            "transaction_id": transaction_id,
            "predicted_prices": input_df["predictions"].values.tolist(),
        }
        return api_output

    def _set_model(self, model_gcs_path):
        """
        download file from gcs to temp file and deserialize it to sklearn object

        :param str model_gcs_path: Path to gcs file
        :return sklearn.Pipeline model: Deserialized pipeline ready for production
        """
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
        print(f"Finished loading model from GCS")
        return model
