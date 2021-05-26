import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import Adam
# from torch.autograd import Variable
from SimpleNet import SimpleNet
from imageClassifierDataset import *

batch_size = 32

# Load the training set
train_set = getImageClassifierDataset("train")

# Create a loader for the training set
train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=0)

# Load the test set, note that train is set to False
test_set = getImageClassifierDataset("test")

# Create a loader for the test set, note that both shuffle is set to false for the test loader
test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=0)

# Check if gpu support is available
cuda_avail = torch.cuda.is_available()

# Create model, optimizer and loss function
model = SimpleNet(num_classes=2)

if cuda_avail:
    pass
    # model.cuda()

optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
loss_fn = nn.CrossEntropyLoss()


# Create a learning rate adjustment function that divides the learning rate by 10 every 30 epochs
def adjust_learning_rate(epoch):
    lr = 0.001

    if epoch > 180:
        lr = lr / 1000000
    elif epoch > 150:
        lr = lr / 100000
    elif epoch > 120:
        lr = lr / 10000
    elif epoch > 90:
        lr = lr / 1000
    elif epoch > 60:
        lr = lr / 100
    elif epoch > 30:
        lr = lr / 10

    for param_group in optimizer.param_groups:
        param_group["lr"] = lr


def save_models(epoch):
    torch.save(model.state_dict(), "faces_model_{}.model".format(epoch))
    print("Checkpoint saved")


def test():
    model.eval()
    test_acc = 0.0
    for i, (images, labels) in enumerate(test_loader):

        if cuda_avail:
            pass
            # images = Variable(images.cuda())
            # labels = Variable(labels.cuda())

        # Predict classes using images from the test set
        outputs = model(images)
        _, prediction = torch.max(outputs.data, 1)
        # prediction = prediction.cpu().numpy()

        test_acc += torch.sum(torch.eq(prediction, labels.data))

    # Compute the average acc and loss over all 132 test images
    test_acc = test_acc / 132

    return test_acc


def train(num_epochs):
    best_acc = 0.0

    for epoch in range(num_epochs):
        model.train()
        train_acc = 0.0
        train_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            # Move images and labels to gpu if available
            if cuda_avail:
                pass
                # images = Variable(images.cuda())
                # labels = Variable(labels.cuda())

            # Clear all accumulated gradients
            optimizer.zero_grad()
            # Predict classes using images from the test set
            outputs = model(images)
            # Compute the loss based on the predictions and actual labels
            loss = loss_fn(outputs, labels)
            # Backpropagate the loss
            loss.backward()

            # Adjust parameters according to the computed gradients
            optimizer.step()

            train_loss += loss.cpu().data.item() * images.size(0)
            _, prediction = torch.max(outputs.data, 1)

            train_acc += torch.sum(prediction == labels.data)

        # Call the learning rate adjustment function
        adjust_learning_rate(epoch)

        # Compute the average acc and loss over all 140 training images
        train_acc = train_acc / 140
        train_loss = train_loss / 140

        # Evaluate on the test set
        test_acc = test()

        # Save the model if the test acc is greater than our current best
        if test_acc > best_acc:
            save_models(epoch)
            best_acc = test_acc

        # Print the metrics
        print("Epoch {}, Train Accuracy: {} , TrainLoss: {} , Test Accuracy: {}"
              .format(epoch, train_acc, train_loss, test_acc))


if __name__ == "__main__":
    train(200)
