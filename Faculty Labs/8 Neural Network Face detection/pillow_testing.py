from matplotlib import image
from matplotlib import pyplot
from PIL import Image

# load and show an image with Pillow
# load the image
myImage = Image.open('f1.jpg')
# summarize some details about the image
print(myImage.format)
print(myImage.mode)
print(myImage.size)
# show the image
myImage.show()


# load and display an image with Matplotlib
# load image as pixel array
#data = image.imread('f1.jpg')
# summarize shape of the pixel array
#print(data.dtype)
#print(data.shape)
# display the array of pixels as an image
#pyplot.imshow(data)
#pyplot.show()


# create a thumbnail of an image
# load the image
img = Image.open('f1.jpg')
# report the size of the image
print(img.size)
# create a thumbnail and preserve aspect ratio
img.thumbnail((222,222))
img.show()
# report the size of the thumbnail
print(img.size)
