import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, random_split, WeightedRandomSampler
import torchvision
import torchvision.transforms as transforms
from models import FeatureExtractor, Classifier
from utils import DEVICE, vis, prepData, imshow

import os

def testVis(
    model,
    feat,
    t_dl,
):
    test_data_iter = iter(t_dl)

    invNorm = transforms.Compose([transforms.Normalize(mean = [ 0., 0., 0.], std = [ 1/0.229, 1/0.224, 1/0.225]),
                                    transforms.Normalize(mean = [ -0.485, -0.456, -0.406], std = [ 1., 1., 1. ]),])

    with torch.no_grad():
        model.eval()
        feat.eval()
        for i in range(20):
            img, label = next(test_data_iter)
            label = torch.from_numpy(label.cpu().numpy().reshape(len(label), 1).astype(np.float32))
            img, label = img.to(DEVICE), label.to(DEVICE)

            extracted = feat(img)

            pred = model(extracted)

            cut = np.array([int(x >= 0.5) for x in pred.detach().cpu().numpy()]).reshape((len(label), 1))

            print(f"guess: {pred.item()}")

            inv_img = invNorm(img.detach().cpu())

            imshow(torchvision.utils.make_grid(inv_img), i, f'Output: {cut[0][0]:.2f}\nLabel: {label.item():.2f}')
            

def main():
    path = "data/"
    split = 0.5
    print(f"Using DEVICE: {DEVICE}")

    # Prepare DataLoaders
    print("Preparing data...")
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    _, _, test_dl = prepData(path, split, 1, preprocess)

    # Prepare Models
    print("Preparing models...")
    model = Classifier().to(DEVICE)
    feat = FeatureExtractor().to(DEVICE)

    model.load_state_dict(torch.load("dense_weights.pth"))

    print("Producing samples...")
    samples = testVis(
        model,
        feat,
        test_dl,
    )

    print("Finishing...")

if __name__ == "__main__":
    main()