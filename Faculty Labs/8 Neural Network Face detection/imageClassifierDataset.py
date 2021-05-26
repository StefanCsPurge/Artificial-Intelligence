from os import listdir
# import torch
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image

device = 'cpu'  # torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


class ImageClassifierDataset(Dataset):
    def __init__(self, image_list, image_classes):
        self.images = []
        self.labels = []
        self.classes = list(set(image_classes))
        self.class_to_label = {c: i for i, c in enumerate(self.classes)}
        self.image_size = 32
        self.transforms = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.CenterCrop(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        for image, image_class in zip(image_list, image_classes):
            transformed_image = self.transforms(image)

            self.images.append(transformed_image)
            label = self.class_to_label[image_class]
            self.labels.append(label)

    def __getitem__(self, index):
        return self.images[index], self.labels[index]

    def __len__(self):
        return len(self.images)


def getImageClassifierDataset(setType):
    img_list = []
    img_classes = []
    folders = [setType + "/male", setType + "/female", setType + "/no_face"]
    for folder in folders:
        for file in listdir(folder):
            img_data = Image.open(folder + "/" + file).convert('RGB')
            img_data.thumbnail((200, 200))
            img_list.append(img_data)
            if folder != setType + '/no_face':
                img_classes.append("face")
            else:
                img_classes.append("no_face")
    print("Loaded",setType,"set")
    return ImageClassifierDataset(img_list, img_classes)
