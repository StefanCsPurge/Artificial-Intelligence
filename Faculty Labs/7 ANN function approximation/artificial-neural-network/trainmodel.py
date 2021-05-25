import torch
import matplotlib.pyplot as plt

import myModel

noOfEpoch = 8888
data = torch.load('myDataSet.dat')

points = torch.empty(0,2)
fun = torch.empty(0,1)
for d in data:  # prepare the points and the function results
    point = torch.tensor([d[0], d[1]])
    points = torch.vstack((points, point))
    fun = torch.vstack((fun, d[2]))

# we set up the lossFunction as the mean square error
lossFunction = torch.nn.MSELoss()

# we create the ANN
ann = myModel.Net(n_feature=2, n_hidden=10, n_output=1)
print(ann)

# we use an optimizer that implements stochastic gradient descent
optimizer_batch = torch.optim.SGD(ann.parameters(), lr=0.05)

# we memorize the losses for some graphics
loss_list = []
avg_loss_list = []

# we set up the environment for training in batches
batch_size = 50
n_batches = int(len(points) / batch_size)
print(n_batches)

for epoch in range(noOfEpoch):
    for batch in range(n_batches):
        # we prepare the current batch  -- please observe the slicing for tensors
        batch_X, batch_y = points[batch * batch_size: (batch + 1) * batch_size, ], \
                           fun[batch * batch_size: (batch + 1) * batch_size, ]

        # we compute the output for this batch
        prediction = ann(batch_X)

        # we compute the loss for this batch
        loss = lossFunction(prediction, batch_y)

        # we save it for graphics
        loss_list.append(loss.item())

        # we set up the gradients for the weights to zero (important in pytorch)
        optimizer_batch.zero_grad()

        # we compute automatically the variation for each weight (and bias) of the network
        loss.backward()

        # we compute the new values for the weights
        optimizer_batch.step()

    # we print the loss for all the dataset for each 50th epoch
    if epoch % 50 == 0:
        y_pred = ann(points)
        loss = lossFunction(y_pred, fun)
        print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss.item()))


# Specify a path
filepath = "myNet.pt"

# save the model to file
torch.save(ann.state_dict(), filepath)
# print(loss_list)

# visualise the parameters for the ann (aka weights and biases)
for name, param in ann.named_parameters():
    if param.requires_grad:
        print(name, param.data)


plt.plot(loss_list)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()
