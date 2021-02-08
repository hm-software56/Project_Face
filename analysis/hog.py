import face_recognition as HOGR
import matplotlib.pyplot as plt

from skimage.feature import hog
from skimage import data, exposure
import cv2

image = cv2.imread('D:/Python/Project_Face/analysis/img/1.jpg')
fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16,16), cells_per_block=(3, 3), visualize=True,
                    multichannel=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
ax1.axis('off')
ax1.imshow(image)
ax1.set_title('Input image')

# Rescale histogram for better display
hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

ax2.axis('off')
ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
ax2.set_title('Histogram of Oriented Gradients')
plt.show()
