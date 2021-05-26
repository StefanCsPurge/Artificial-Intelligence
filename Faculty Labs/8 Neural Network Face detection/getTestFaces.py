import requests
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import io


for i in range(50):
    response = requests.get(requests.get("https://fakeface.rest/face/json?gender=male").json()['image_url'])
    file = open("test/male/" + str(i + 1) + ".jpg", "wb")
    file.write(response.content)
    file.close()

    response = requests.get(requests.get("https://fakeface.rest/face/json?gender=female").json()['image_url'])
    file = open("test/female/" + str(i + 1) + ".jpg", "wb")
    file.write(response.content)
    file.close()

    print(i)

    # Show the image
    # imgBytes = response.content
    # img = mpimg.imread(io.BytesIO(imgBytes), format='jpg')
    # plt.imshow(img)
    # plt.show()






