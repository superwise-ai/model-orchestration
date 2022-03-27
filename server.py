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
    predictions = predictor.predict(request.json["instances"])
    return jsonify(
        {
            "predictions": predictions["predicted_prices"],
            "transaction_id": predictions["transaction_id"],
        }
    )


@app.route("/diamonds/v1", methods=["GET"])
def healthcheck():
    resp = jsonify(health="Diamonds Prediction Service is Alive!")
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(host="localhost")
