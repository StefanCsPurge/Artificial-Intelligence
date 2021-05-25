
import numpy as np
import torch


def f(x1, x2):
    return np.sin(x1 + (x2/np.pi))


points_tensor = 20 * torch.rand((1000, 2)) - 10
x1s = []
x2s = []

for point in points_tensor:
    # print(point)
    x1s.append(point[0])
    x2s.append(point[1])
print(points_tensor)

x1s_tensor = torch.tensor(x1s)
x2s_tensor = torch.tensor(x2s)

f = torch.sin(x1s_tensor + (x2s_tensor / np.pi))
print(f)

pairs = torch.column_stack((points_tensor, f))
print(pairs)

torch.save(pairs, "myDataSet.dat")

# savedPairs = torch.load("myDataSet.dat")
# print(savedPairs)
