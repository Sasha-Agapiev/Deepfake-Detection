import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, random_split, WeightedRandomSampler
import torchvision
import torchvision.transforms as transforms
from models import FeatureExtractor, Classifier
from utils import DEVICE, vis, prepData

import os
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str, help="filepath of data")
parser.add_argument('epochs', type=int, help="number of epochs to train")
parser.add_argument('split', type=float, help="percent train split")
args = parser.parse_args()

def test(
    model,
    feat,
    test_dl,
):
    loss_fn = nn.BCELoss()

    acc = []
    test_loss = []

    with torch.no_grad():
        model.eval()
        feat.eval()
        for img, label in tqdm(test_dl, total=len(test_dl)):
            label = torch.from_numpy(label.cpu().numpy().reshape(len(label), 1).astype(np.float32))
            img, label = img.to(DEVICE), label.to(DEVICE)

            extracted = feat(img)

            pred = model(extracted)

            loss = loss_fn(pred, label)
            test_loss.append(loss.item())

            cut = np.array([int(x >= 0.5) for x in pred.detach().cpu().numpy()]).reshape((len(label), 1))

            batch_acc = np.sum(np.equal(cut, label.detach().cpu().numpy())) / len(cut)

            acc.append(batch_acc)

    acc = np.array(acc)
    test_loss = np.array(test_loss)
    print(f"\nAverage Test Accuracy across batches: {np.mean(acc): .5f}\nAverage Test Loss across batches: {np.mean(test_loss): .5f}")
    return np.mean(acc), np.mean(test_loss)



def train(
    model,
    feat,
    tdl,
    vdl,
    epochs,
):
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    loss_fn = nn.BCELoss()

    last_best = np.inf
    best_so_far = None

    t_train_loss, t_val_loss = [], []

    for epoch in range(epochs):
        model.train()
        feat.eval()

        print(f"EPOCH: {epoch}")

        c_train_loss, c_val_loss = [], []

        """
        DEBUGGING
        """
        percent_pos = []
        val_pos = []
        val_acc = []
        train_acc = []

        # Training Loop
        for img, label in tqdm(tdl, total=len(tdl)):
            percent_pos.append(sum(label.cpu().numpy()) / len(label)) 

            label = torch.from_numpy(label.cpu().numpy().reshape(len(label), 1).astype(np.float32))
            img, label = img.to(DEVICE), label.to(DEVICE)

            optimizer.zero_grad()

            extracted = feat(img)

            pred = model(extracted)

            loss = loss_fn(pred, label)
            loss.backward()

            c_train_loss.append(loss.detach().cpu().numpy())
            optimizer.step()

            cut = np.array([int(x >= 0.5) for x in pred.detach().cpu().numpy()]).reshape((len(label), 1))

            batch_acc = np.sum(np.equal(cut, label.detach().cpu().numpy())) / len(cut)

            train_acc.append(batch_acc)

        with torch.no_grad():
            model.eval()
            feat.eval()
            
            for img, label in tqdm(vdl, total=len(vdl)):
                val_pos.append(sum(label.cpu().numpy()) / len(label))
                label = torch.from_numpy(label.cpu().numpy().reshape(len(label), 1).astype(np.float32))
                img, label = img.to(DEVICE), label.to(DEVICE)

                extracted = feat(img)

                pred = model(extracted)

                loss = loss_fn(pred, label)
                c_val_loss.append(loss.detach().cpu().numpy())

                cut = np.array([int(x >= 0.5) for x in pred.detach().cpu().numpy()]).reshape((len(label), 1))

                batch_acc = np.sum(np.equal(cut, label.detach().cpu().numpy())) / len(cut)

                val_acc.append(batch_acc)
        
        #print(pred)

        """
        DEBUGGING
        """
        train_avg_pos = np.mean(np.array(percent_pos))
        val_avg_pos = np.mean(np.array(val_pos))

        print(f" Train mean positive for epoch {epoch}: {train_avg_pos: .5f}")
        print(f" Validation mean positive for epoch {epoch}: {val_avg_pos: .5f}")
        
        print(f"\n Average Train Accuracy: {np.mean(np.array(train_acc)): .5f}")
        print(f" Average Validation Accuracy: {np.mean(np.array(val_acc)): .5f}")
        
        mean_train_loss = np.mean(c_train_loss)
        mean_val_loss = np.mean(c_val_loss)
        print(f"\n Training Loss: {mean_train_loss: .5f}\n Validation Loss: {mean_val_loss: .5f}\n")
        t_train_loss.append(mean_train_loss)
        t_val_loss.append(mean_val_loss)

        # Save best-so-far
        if mean_val_loss < last_best:
            best_so_far = model.state_dict()
            last_best = mean_val_loss
        
    # Output Loss Over Epoch Visualization
    vis(t_train_loss, t_val_loss)
    
    return best_so_far

def main():
    path = args.path
    epochs = args.epochs
    split = args.split
    print(f"Using DEVICE: {DEVICE}")

    # Prepare DataLoaders
    print("Preparing data...")
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dl, val_dl, test_dl = prepData(path, split, 32, preprocess)

    # Prepare Models
    print("Preparing models...")
    model = Classifier().to(DEVICE)
    feat = FeatureExtractor().to(DEVICE)

    print("Entering train...")
    print(f"Training for {epochs} epochs.")
    res = train(
        model,
        feat,
        train_dl,
        val_dl,
        epochs,
    )

    print("Saving best model...")
    torch.save(res, "dense_weights.pth")

    print("Entering test...")
    model.load_state_dict(torch.load("dense_weights.pth"))
    test_acc, test_loss = test(
        model,
        feat,
        test_dl,
    )

    print("Logging test results...")
    with open("log/test_log.txt", "w") as f:
        f.write("Acc: " + str(test_acc) + "\nLoss: " + str(test_loss))

if __name__ == "__main__":
    main()