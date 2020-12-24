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


def load_model(model_dict):
    model_ft = models.resnet18()
    num_ftrs = model_ft.fc.in_features
    n_classes = 2
    model_ft.fc = nn.Linear(num_ftrs, 2)
    model_ft.load_state_dict(torch.load(model_dict, map_location='cpu'))

    model_ft = model_ft.to(DEVICE)
    return model_ft


def prepare_one_image(file):

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


def predict_one_sample(model, inputs, device=DEVICE):
    """Предсказание, для одной картинки"""
    with torch.no_grad():
        inputs = inputs.to(device)
        model.eval()
        logit = model(inputs).cpu()
        probs = torch.nn.functional.softmax(logit, dim=-1).numpy()
    return probs


def get_model_output(model_ft, filename):
    ready_img = prepare_one_image(filename)
    prob_pred = predict_one_sample(model_ft, ready_img.unsqueeze(0))
    label_encoder = pickle.load(open("label_encoder.pkl", 'rb'))
    predicted_proba = np.max(prob_pred)*100
    y_pred = np.argmax(prob_pred)
    predicted_label = label_encoder.classes_[y_pred]

    if predicted_label == 'solution':
        return True
    else:
        return False
