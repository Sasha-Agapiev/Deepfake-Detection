import numpy as np
import os
import pandas as pd
import torchvision.models
from tqdm import tqdm

from utils import DEVICE

"""

Feature Extractor (DenseNet-169)

"""

class FeatureExtractor():
    def __init__(self):
        super(FeatureExtractor, self).__init__()

        self.cnnModel = torchvision.models.densenet169(weights=DenseNet169_Weights.DEFAULT)
        self.feat_extractor = nn.Sequential(*(list(self.cnnModel.children())[:-1]))

    def extractFeatures(
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
        
        return X, y