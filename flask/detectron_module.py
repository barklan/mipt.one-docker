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
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
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

        # Read and predict
        im = Image.open(image_path)
        # resize initial image to reduce inference time on cpu
        # im = self.resize(im, 1000)
        im = self.pil_to_cv(im)
        outputs = self.predictor(im)
        v = Visualizer(im[:, :, ::-1],
                    scale=1,
        )
        out = v.draw_instance_predictions(outputs["instances"])
        img_det = self.get_image(out.get_image()[:, :, ::-1])

        # Save
        img_det.save(detect_image_path)
        
        with open(output_path, "w") as f:
            to_write = ["yes\n", str(random_id)]
            f.writelines(to_write)

        return None