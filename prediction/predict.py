import numpy as np
from PIL import Image

import cv2
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from prediction.models import FeatureExtractor, Classifier
from prediction.utils import DEVICE

import os
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help="filepath of image")
args = parser.parse_args()

"""

Face Extractor code from JeeveshN/Face-Detect

"""

CASCADE="prediction/Face_cascade.xml"
FACE_CASCADE=cv2.CascadeClassifier(CASCADE)

def extractFaces(
    impath: str,
):
    image=cv2.imread(impath)
    image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,minNeighbors=5,minSize=(25,25),flags=0)

    for i, (x,y,w,h) in enumerate(faces):
        sub_img=image[y-15:y+h+15,x-15:x+w+15]
        os.chdir("Extracted")
        cv2.imwrite(str(i) + ".jpg",sub_img)
        os.chdir("../")

    return len(faces)

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
        string   : If successful, returns percent confidence of deepfake detected. Otherwise, reason for failure
    """
    # Create 'Extracted' dir
    if not "Extracted" in os.listdir("."):
        os.mkdir("Extracted")
    else:
        # If it already exists, delete all its contents
        files = glob.glob("Extracted/*")
        for f in files:
            os.remove(f)

    # Extract face(s)
    num_subjects  = extractFaces(impath)
    if num_subjects == 0:
        return "Failed to identify subject in image."

    images = []
    subjects = glob.glob("Extracted/*")

    for subject in subjects:
        images.append(Image.open(subject))

    # Preprocess image
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    for i in range(len(images)):
        images[i] = preprocess(images[i])
    
    # Prepare models
    model = Classifier().to(DEVICE)
    feat = FeatureExtractor().to(DEVICE)

    model.load_state_dict(torch.load("prediction/dense_weights.pth", map_location ='cpu'))

    model.eval()
    feat.eval()

    results = []
    with torch.no_grad():
        for img in images:
            img = img.to(DEVICE)
            img = img.unsqueeze(0)

            features = feat(img)
            pred = model(features)

            results.append(pred.item())
    
    confidence = max(results)
    confidence = "%.2f" % (confidence * 100) + "%"
    
    return confidence

def main():
    conf = predict(args.path)
    print(f"Predicted confidence: {conf}")

if __name__=="__main__":
    main()