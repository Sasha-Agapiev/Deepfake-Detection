import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import torchvision
import torchvision.transforms as transforms

import os
import utils
#import argparse

def train():


def main():
    # Dataset
    filepath = "data/"
    preprocess = transform.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    dataset = torchvision.datasets.ImageFolder(root=filepath, transform=preprocess)
    
    # Determine train/val split
    dataset_size = len(dataset)
    num_train = int(dataset_size * 0.7)
    num_val = dataset_size - num_train
    train_dataset, val_dataset = torch.utils.random_split(dataset, [num_train, num_val])

    # Determine weighted sampler for training set
    y_indices = train_dataset.indices
    y_train = [dataset.targets[i] for i in y_indices]
    class_sample_count = np.array([len(np.where(y_train == t)[0]) for t in np.unique(y_train)])

    weight = 1. / class_sample_count
    samples_weight = np.array([weight[t] for t in y_train])
    samples_weight = torch.from_numpy(samples_weight)

    sampler = WeightedRandomSampler(samples_weight.type('torch.DoubleTensor'), len(samples_weight))

    # DataLoaders
    train_dataloader = DataLoader(train_dataset, batch_size=32, num_workers=8, shuffle=True, sampler=sampler)
    val_dataloader = DataLoader(val_dataset, batch_size=32, num_workers=8, shuffle=True)

if __name__ == "__main__":
    main()