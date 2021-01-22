import os
import pickle
import numpy as np
import PIL
from PIL import Image
from pathlib import Path
from torchvision import transforms, datasets, models
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import sklearn


DEVICE = torch.device('cpu')


class BaseResnet8():
    def __init__(self, model_dict):
        self.model = models.resnet18()
        num_ftrs = self.model.fc.in_features
        n_classes = 2
        self.model.fc = nn.Linear(num_ftrs, 2)
        self.model.load_state_dict(torch.load(model_dict, map_location='cpu'))
        self.model = self.model.to(DEVICE)

    def prepare_one_image(self, file):
        def load_sample(file):
            image = Image.open(file)
            image.load()
            return image

        def prepare_sample(image):
            image = image.resize((224, 224))
            return np.array(image)

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) 
        ])

        # rescale and convert to numpy
        x = load_sample(file)
        x = prepare_sample(x)
        x = np.array(x / 255, dtype='float32')
        x = transform(x)
        return x

    def predict_one_sample(self, inputs, device=DEVICE):
        """For one image"""
        with torch.no_grad():
            inputs = inputs.to(device)
            self.model.eval()
            logit = self.model(inputs).cpu()
            probs = torch.nn.functional.softmax(logit, dim=-1).numpy()
        return probs

    def get_model_output(self, filename):
        ready_img = self.prepare_one_image(filename)
        prob_pred = self.predict_one_sample(ready_img.unsqueeze(0))
        label_encoder = pickle.load(open("label_encoder.pkl", 'rb'))
        predicted_proba = np.max(prob_pred)*100
        y_pred = np.argmax(prob_pred)
        predicted_label = label_encoder.classes_[y_pred]

        if predicted_label == 'solution':
            return True
        else:
            return False