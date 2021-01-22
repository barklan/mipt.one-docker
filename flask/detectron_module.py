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


class Detectron():
    def __init__(self, cfg_path, weights_path):
        # cfg = get_cfg()
        # cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
        # cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
        # cfg.MODEL.DEVICE = "cpu"
        # predictor = DefaultPredictor(cfg)
        
        with open(cfg_path, "rb") as f:
            cfg = pickle.load(f)

        cfg.MODEL.DEVICE = "cpu"
        cfg.MODEL.WEIGHTS = weights_path
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
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

    def detect_and_save(self, random_id):
        # Paths! paths are my favourite
        random_id = str(random_id)
        base_path = "/home/app/flask/mediafiles/detection_demo/"
        ocred_string = ""
        detected = False
        image_path = base_path + random_id + ".jpg"
        detect_image_path = base_path + random_id + "_detect.jpg"
        crop_image_path = base_path + random_id + "_crop.jpg"
        output_path = base_path + random_id + ".txt"
        task_number = ""

        # Read and predict
        im = Image.open(image_path)
        im = self.resize(im, 1000)
        orig = im
        im = self.pil_to_cv(im)
        outputs = self.predictor(im)
        v = Visualizer(im[:, :, ::-1],
                    scale=1,
        )
        out = v.draw_instance_predictions(outputs["instances"])
        img_det = self.get_image(out.get_image()[:, :, ::-1])

        # Save
        img_det.save(detect_image_path)

        # Crop and save if detected
        boxes_tensor = outputs["instances"].pred_boxes.tensor
        n_boxes = boxes_tensor.shape[0]
        if n_boxes == 0:
            detected = False
        else:
            detected = True
            boxes = [tuple(boxes_tensor[i].numpy()) for i in range(n_boxes)]
            best_box = (5000, 5000, 5000, 5000)
            for box in boxes:
                if box[1] < best_box[1]:
                    best_box = box
            x1, y1, x2, y2 = best_box
            area = (ceil(x1), ceil(y1), ceil(x2), ceil(y2))
            region = orig.crop(area)
            region.save(crop_image_path)
        
        # OCR
        ocr_output_path = base_path + random_id + "_tesseract"
        exit_code = os.system(f"tesseract {crop_image_path} {ocr_output_path}")
        assert exit_code == 0
        with open(ocr_output_path + ".txt", "r") as f:
            string = f.read().strip()
        ocr_failed = False

        # Checks
        if len(string) == 0:
            ocr_failed = True
        else:
            if "." in string:
                some = re.search(r"\d+\.\d+", string)
                if some is not None:
                    task_number = some.group(0)
                else:
                    ocr_failed = True
            else:
                some = re.search(r"\d*", string).group(0)
                if len(some) in [2, 3]:
                    task_number = ".".join((some[0], some[1:]))
                elif len(some) in [4, 5]:
                    task_number = ".".join((some[:2], some[2:]))
                else:
                    ocr_failed = True
                    
        if ocr_failed == True:
            task_number = ""

        with open(output_path, "w") as f:
            yes_or_no_detected = "yes" if detected else "no"
            yes_or_no_ocred = "yes" if not ocr_failed else "no"
            to_write = [f"{yes_or_no_detected}\n", f"{yes_or_no_ocred}\n", str(task_number)]
            f.writelines(to_write)

        return None