# Some basic setup:
# Setup detectron2 logger
import detectron2

# import some common libraries
import pickle
import numpy as np
import os, json, cv2, random
import PIL
from PIL import Image


# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from detectron2.data.datasets import register_coco_instances
from detectron2.structures import BoxMode
from detectron2.modeling import build_model
from detectron2.checkpoint import DetectionCheckpointer

import time
from math import ceil
import re


class BaseDetectron():
    def __init__(self):
        self.base_path = "/home/app/flask/mediafiles/detection_demo/"
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
        cfg.MODEL.DEVICE = "cpu"
        self.predictor = DefaultPredictor(cfg)

    def get_image(self, a):
        a = a.clip(0, 255).astype('uint8')
        # cv2 stores colors as BGR; convert to RGB
        if a.ndim == 3:
            if a.shape[2] == 4:
                a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
            else:
                a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(a)

    def resize(self, img, basewidth):
        width, height = img.size
        if (width <= basewidth) or (height <= basewidth):
            return img
        else:
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth,hsize), Image.ANTIALIAS)
            return img

    def pil_to_cv(self, pil_image):
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    def save_text_output(self):
        with open(self.output_path, "w") as f:
            yes_or_no_detected = "yes" if self.detected else "no"
            yes_or_no_ocred = "yes" if not self.ocr_failed else "no"
            to_write = [f"{yes_or_no_detected}\n", f"{yes_or_no_ocred}\n", str(self.text_output)]
            f.writelines(to_write)

    def detect_and_save_base(self, random_id):
        self.random_id = str(random_id)
        self.base_path = "/home/app/flask/mediafiles/detection_demo/"
        self.detected = False
        self.ocr_failed = True
        self.image_path = self.base_path + self.random_id + ".jpg"
        self.detect_image_path = self.base_path + self.random_id + "_detect.jpg"
        self.crop_image_path = self.base_path + self.random_id + "_crop.jpg"
        self.output_path = self.base_path + self.random_id + ".txt"
        self.text_output = ""

        # Read and predict
        im = Image.open(self.image_path)
        im = self.resize(im, 1500)
        self.orig = im
        im = self.pil_to_cv(im)
        self.outputs = self.predictor(im)
        v = Visualizer(im[:, :, ::-1],
                    scale=1,
        )
        out = v.draw_instance_predictions(self.outputs["instances"])
        img_det = self.get_image(out.get_image()[:, :, ::-1])

        # Save
        img_det.save(self.detect_image_path)




class TaskDetectron(BaseDetectron):
    def __init__(self, cfg_path, weights_path):
        with open(cfg_path, "rb") as f:
            cfg = pickle.load(f)

        cfg.MODEL.DEVICE = "cpu"
        cfg.MODEL.WEIGHTS = weights_path
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        self.predictor = DefaultPredictor(cfg)

    def detect_and_save(self, random_id):
        self.detect_and_save_base(random_id)

        # Crop and save if detected
        boxes_tensor = self.outputs["instances"].pred_boxes.tensor
        n_boxes = boxes_tensor.shape[0]
        if n_boxes == 0:
            self.detected = False
        else:
            self.detected = True
            boxes = [tuple(boxes_tensor[i].numpy()) for i in range(n_boxes)]
            best_box = (5000, 5000, 5000, 5000)
            for box in boxes:
                if box[1] < best_box[1]:
                    best_box = box
            x1, y1, x2, y2 = best_box
            area = (ceil(x1), ceil(y1), ceil(x2), ceil(y2))
            region = self.orig.crop(area)
            region.save(self.crop_image_path)
        
        # OCR
            ocr_output_path = self.base_path + random_id + "_tesseract"
            exit_code = os.system(f"tesseract {self.crop_image_path} {ocr_output_path}")
            assert exit_code == 0
            with open(ocr_output_path + ".txt", "r") as f:
                string = f.read().strip()
            self.ocr_failed = False

            # Checks
            if len(string) == 0:
                self.ocr_failed = True
            else:
                if "." in string:
                    some = re.search(r"\d+\.\d+", string)
                    if some is not None:
                        self.text_output = some.group(0)
                    else:
                        self.ocr_failed = True
                else:
                    some = re.search(r"\d*", string).group(0)
                    if len(some) in [2, 3]:
                        self.text_output = ".".join((some[0], some[1:]))
                    elif len(some) in [4, 5]:
                        self.text_output = ".".join((some[:2], some[2:]))
                    else:
                        self.ocr_failed = True
        
        if self.detected and not self.ocr_failed:
            pass  # task_number already written in here     
        elif self.detected and self.ocr_failed:
            self.text_output = "Task number was detected, but not recognized by tesseract."
        elif not self.detected:
            self.text_output = "Task number was not detected :("

        self.save_text_output()
        return None
