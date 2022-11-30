import numpy as np
from PIL import Image

import cv2
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from ML_ALGO.models import FeatureExtractor, Classifier
from ML_ALGO.utils import DEVICE

import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help="filepath of image")
args = parser.parse_args()

"""

Face Extractor code from JeeveshN/Face-Detect

"""

CASCADE="ML_ALGO/Face_cascade.xml"
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

    return len(faces) == 0

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
    nofaces  = extractFaces(impath)
    if nofaces: return 0
        
    ext_impath = 'Extracted/0.jpg'

    img = Image.open(ext_impath)

    # Preprocess image
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    img = preprocess(img)

    torchvision.transforms.ToPILImage()(img).save("Extracted/extracted_process.jpg")
    
    # Prepare models
    model = Classifier().to(DEVICE)
    feat = FeatureExtractor().to(DEVICE)

    model.load_state_dict(torch.load("ML_ALGO/dense_weights.pth", map_location ='cpu'))

    model.eval()
    feat.eval()

    with torch.no_grad():
        img = img.to(DEVICE)
        img = img.unsqueeze(0)

        features = feat(img)
        pred = model(features)

        confidence = pred.item()

    return confidence

def main():
    conf = predict(args.path)
    print(f"Predicted confidence: {conf}")

if __name__=="__main__":
    main()