from PIL import Image
from tkinter.filedialog import askopenfilename
import os
import io
import sys

def prepare_image(ipath, opath):
    with Image.open(ipath) as img:
        
        if img.format != 'JPEG':
            print("Converting file to JPEG...")
            img = img.convert('RGB')

        if img.size != (512, 512):
            print("Resizing file to 512x512...")
            img = img.resize((512, 512))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        print("Saving image as JPEG...")
        img.save(opath, format='JPEG')

    return img_byte_arr

if __name__ == '__main__':
    ipath = askopenfilename()
    opath = filedialog.askdirectory()
    prepare_image(ipath, opath)
    print("DONE.")
