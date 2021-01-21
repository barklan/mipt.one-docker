import sys
import argparse

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


# def cv2_imshow(a):
#     """A replacement for cv2.imshow() for use in Jupyter notebooks.
#     Args:
#     a : np.ndarray. shape (N, M) or (N, M, 1) is an NxM grayscale image. shape
#       (N, M, 3) is an NxM BGR color image. shape (N, M, 4) is an NxM BGRA color
#       image.
#     """
#     a = a.clip(0, 255).astype('uint8')
#     # cv2 stores colors as BGR; convert to RGB
#     if a.ndim == 3:
#         if a.shape[2] == 4:
#             a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
#         else:
#             a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
#     display.display(PIL.Image.fromarray(a))
    

def get_image(a):
    a = a.clip(0, 255).astype('uint8')
    # cv2 stores colors as BGR; convert to RGB
    if a.ndim == 3:
        if a.shape[2] == 4:
            a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
        else:
            a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(a)


def resize(img, basewidth):
    width, height = img.size
    if (width <= basewidth) or (height <= basewidth):
        return img
    else:
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        return img


def pil_to_cv(pil_image):
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def init_and_run(random_id):
    # with open("/home/app/web/mediafiles/models/cfg.pkl", "rb") as f:
    #     cfg = pickle.load(f)

    # cfg.MODEL.DEVICE = "cpu"
    # # cfg.MODEL.WEIGHTS = os.path.join("/home/app/web/mediafiles/models/model_final.pth")
    # cfg.MODEL.WEIGHTS = "/home/app/web/mediafiles/models/model_final.pth"
    # cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    # predictor = DefaultPredictor(cfg)
    
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cpu"
    predictor = DefaultPredictor(cfg)

    random_id = str(random_id)
    base_path = "/home/app/detectron2/mediafiles/detection_demo/"
    base_relative_url = "/mediafiles/detection_demo/"
    ocred_string = ""
    detected = False

    image_url = base_relative_url + random_id + ".jpg"
    detect_image_url = base_relative_url + random_id + "_detect.jpg"
    crop_image_url = base_relative_url + random_id + "_crop.jpg"
    output_filename = random_id + ".txt"
    output_path = base_path + output_filename

    # im = cv2.imread("demo2.jpg")
    im = Image.open("/home/app/detectron2" + image_url)
    orig = im
    
    # resize initial image to reduce inference time on cpu
    # im = resize(im, 1000)
    im = pil_to_cv(im)

    print('we are here1')
    outputs = predictor(im)  # format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format
    print('we are here2')

    v = Visualizer(im[:, :, ::-1],
    #                metadata=my_dataset_test_metadata, 
                scale=1,
    )
    out = v.draw_instance_predictions(outputs["instances"])


    img_det = get_image(out.get_image()[:, :, ::-1])

    img_det.save("/home/app/detectron2" + detect_image_url)
    
    with open(output_path, "w") as f:
        to_write = ["yes", str(random_id)]
        f.writelines(to_write)

    print('init_finished')
    return None


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id')
    return parser


if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args()
    random_id = args.id

    print('hey1')
    print(random_id)
    init_and_run(random_id)