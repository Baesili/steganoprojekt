# KONRAD
# ARNOLD + LSB

import os
import io
import sys
import numpy as np
from PIL import Image


def arnolds_cat_transform(image, iterations, mode):
    if mode:
        with Image.open(image).convert("RGB") as image:
            image = image.resize((350, 350))
    
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
