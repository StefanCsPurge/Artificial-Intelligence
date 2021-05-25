
# load and test the trained model

import torch
import numpy as np

import myModel

filepath = "myNet.pt"
ann = myModel.Net(2, 10, 1)
ann.load_state_dict(torch.load(filepath))
ann.eval()

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print(name, param.data)

x1 = float(input("x1 = "))
x2 = float(input("x2 = "))
x = torch.tensor([x1, x2])

print("Model result:",ann(x).tolist()[0])
print("Correct:", np.sin(x1 + (x2/np.pi)))

