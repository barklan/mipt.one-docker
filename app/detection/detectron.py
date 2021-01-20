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