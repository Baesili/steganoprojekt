import cv2
import numpy as np
import sys

def embed_lsb(cover_image_path, secret_image_path, output_image_path):
    # Load cover and secret images
    cover_image = cv2.imread(cover_image_path)  # Cover image as RGB
    secret_image = cv2.imread(secret_image_path)  # Secret image as RGB

    # Resize the secret image to match the embedding area (350x350)
    secret_image_resized = cv2.resize(secret_image, (350, 350))

    # Ensure both images are of the same depth and type
    cover_image = cover_image.astype(np.uint8)
    secret_image_resized = secret_image_resized.astype(np.uint8)

    # Embed the secret image into the least significant bits of the cover image
    # First clear the least significant bit of the cover image
    cover_image_cleared = cover_image & 0b11111110

    # Prepare the secret image for embedding (shift MSB of secret to LSB position)
    secret_mask = np.zeros_like(cover_image)
    secret_mask[:350, :350] = secret_image_resized
    secret_image_shifted = secret_mask >> 7  # Shift MSB to LSB

    # Combine the cleared cover image and the shifted secret image
    stego_image = cover_image_cleared | secret_image_shifted

    # Save the stego image
    cv2.imwrite(output_image_path, stego_image)

def extract_lsb(stego_image_path, output_secret_path):
    # Load the stego image
    stego_image = cv2.imread(stego_image_path)

    # Extract the LSBs and scale back to full intensity
    secret_image_extracted = (stego_image & 1) * 255

    # Crop the extracted secret to the embedding area (350x350)
    secret_image_cropped = secret_image_extracted[:350, :350]

    # Save the extracted secret image
    cv2.imwrite(output_secret_path, secret_image_cropped)

def main():
    args = sys.argv

    if len(args) < 2:
        sys.exit("Usage: python lsb.py e <cover_path> <secret_path> <stego_path> OR python lsb.py d <extracted_secret_path> <stego_path>")
    
    command = args[1]

    if command == "e" and len(args) == 5:
        cover_image_path = args[2]
        secret_image_path = args[3]
        output_image_path = args[4]
        embed_lsb(cover_image_path, secret_image_path, output_image_path)

    elif command == "d" and len(args) == 4:
        output_secret_path = args[2]
        stego_image_path = args[3]
        extract_lsb(stego_image_path, output_secret_path)

    else:
        sys.exit("Invalid arguments. Usage: python lsb.py e <cover_path> <secret_path> <stego_path> OR python lsb.py d <extracted_secret_path> <stego_path>")

if __name__ == "__main__":
    main()
