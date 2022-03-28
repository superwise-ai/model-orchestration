import logging
import os

from flask import Flask, jsonify, request

from predictor import DiamondPricePredictor

app = Flask("DiamondPricePredictor")
gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
predictor = DiamondPricePredictor(os.environ["MODEL_PATH"])


@app.route("/diamonds/v1/predict", methods=["POST"])
def predict():
    """
    Handle the Endpoint predict request.
    request.json - expected in the following format:
        {
            "instances": [
            {
                "carat" : 1.42, "clarity" : "VVS1", "color" : "F", "cut" : "Ideal", "depth" : 60.8, "record_id" : 27671, "table" : 56, "x" : 7.25, "y" : 7.32, "z" : 4.43
            },
            {
                "carat" : 2.03, "clarity" : "VS2", "color" : "G", "cut" : "Premium", "depth" : 59.6, "record_id" : 27670, "table" : 60, "x" : 8.27, "y" : 8.21, "z" : 4.91
            }
            ]
        }
    """
    predictions = predictor.predict(request.json["instances"])
    return jsonify(
        {
            "predictions": predictions["predicted_prices"],
            "transaction_id": predictions["transaction_id"],
        }
    )


@app.route("/diamonds/v1", methods=["GET"])
def healthcheck():
    """
    Vertex AI intermittently performs health checks on your
    HTTP server while it is running to ensure that it is
    ready to handle prediction requests.
    """
    resp = jsonify(health="Diamonds Prediction Service is Alive!")
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(host="localhost")
