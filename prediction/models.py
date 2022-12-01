import numpy as np
import os
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as tvmodels

from prediction.utils import DEVICE

"""

Feature Extractor (DenseNet-169)

"""

class FeatureExtractor(nn.Module):
    def __init__(self):
        super(FeatureExtractor, self).__init__()

        self.model = tvmodels.densenet169(weights=tvmodels.DenseNet169_Weights.DEFAULT)
        self.feat_extractor = nn.Sequential(*(list(self.model.children())[:-1]))
        
        self.flatten = nn.Flatten()

    """def extractFeatures(
        self,
        dl,
    ):

        extractor = self.feat_extractor
        extractor = extractor.to(DEVICE)

        X, y = [], []
        with torch.no_grad():
            extractor.eval()
            for img, label in tqdm(dl, total = len(dl)):
                img = img.to(DEVICE)

                output = extractor(img)

                X.append(output.cpu().numpy())
                y.append(label)
        
        return X, y"""

    def forward(
        self,
        input,
    ):
        output = self.feat_extractor(input)
        output = F.relu(output, inplace=True)
        output = F.adaptive_avg_pool2d(output, (1, 1))
        output = torch.flatten(output, 1)

        return output

class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        
        self.head = nn.Sequential(
            nn.Linear(1664, 416),
            nn.BatchNorm1d(416),
            nn.ReLU(inplace=True),

            nn.Linear(416, 1),
            nn.Sigmoid(),
        )

    def forward(
        self,
        input,
    ):
        output = self.head(input)
        
        return output