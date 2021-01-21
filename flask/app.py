import io
import json
import os

from flask import Flask, jsonify, request

from detectron_module import Detectron

app = Flask(__name__)


cfg_path = "/home/app/flask/mediafiles/models/cfg.pkl"
weights_path = "/home/app/flask/mediafiles/models/model_final.pth"
detector = Detectron(cfg_path, weights_path)


@app.route("/detectron", methods=['GET', 'POST'])
def run_detectron():
    random_id = request.args.get("random_id", "flask_got_no_id")
    detector.detect_and_save(random_id)
    success = True
    return jsonify({"success": success})


@app.route("/", methods=["GET"])
def root():
    return jsonify(
        {"msg": "Hi there! You reached flask module!"}
    )


# @app.route("/predict", methods=["POST"])
# def predict():
#     if request.method == "POST":
#         file = request.files["file"]
#         if file is not None:
#             input_tensor = transform_image(file)
#             prediction_idx = get_prediction(input_tensor)
#             class_id, class_name = render_prediction(prediction_idx)
#             return jsonify({"class_id": class_id, "class_name": class_name})


if __name__ == "__main__":
    app.run()