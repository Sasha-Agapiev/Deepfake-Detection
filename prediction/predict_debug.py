import numpy as np
from PIL import Image

import cv2
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from models import FeatureExtractor, Classifier
from utils import DEVICE

import os
import sys
import argparse
from tqdm import tqdm

"""

Face Extractor code from JeeveshN/Face-Detect

"""

CASCADE="Face_cascade.xml"
FACE_CASCADE=cv2.CascadeClassifier(CASCADE)

def extractFaces(
    impath: str,
):
    image=cv2.imread(impath)
    image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,minNeighbors=5,minSize=(25,25),flags=0)

    for i, (x,y,w,h) in enumerate(faces):
        sub_img=image[y-30:y+h+30,x-30:x+w+30]
        os.chdir("Extracted")
        cv2.imwrite(str(i) + ".jpg",sub_img)
        os.chdir("../")
        #cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255,0),2)

def predict(
    impath: str,
):
    """
    Takes input image and returns likelihood of it being a deepfake.

    Parameters:
    -----------
    impath
        str     : Filepath of image
    
    Returns:
    --------
    prediction
        float   : Float value between 0-1 indicating confidence of deepfake detection
    """
    # Create 'Extracted' dir
    if not "Extracted" in os.listdir("."):
        os.mkdir("Extracted")

    # Extract face(s)
    # For now, only consider single face extracted
    extractFaces(impath)

    ext_impath = 'Extracted/0.jpg'

    img = Image.open(ext_impath)
    org_img = Image.open(impath)

    # Preprocess image
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    img = preprocess(img)
    org_img = preprocess(org_img)

    torchvision.transforms.ToPILImage()(img).save("Extracted/extracted_process.jpg")
    torchvision.transforms.ToPILImage()(org_img).save("Extracted/original_process.jpg")
    
    # Prepare models
    model = Classifier().to(DEVICE)
    feat = FeatureExtractor().to(DEVICE)

    model.load_state_dict(torch.load("dense_weights.pth"))

    model.eval()
    feat.eval()

    with torch.no_grad():
        img, org_img = img.to(DEVICE), org_img.to(DEVICE)
        img, org_img = img.unsqueeze(0), org_img.unsqueeze(0)

        features = feat(img)
        pred = model(features)

        org_features = feat(org_img)
        org_pred = model(org_features)

        confidence = pred.item()
        org_confidence = org_pred.item()

    return confidence, org_confidence

def main():
    conf, org_conf = predict("/scratch/kl3642/train/dds/Deepfake-Detection/prediction/data/Negative/001575.jpg")
    print(f"Extracted image: {conf}\nOriginal Image: {org_conf}")

if __name__=="__main__":
    main()