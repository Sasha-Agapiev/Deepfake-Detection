import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, random_split, WeightedRandomSampler
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt


def vis(train_loss, val_loss):
  """
  Visualization of loss over epochs
  """

  plt.plot(np.arange(len(train_loss)), train_loss, c='r')
  plt.plot(np.arange(len(val_loss)), val_loss, c='y')
  plt.legend(['Training','Validation'])
  plt.grid(True)
  plt.title('Loss over Epochs')
  plt.xlabel('Epoch')
  plt.ylabel('Loss')
  plt.savefig("log/loss.png")

  print(f"Average Training Loss   : {np.mean(train_loss)}\n")

def imshow(img, num, text=None):
  npimg = img.numpy()
  plt.axis("off")
  if text:
    plt.text(75, 8, text, style='italic',fontweight='bold', 
      bbox={'facecolor':'white', 'alpha':0.8, 'pad':10})

  plt.imshow(np.transpose(npimg, (1, 2, 0)))
  plt.savefig(f"log/sample{num}.png")

def prepData(
    filepath:       str,
    train_split:    float,
    batch_s:        int,
    preprocess:     transforms.Compose,
):
    # Dataset
    dataset = torchvision.datasets.ImageFolder(root=filepath, transform=preprocess)
    
    # Determine train/test split
    dataset_size = len(dataset)
    num_train = int(dataset_size * train_split)
    num_remain = dataset_size - num_train
    train_dataset, remainder = random_split(dataset, [num_train, num_remain])

    # Determine val/test split
    num_val = int(num_remain * 0.5)
    num_test = num_remain - num_val
    val_dataset, test_dataset = random_split(remainder, [num_val, num_test])


    # Determine weighted sampler for training set
    y_indices = train_dataset.indices
    y_train = [dataset.targets[i] for i in y_indices]
    class_sample_count = np.array([len(np.where(y_train == t)[0]) for t in np.unique(y_train)])

    weight = 1. / class_sample_count
    samples_weight = np.array([weight[t] for t in y_train])
    samples_weight = torch.from_numpy(samples_weight)

    train_sampler = WeightedRandomSampler(samples_weight.type('torch.DoubleTensor'), len(samples_weight))

    # Determine weighted sampler for validation set
    y_indices = val_dataset.indices
    y_val = [dataset.targets[i] for i in y_indices]
    class_sample_count = np.array([len(np.where(y_val == t)[0]) for t in np.unique(y_val)])

    weight = 1. / class_sample_count
    samples_weight = np.array([weight[t] for t in y_val])
    samples_weight = torch.from_numpy(samples_weight)

    val_sampler = WeightedRandomSampler(samples_weight.type('torch.DoubleTensor'), len(samples_weight))

    # Determine weighted sampler for testing set
    y_indices = test_dataset.indices
    y_test = [dataset.targets[i] for i in y_indices]
    class_sample_count = np.array([len(np.where(y_test == t)[0]) for t in np.unique(y_test)])

    weight = 1. / class_sample_count
    samples_weight = np.array([weight[t] for t in y_test])
    samples_weight = torch.from_numpy(samples_weight)

    test_sampler = WeightedRandomSampler(samples_weight.type('torch.DoubleTensor'), len(samples_weight))

    # DataLoaders
    train_dataloader = DataLoader(train_dataset, batch_size=batch_s, num_workers=8, sampler=train_sampler)
    val_dataloader = DataLoader(val_dataset, batch_size=batch_s, num_workers=8, sampler=val_sampler)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_s, num_workers=8, sampler=test_sampler)

    return train_dataloader, val_dataloader, test_dataloader

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")