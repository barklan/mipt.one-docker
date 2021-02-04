---
layout: post
title: "Detectron2 - convenient detection framework"
subtitle: "Training Detectron2 on custom dataset"
author: "Gleb"
# header-style: text
lang: en
header-img: "img/in-post/post-detectron2-train/kangaroo.jpg"
header-mask: 0.7
mathjax: true
tags:
  - Python
  - PyTorch
  - Deep Learning
  - Computer Vision
  - Detection
  - Detectron2
  - CVAT
---

### Object Detection

<!-- ![kangaroo](/img/in-post/post-detectron2-train/kangaroo.jpg) -->

The main goal of object detection is to build a model that can detect and localize specific objects in images. It is can be used for face detection, object detection on the road, vehicle type detection, count of pedestrian in any event etc. If you are new to object detection have a look at [awesome starter tutorial](https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Object-Detection) on object detection with PyTorch.


### Making custom dataset

First, we will need our own labeled dataset. I will try to do something uncommon - my objective will be to **detect if there is a specific mark on hand-written text**. Or more specifically, to detect the task number of written solution to physics problem. OCR (optical character recognition) tools are developing rapidly ([Google](https://cloud.google.com/document-ai/docs/ocr), [Abbyy](https://www.abbyy.com/cloud-ocr-sdk/) as a cloud solutions), and although they perform great at extracting text, often times general ocr algorithms fail at defining general document structure.

Thus, if the neural network will successfully train for specific class of documents, it will prove to be a good solution to aid the ocr tool in **structuring hand-written documents**.

Now, to make our dataset we first need the actual images of hand-written solutions. Fortunately, there is no lack of those, we just need to make a pretty structure by renaming each image to it's unique id:

```python
import os
import glob


os.chdir(r"dataset")
for index, oldfile in enumerate(glob.glob('*.jpg'), start=1):
    newfile = f'{index}.jpg'
    os.rename(oldfile, newfile)
```

Then, after splitting the dataset into tran/val/test we need to label the task number on each photo. To do that I will use Intel's **[CVAT](https://github.com/openvinotoolkit/cvat)** (Computer Vision Annotation Tool). It stands out from other labeling tool with it's heavy use of detection models to progressively aid the user with marking the objects.

![cvatmain](/img/in-post/post-detectron2-train/cvat.jpg)

We will save the annotations in YOLO format as a json files which is most common among detection datasets.
Lastly, for convenient use we will upload the dataset to Kaggle.
[![kaggle_dataset](/img/in-post/post-detectron2-train/kaggle_dataset.png)](https://www.kaggle.com/glebbuzin/physics-tasks-written-solutions)


### Detectron2

![detectron2](https://dl.fbaipublicfiles.com/detectron2/Detectron2-Logo-Horz.png)

Aside from writing the training cycle in bare-bones PyTorch there are two main detection frameworks:
- **[MMDetection](https://github.com/open-mmlab/mmdetection)** - part of the OpenMMLab project developed by Multimedia Laboratory, CUHK
- **[Detectron2](https://github.com/facebookresearch/detectron2)** - developed by Facebook AI Research

I decided to stick with Detectron2 as it provides a more user-friendly documentation and modular structure ([official tutorial](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5))


### Prepare dataset

We will use Kaggle to train our network on GPU. First [install Detectron2](https://detectron2.readthedocs.io/en/latest/tutorials/install.html) according to PyTorch version and make necessary imports (**[see full Kaggle notebook](https://www.kaggle.com/glebbuzin/detectron2-train)**). Also connect the dataset to kaggle notebook:

```python
import detectron2

import numpy as np
import os, json, cv2, random
# from google.colab.patches import cv2_imshow
from IPython import display
import PIL

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
```

Detectron2 provides suppport for common dataset formats, including YOLO. We just need to register our dataset: 

```python
from detectron2.data.datasets import register_coco_instances


for d in ["train", "val", "test"]:
    register_coco_instances(f"physics_{d}", {},
                            f"../input/your_dataset/annotations/{d}.json",
                            f"../input/your_dataset/{d}")
```

If your dataset is in custom format you need to write a function to parse it and prepare it into detectron2's standard format. See the [official tutorial](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5) for more details.

To verify the data loading is correct, let's visualize the annotations of randomly selected samples in the training set:

```python
import random
from detectron2.utils.visualizer import Visualizer


my_dataset_train_metadata = MetadataCatalog.get("physics_train")
dataset_dicts = DatasetCatalog.get("physics_train")

for d in random.sample(dataset_dicts, 3):
    img = cv2.imread(d["file_name"])
    visualizer = Visualizer(img[:, :, ::-1],
                            metadata=my_dataset_train_metadata,
                            scale=0.5)
    vis = visualizer.draw_dataset_dict(d)
    cv2_imshow(vis.get_image()[:, :, ::-1])
```

![marked](/img/in-post/post-detectron2-train/marked_sol.jpg)


### Train!

We will use pre-trained on COCO dataset **Faster R-CNN** from [model zoo](https://github.com/facebookresearch/detectron2/blob/master/MODEL_ZOO.md) to initialize the model.

```python
from detectron2.engine import DefaultTrainer


cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file(
    "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
))
cfg.DATASETS.TRAIN = ("physics_train",)
cfg.DATASETS.TEST = ()
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
)  # Let training initialize from model zoo
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025  # pick a good LR
cfg.SOLVER.MAX_ITER = 10000
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 512
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # only has one class

os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
trainer = DefaultTrainer(cfg) 
trainer.resume_or_load(resume=False)
trainer.train()
```

Total training time about ~1 hour with 10000 iterations. In google colab it is possible to use TensorBoard to visualize metrics:

```python
%reload_ext tensorboard
%tensorboard --logdir /kaggle/working/output
```

### Evaluation

Inference should use the config with parameters that are used in training. cfg now already contains everything we've set previously. We changed it a little bit for inference:

```python
# path to the model we just trained
cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR,
                                 "model_final.pth")
# set a custom testing threshold
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
predictor = DefaultPredictor(cfg)
```

Then, we randomly select several samples to visualize the prediction results.

```python
my_dataset_test_metadata = MetadataCatalog.get("physics_train")
from detectron2.utils.visualizer import ColorMode
dataset_dicts = DatasetCatalog.get("physics_test")
for d in random.sample(dataset_dicts, 5):    
    im = cv2.imread(d["file_name"])
    outputs = predictor(im)  
    v = Visualizer(im[:, :, ::-1],
                   metadata=my_dataset_test_metadata, 
                   scale=0.5, 
    )
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2_imshow(out.get_image()[:, :, ::-1])
```

![infer](/img/in-post/post-detectron2-train/infer.jpg)

We can also evaluate its performance using AP metric implemented in COCO API.

```python
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader
evaluator = COCOEvaluator("physics_test",
                          ("bbox", "segm"),
                          False,
                          output_dir="./output/")
test_loader = build_detection_test_loader(cfg, "physics_test")
inference_on_dataset(trainer.model, test_loader, evaluator)
# another equivalent way to evaluate the model is to use `trainer.test`
```

This gives an **AP of ~55**. It is not that good, but for such a difficult task it is expected.

![ap](/img/in-post/post-detectron2-train/ap_metric.jpg)

### What's next?

See **[Part 2](https://barklan.github.io/2021/01/22/deploying-dl-models/)** about deploying deep learning models in production-like environment.

[![demo](/img/in-post/post-detectron2-train/demo.jpg)](https://mipt.one/detection/)
