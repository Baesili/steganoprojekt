from PIL import Image
import numpy as np

def embed_secret_image(cover_image_path, secret_image_path, output_image_path):
    # Load cover and secret images
    cover_image = Image.open(cover_image_path)
    secret_image = Image.open(secret_image_path)

    # Resize the secret image to fit into the cover image
    secret_image = secret_image.resize((350, 350))  # Ensure the secret image is 350x350

    # Convert images to numpy arrays
    cover_array = np.array(cover_image)
    secret_array = np.array(secret_image)

    # Ensure the secret image is binary (black and white)
    secret_array = (secret_array > 128).astype(np.uint8)  # Convert to binary (0 or 1)

    # Create a new array for the output image
    output_array = cover_array.copy()

    # Embed the secret image into the least significant bits of the cover image
    for i in range(secret_array.shape[0]):
        for j in range(secret_array.shape[1]):
            # For each color channel, modify the LSB with the secret bit
            for channel in range(3):  # Assuming RGB channels
                # Set the least significant bit of the cover pixel channel
                output_array[i, j, channel] = (cover_array[i, j, channel] & ~1) | secret_array[i, j]

    # Convert back to an image
    output_image = Image.fromarray(output_array)

    # Save the output image
    output_image.save(output_image_path)
    print(f"Secret image embedded successfully in {output_image_path}")


def extract_secret_image(stego_image_path, output_secret_image_path):
    # Load the stego image
    stego_image = Image.open(stego_image_path)
    stego_array = np.array(stego_image)

    # Initialize an array for the extracted secret image
    secret_array = np.zeros((350, 350), dtype=np.uint8)  # Create an empty binary image

    # Extract the least significant bits from the stego image
    for i in range(secret_array.shape[0]):
        for j in range(secret_array.shape[1]):
            # Get the least significant bit from the red channel of the stego image
            secret_bit = stego_array[i, j, 0] & 1  # Using the red channel
            secret_array[i, j] = secret_bit * 255  # Scale to 255 for visibility (0 or 255)

    # Convert the extracted array back to an image
    secret_image = Image.fromarray(secret_array)

    # Save the extracted secret image
    secret_image.save(output_secret_image_path)
    print(f"Secret image extracted successfully to {output_secret_image_path}")


# Example usage
cover_image_path = "forest test 1000x1000.png"  # Path to your cover image (1000x1000)
secret_image_path = "poczowek test 350x350.png"  # Path to your secret image (350x350)
output_image_path = "output_stego.png"  # Path for the output image
output_secret_image_path = "output_secret.png"  # Path for the extracted secret image

# Embed the secret image
embed_secret_image(cover_image_path, secret_image_path, output_image_path)

# Extract the secret image from the stego image
extract_secret_image(output_image_path, output_secret_image_path)