from PIL import Image
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
import os
import io
import sys

def prepare_image(ipath, opath, size):
    with Image.open(ipath) as img:
        
        if img.format != 'JPEG':
            print("Converting file to JPEG...")
            img = img.convert('RGB')

        if img.size != (size, size):
            print(f"Resizing file to {size}x{size}...")
            img = img.resize((size, size))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        print("Saving image as JPEG...")
        imgname = str(os.path.basename(ipath).split('.')[0])
        img.save(str(opath+"/"+imgname+"_"+str(size)+".jpg"), format='JPEG')

    return img_byte_arr

if __name__ == '__main__':
    size = int(input("What size square?: "))
    ipath = askopenfilename()
    opath = filedialog.askdirectory()
    prepare_image(ipath, opath, size)
    print("DONE.")
