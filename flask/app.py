import io
import json
import os
from PIL import Image

from flask import Flask, jsonify, request

from detectron_module import TaskDetectron, BaseDetectron
from resnet_module import BaseResnet8

app = Flask(__name__)


cfg_path = "/home/app/flask/mediafiles/models/cfg.pkl"
weights_path = "/home/app/flask/mediafiles/models/model_final.pth"
task_detector = TaskDetectron(cfg_path, weights_path)
base_detector = BaseDetectron()
base_resnet = BaseResnet8("saved_model")


@app.route("/detectron", methods=['GET', 'POST'])
def run_detectron():
    # Initial setup for output
    random_id = str(request.args.get("random_id", "flask_got_no_id"))
    base_path = "/home/app/flask/mediafiles/detection_demo/"
    detected = False
    ocr_failed = True
    image_path = base_path + random_id + ".jpg"
    detect_image_path = base_path + random_id + "_detect.jpg"
    output_path = base_path + random_id + ".txt"

    solution_status = base_resnet.get_model_output(image_path)
    if not solution_status:
        text_output = "This is not a solution photo at all!"
        img = Image.open(image_path)
        img.save(detect_image_path)
        with open(output_path, "w") as f:
            yes_or_no_detected = "yes" if detected else "no"
            yes_or_no_ocred = "yes" if not ocr_failed else "no"
            to_write = [f"{yes_or_no_detected}\n", f"{yes_or_no_ocred}\n", str(text_output)]
            f.writelines(to_write)
    else:
        task_detector.detect_and_save(random_id)

    return jsonify({"success": True, "solution_status": solution_status})


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