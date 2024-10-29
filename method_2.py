# KONRAD
# ARNOLD + LSB

import os
import io
import sys
import numpy as np
from PIL import Image
from tkinter.filedialog import askopenfilename
print("imports")


def arnolds_cat_transform(image, iterations):
    # Convert the image to a numpy array
    img_array = np.array(image)
    n = img_array.shape[0]  # Assuming square image

    # Check if the image is square
    if img_array.shape[0] != img_array.shape[1]:
        raise ValueError("Image must be square for Arnold's Cat Map.")

    transformed_img = img_array.copy()

    for _ in range(iterations):
        new_img = np.zeros_like(transformed_img)
        
        # Apply Arnold's Cat Map transformation
        for x in range(n):
            for y in range(n):
                new_x = (x + y) % n
                new_y = (x + 2 * y) % n
                new_img[new_x, new_y] = transformed_img[x, y]

        transformed_img = new_img

    # Convert the result back to an image
    return Image.fromarray(transformed_img)


if __name__ == "__main__":
    ipath = askopenfilename()
    with Image.open(ipath).convert("RGB") as img:
        if img.size != (64, 64):
            img = img.resize((64, 64))
    img.load()
    iterations = int(input("How many iterations?: "))
    transformed_image = arnolds_cat_transform(img, iterations)
    transformed_image.save("scrambled.jpg", format="JPEG")
