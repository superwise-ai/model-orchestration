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
        """
        The constructor method should do the following:
            1 - Set the sklearn model
            2 - Define Superwise driver for logging the predictions
        """
        ### TODO Workshop: Complete Here
        pass 

    def _send_monitor_data(self, predictions):
        transaction_id = self._sw.transaction.log_records(
            model_id=os.getenv("SUPERWISE_MODEL_ID"),
            version_id=os.getenv("SUPERWISE_VERSION_ID"),
            records=predictions,
        )
        return transaction_id

    def predict(self, instances, **kwargs):
        """
            Pseudo:
                - read instances into DataFrame
                - use the dataframe to predict values
                - send the prediction and data to Superwise using
                self._send_monitor_data(x)
                - create an output contains of the whole Dataframe and
                transaction_id
        """ 
        ### TODO Workshop: Complete HERE


        ###############################
        # Send data to Superwise
        transaction_id = self._send_monitor_data(input_df)
        api_output = {
            "transaction_id": transaction_id,
            "predicted_prices": input_df["predictions"].values.tolist(),
        }
        return api_output

    def _set_model(self, model_gcs_path):
        """
        This function read a file from GCS, unserialze it using joblib and
        returns sklearn-pipeline ready for predictions

        @params:
            - path to GCS joblib file
        RETURNS: Pipeline ready for predictions
        """
        ## TODO Workshop: COMPLETE_HERE
        return model
