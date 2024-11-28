from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from stegano import lsb
from random import randrange
from method_2 import arnolds_cat_transform
from pvd_lib import pvd_lib
from lsb_lib import extract_secret_image
from lsb_lib import embed_secret_image
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
from huffman_lib import HuffmanCoding
from lsb import extract_lsb
from lsb import embed_lsb
import base64
import numpy
import io
import time


global image_list
image_list = ["cover-image", "secret-image", "stego-image"]

global temp_image_path
temp_image_path = ["temp/cover-image-temp.png", "temp/secret-image_temp.png", "temp/stego-image-temp.png"]

global display_list
display_list = ["cover-display", "secret-display", "stego-display"]

global cover_image_path, secret_image_path, stego_image_path
cover_image_path = 0
secret_image_path = 0
stego_image_path = 0

global cover_path, secret_path, stego_path


def reset_frames():
    Label(cover_frame, image=blank500).grid(row=0, column=0, padx=0, pady=0)
    Label(secret_frame, image=blank350).grid(row=0, column=0, padx=0, pady=0)
    Label(stego_frame, image=blank500).grid(row=0, column=0, padx=0, pady=0)
    print("RESET ALL IMAGES TO BLANK")

def zero_last_bit(image_path):
    img = Image.open(image_path)
    img_array = numpy.array(img)
    img_array = img_array & 0xFE
    modified_img = Image.fromarray(img_array)
    print("ZERO'D LSB OF STEGO-IMAGE TO DISPLAY AS COVER")
    return modified_img

def method_select(selection):
    global selected_method
    selected_method = selection
    print("SELECTED METHOD: " + selection)

def endec_mode_select(selection):
    global endec_mode
    endec_mode = selection
    print("SELECTED MODE: " + selection)

def pick_cover():
    try:
        global cover_image_path, cover_path
        if endec_mode == "CONCEAL" or (selected_method == "M3 - PIXEL VALUE DIFFERENCE LSB" or "W2 - HUFFMAN + PVD" and endec_mode == "REVEAL"):
            cover_path = askopenfilename()
            cover_image = cover_path
            with Image.open(cover_image).convert("RGB") as cover_image:
                if cover_image.size != (1000, 1000):
                    cover_image = cover_image.resize((1000, 1000))
            cover_image.save(temp_image_path[0])
            global image_list
            image_list[0] = cover_image 
            cover_display = cover_image.resize((500, 500))
            cover_display = ImageTk.PhotoImage(cover_display)
            global display_list
            display_list[0] = cover_display
            Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)
            print("COVER IMAGE SELECTED")
        elif endec_mode == "REVEAL" and selected_method != "M3 - PIXEL VALUE DIFFERENCE LSB" or "W2 - HUFFMAN + PVD":
            cover_image_path = filedialog.askdirectory()  
            print("COVER SAVE PATH SELECTED")
    except Exception:
        print("SELECT METHOD, MODE AND IMAGES")  

def pick_secret():
    try:
        if endec_mode == "CONCEAL": 
            global secret_path
            secret_path = askopenfilename()
            secret_image = secret_path
            with Image.open(secret_image).convert("RGB") as secret_image:
                if secret_image.size != (350, 350):
                    secret_image = secret_image.resize((350, 350))
            secret_image.save(temp_image_path[1])
            global image_list
            image_list[1] = secret_image
            secret_display = ImageTk.PhotoImage(secret_image)
            global display_list
            display_list[1] = secret_display
            Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
            print("SECRET IMAGE SELECTED")
        elif endec_mode == "REVEAL":
            global secret_image_path
            secret_image_path = filedialog.askdirectory()
            print("SECRET SAVE PATH SELECTED")
    except Exception:
        print("SELECT METHOD, MODE AND IMAGES") 

def pick_stego():
    try:
        if endec_mode == "REVEAL": 
            global stego_path
            stego_path = askopenfilename()
            stego_image = stego_path
            with Image.open(stego_image).convert("RGB") as stego_image:
                if stego_image.size != (1000, 1000):
                    stego_image = stego_image.resize((1000, 1000))
            stego_image.save(temp_image_path[2])
            global image_list
            image_list[2] = stego_image 
            stego_display = stego_image.resize((500, 500))
            stego_display = ImageTk.PhotoImage(stego_display)
            global display_list
            display_list[2] = stego_display
            Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
            print("STEGO-IMAGE SELECTED")
        elif endec_mode == "CONCEAL":
            global stego_image_path
            stego_image_path = filedialog.askdirectory() 
            print("STEGO-IMAGE SAVE PATH SELECTED")
    except Exception:
        print("SELECT METHOD, MODE AND IMAGES")

def go_activate():
    try:
        global image_list
        global display_list
        global stego_image_path, secret_image_path, cover_image_path
        global cover_path, secret_path, stego_path

        if selected_method == "v CHOOSE METHOD v": 
            return
        
        elif selected_method == "M1 - AES + BLOWFISH ENCRYPTION":
            if endec_mode == "CONCEAL":
                AES_KEY = b'1234567890abcdef' 
                AES_IV = b'abcdef1234567890'
                BLOWFISH_KEY = b'12345678'
                BLOWFISH_IV = b'abcdefgh' 
                
                with open(temp_image_path[1], 'rb') as f:
                    img_data = f.read()
                
                print("ENCRYPTING WITH AES...")
                aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
                aes_encrypted = aes_cipher.encrypt(pad(img_data, AES.block_size))
                
                print("ENCRYPTING WITH BLOWFISH...")
                blowfish_cipher = Blowfish.new(BLOWFISH_KEY, Blowfish.MODE_CBC, BLOWFISH_IV)
                blowfish_encrypted = blowfish_cipher.encrypt(pad(aes_encrypted, Blowfish.block_size))
                print(blowfish_encrypted[-32:])

                with open("method-1/m-1_encrypted-secret.png", 'wb') as f:
                    f.write(blowfish_encrypted)

                print("CONVERTING SECRET TO BYTES...")
                with open("method-1/m-1_encrypted-secret.png", "rb") as image:
                    encrypted_secret_string = base64.b64encode(image.read())
                #print(encrypted_secret_string[:32])
                #print(encrypted_secret_string[-32:])
                #print(len(encrypted_secret_string))
                print("CONCEALING SECRET IN COVER WITH LSB...")
                stego_image = lsb.hide(image_list[0], encrypted_secret_string + b'12')
                
                print("DISPLAYING STEGO-IMAGE")
                stego_display = stego_image.resize((500, 500))
                stego_display = ImageTk.PhotoImage(stego_display)
                display_list[2] = stego_display
                Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
                
                print("SAVING STEGO-IMAGE...")
                if stego_image_path:
                    stego_image.save(stego_image_path+"/method-1_stego-image.png")
                else:
                    stego_image.save("method-1/m-1_stego-image.png")
                print("DONE")
                

            elif endec_mode == "REVEAL":
                AES_KEY = b'1234567890abcdef' 
                AES_IV = b'abcdef1234567890'
                BLOWFISH_KEY = b'12345678' 
                BLOWFISH_IV = b'abcdefgh' 
                
                print("REVEALING SECRET FROM COVER USING LSB...")
                encrypted_secret_string = lsb.reveal(temp_image_path[2])[2:]
                #print(encrypted_secret_string[:32])
                #print(encrypted_secret_string[-32:])
                #print(len(encrypted_secret_string))

                print("PADDING DATA...")
                missing_padding = len(encrypted_secret_string) % 4
                if missing_padding:
                    encrypted_secret_string += '=' * (4 - missing_padding)
                #print(encrypted_secret_string[-32:])

                print("CONVERTING SECRET FROM BYTES...")
                imgdata = base64.b64decode(encrypted_secret_string)
                extracted_secret = "method-1/m-1_extracted-secret.png"
                with open(extracted_secret, 'wb') as f:
                    f.write(imgdata)

                with open("method-1/m-1_extracted-secret.png", 'rb') as f:
                    encrypted_data = f.read()
                
                #print(encrypted_data[-32:])
                print("DECRYPTING BLOWFISH...")
                blowfish_cipher = Blowfish.new(BLOWFISH_KEY, Blowfish.MODE_CBC, BLOWFISH_IV)
                blowfish_decrypted = unpad(blowfish_cipher.decrypt(encrypted_data), Blowfish.block_size)
                
                print("DECRYPTING AES...")
                aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
                aes_decrypted = unpad(aes_cipher.decrypt(blowfish_decrypted), AES.block_size)
                
                with open("method-1/m-1_decrypted-secret.png", 'wb') as f:
                    f.write(aes_decrypted)
                
                print("DISPLAYING SECRET & COVER [WITH 0 LSB]")
                with Image.open("method-1/m-1_decrypted-secret.png") as secret_image:
                    secret_display = ImageTk.PhotoImage(secret_image)
                display_list[1] = secret_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
                
                display_list[0] = ImageTk.PhotoImage(zero_last_bit(temp_image_path[2]).resize((500,500)))
                Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)
                
                print("SAVING SECRET...")
                if secret_image_path:
                    secret_image.save(stego_image_path+"/method-1_decrypted-secret.png")
                else:
                    secret_image.save("method-1/m-1_decrypted-secret.png")
                print("DONE")

        
        elif selected_method == "M2 - ARNOLD'S CAT MAP":
            if endec_mode == "CONCEAL":
                iterations = 1
                print("APPLYING ARNOLD'S CAT MAP...")
                scrambled_secret = arnolds_cat_transform(image_list[1], iterations, 0)
                
                print("DISPLAYING SCRAMBLED SECRET")
                scrambled_display = ImageTk.PhotoImage(scrambled_secret)
                display_list[1] = scrambled_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
                
                print("CONVERTING SECRET TO BYTES...")
                scrambled_secret.save("method-2/m-2_scrambled-secret.png")
                with open("method-2/m-2_scrambled-secret.png", "rb") as image:
                    scrambled_secret_string = base64.b64encode(image.read())
                
                print("CONCEALING SECRET IN COVER USING LSB...")
                stego_image = lsb.hide(image_list[0], scrambled_secret_string)
                
                print("DISPLAYING STEGO-IMAGE")
                stego_display = stego_image.resize((500, 500))
                stego_display = ImageTk.PhotoImage(stego_display)
                display_list[2] = stego_display
                Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
                
                print("SAVING STEGO-IMAGE...")
                if stego_image_path:
                    stego_image.save(stego_image_path+"/method-2_stego-image.png")
                else:
                    stego_image.save("method-2/m-2_stego-image.png")
                print("DONE")

            elif endec_mode == "REVEAL":
                iterations = 599
                print("REVEALING SECRET FROM COVER USING LSB...")
                scrambled_secret_string = lsb.reveal(image_list[2])[2:]

                print("PADDING DATA...")
                missing_padding = len(scrambled_secret_string) % 4
                if missing_padding:
                    scrambled_secret_string += '=' * (4 - missing_padding)

                print("CONVERTING SECRET FROM BYTES...")
                imgdata = base64.b64decode(scrambled_secret_string)
                scrambled_image = "method-2/m-2_extracted-scrambled-secret.png"
                
                with open(scrambled_image, 'wb') as f:
                    f.write(imgdata)

                print("UN-SCRAMBLING ARNOLD'S CAT MAP [THIS MIGHT TAKE A WHILE]")
                secret_image = arnolds_cat_transform(scrambled_image, iterations, 1)
                image_list[1] = secret_image
                

                print("DISPLAYING SECRET & COVER [WITH 0 LSB]")
                secret_display = ImageTk.PhotoImage(secret_image)
                display_list[1] = secret_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)

                display_list[0] = ImageTk.PhotoImage(zero_last_bit(temp_image_path[2]).resize((500,500)))
                Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)

                print("SAVING SECRET...")
                if secret_image_path:
                    secret_image.save(stego_image_path+"/method-2_descrambled-secret.png")
                else:
                    secret_image.save("method-2/m-2_descrambled-secret.png")
                print("DONE")

        elif selected_method == "M3 - PIXEL VALUE DIFFERENCE":
            pvd_obj = pvd_lib()
            if endec_mode == "CONCEAL":
                print("EMBEDDING SECRET IN COVER USING PVD...")
                pvd_obj.pvd_embed(temp_image_path[0], temp_image_path[1], "method-3/m-3_stego-image.png")
                
                with Image.open("method-3/m-3_stego-image.png").convert("RGB") as stego_image:
                    stego_display = stego_image.resize((500, 500))
                    stego_display = ImageTk.PhotoImage(stego_display)

                print("DISPLAYING STEGO-IMAGE")
                display_list[2] = stego_display
                Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)

                print("SAVING STEGO-IMAGE...")
                if stego_image_path:
                    stego_image.save(stego_image_path+"/method-3_stego-image.png")
                else:
                    stego_image.save("method-3/m-3_stego-image.png")
                print("DONE")

            elif endec_mode == "REVEAL":
                print("EXTRACTING SECRET FROM STEGO-IMAGE BY COMPARING WITH COVER USING PVD...")
                pvd_obj.pvd_extract(temp_image_path[0], "method-3/m-3_secret-image.png", temp_image_path[2])

                with Image.open("method-3/m-3_secret-image.png").convert("RGB") as secret_image:
                    secret_display = secret_image.resize((350, 350))
                    secret_display = ImageTk.PhotoImage(secret_display)
                    if secret_image_path:
                        secret_image.save(secret_image_path)
                print("DISPLAYING SECRET")
                display_list[1] = secret_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)

                print("SAVING SECRET...")
                if secret_image_path:
                    secret_image.save(stego_image_path+"/method-3_extracted-secret.png")
                else:
                    secret_image.save("method-3/m-3_extracted-secret.png")
                print("DONE")
                
        
        elif selected_method == "M4 - HUFFMAN COMPRESSION":
            if endec_mode == "CONCEAL":
                with open("temp/secret-image_temp.png", "rb") as image:
                    scrambled_secret_string = base64.b64encode(image.read())
                
                print("CONCEALING SECRET IN COVER USING LSB...")
                stego_image = lsb.hide(image_list[0], scrambled_secret_string)
                
                print("DISPLAYING STEGO-IMAGE")
                stego_display = stego_image.resize((500, 500))
                stego_display = ImageTk.PhotoImage(stego_display)
                display_list[2] = stego_display
                Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
                
                print("SAVING STEGO-IMAGE...")
                if stego_image_path:
                    stego_image.save(stego_image_path+"/method-4_stego-image.png")
                else:
                    stego_image.save("method-4/m-4_stego-image.png")
                print("DONE")


            elif endec_mode == "REVEAL":
                print("REVEALING SECRET FROM COVER USING LSB...")
                scrambled_secret_string = lsb.reveal(image_list[2])[2:]

                print("PADDING DATA...")
                missing_padding = len(scrambled_secret_string) % 4
                if missing_padding:
                    scrambled_secret_string += '=' * (4 - missing_padding)

                print("CONVERTING SECRET FROM BYTES...")
                imgdata = base64.b64decode(scrambled_secret_string)
                scrambled_image = "method-4/m-4_extracted-secret.png"
                
                with open(scrambled_image, 'wb') as f:
                    f.write(imgdata)
                
                image_list[1] = scrambled_image
                
                print("DISPLAYING SECRET & COVER [WITH 0 LSB]")
                secret_img = Image.open(scrambled_image)
                secret_display = ImageTk.PhotoImage(secret_img)
                display_list[1] = secret_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)

                display_list[0] = ImageTk.PhotoImage(zero_last_bit(temp_image_path[2]).resize((500,500)))
                Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)

                print("DONE")
        
        elif selected_method == "M5 - K-LEAST SIGNIFICANT BITS ENCODING":
            if endec_mode == "CONCEAL":
                with open("temp/secret-image_temp.png", "rb") as image:
                    scrambled_secret_string = base64.b64encode(image.read())
                
                print("CONCEALING SECRET IN COVER USING LSB...")
                stego_image = lsb.hide(image_list[0], scrambled_secret_string)
                
                print("DISPLAYING STEGO-IMAGE")
                stego_display = stego_image.resize((500, 500))
                stego_display = ImageTk.PhotoImage(stego_display)
                display_list[2] = stego_display
                Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
                
                print("SAVING STEGO-IMAGE...")
                if stego_image_path:
                    stego_image.save(stego_image_path+"/method-5_stego-image.png")
                else:
                    stego_image.save("method-5/m-5_stego-image.png")
                print("DONE")


            elif endec_mode == "REVEAL":
                print("REVEALING SECRET FROM COVER USING LSB...")
                scrambled_secret_string = lsb.reveal(image_list[2])[2:]

                print("PADDING DATA...")
                missing_padding = len(scrambled_secret_string) % 4
                if missing_padding:
                    scrambled_secret_string += '=' * (4 - missing_padding)

                print("CONVERTING SECRET FROM BYTES...")
                imgdata = base64.b64decode(scrambled_secret_string)
                scrambled_image = "method-5/m-5_extracted-secret.png"
                
                with open(scrambled_image, 'wb') as f:
                    f.write(imgdata)
                
                image_list[1] = scrambled_image
                
                print("DISPLAYING SECRET & COVER [WITH 0 LSB]")
                secret_img = Image.open(scrambled_image)
                secret_display = ImageTk.PhotoImage(secret_img)
                display_list[1] = secret_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)

                display_list[0] = ImageTk.PhotoImage(zero_last_bit(temp_image_path[2]).resize((500,500)))
                Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)

                print("DONE")

        elif selected_method == "W1 - ARNOLD'S CAT MAP + ENCRYPTION":
            if endec_mode == "CONCEAL":
                AES_KEY = b'1234567890abcdef' 
                AES_IV = b'abcdef1234567890' 
                BLOWFISH_KEY = b'12345678' 
                BLOWFISH_IV = b'abcdefgh'

                print("APPLYING ARNOLD'S CAT MAP...")
                iterations = 1
                scrambled_secret = arnolds_cat_transform(image_list[1], iterations, 0)
                
                print("DISPLAYING SCRAMBLED SECRET")
                scrambled_display = ImageTk.PhotoImage(scrambled_secret)
                display_list[1] = scrambled_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
                
                scrambled_secret.save("method-w1/m-w1_scrambled-secret.png")
                
                with open("method-w1/m-w1_scrambled-secret.png", 'rb') as f:
                    img_data = f.read()
                
                print("ENCRYPTING WITH AES...")
                aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
                aes_encrypted = aes_cipher.encrypt(pad(img_data, AES.block_size))
                
                print("ENCRYPTING WITH BLOWFISH...")
                blowfish_cipher = Blowfish.new(BLOWFISH_KEY, Blowfish.MODE_CBC, BLOWFISH_IV)
                blowfish_encrypted = blowfish_cipher.encrypt(pad(aes_encrypted, Blowfish.block_size))
                
                with open("method-w1/m-w1_scrambled-encrypted-secret.png", 'wb') as f:
                    f.write(blowfish_encrypted)

                print("CONVERTING SECRET TO BYTES...")
                with open("method-w1/m-w1_scrambled-encrypted-secret.png", "rb") as image:
                    encrypted_secret_string = base64.b64encode(image.read())
                print(encrypted_secret_string[:32])
                print(encrypted_secret_string[-32:])
                print(len(encrypted_secret_string))
                print("CONCEALING SECRET IN COVER USING LSB...")
                stego_image = lsb.hide(image_list[0], encrypted_secret_string + b'12')
                
                print("DISPLAYING STEGO-IMAGE")
                stego_display = stego_image.resize((500, 500))
                stego_display = ImageTk.PhotoImage(stego_display)
                display_list[2] = stego_display
                Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
                
                print("SAVING STEGO-IMAGE...")
                if stego_image_path:
                    stego_image.save(stego_image_path+"/method-w1_stego-image.png")
                else:
                    stego_image.save("method-w1/m-w1_stego-image.png")
                print("DONE")

            elif endec_mode == "REVEAL":
                iterations = 599
                AES_KEY = b'1234567890abcdef' 
                AES_IV = b'abcdef1234567890'
                BLOWFISH_KEY = b'12345678' 
                BLOWFISH_IV = b'abcdefgh' 
                
                print("REVEALING SECRET...")
                encrypted_secret_string = lsb.reveal(temp_image_path[2])[2:]
                print(encrypted_secret_string[:32])
                print(encrypted_secret_string[-32:])
                print(len(encrypted_secret_string))

                missing_padding = len(encrypted_secret_string) % 4
                if missing_padding:
                    encrypted_secret_string += '=' * (4 - missing_padding)
                #print(encrypted_secret_string[-32:])

                imgdata = base64.b64decode(encrypted_secret_string)
                extracted_secret = "method-1/m-w1_extracted-secret.png"
                with open(extracted_secret, 'wb') as f:
                    f.write(imgdata)

                with open("method-1/m-w1_extracted-secret.png", 'rb') as f:
                    encrypted_data = f.read()
                
                #print(encrypted_data[-32:])
                print("DECRYPTING BLOWFISH...")
                blowfish_cipher = Blowfish.new(BLOWFISH_KEY, Blowfish.MODE_CBC, BLOWFISH_IV)
                blowfish_decrypted = unpad(blowfish_cipher.decrypt(encrypted_data), Blowfish.block_size)
                
                print("DECRYPTING AES...")
                aes_cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
                aes_decrypted = unpad(aes_cipher.decrypt(blowfish_decrypted), AES.block_size)
                
                with open("method-1/m-w1_decrypted-secret.png", 'wb') as f:
                    f.write(aes_decrypted)

                with Image.open("method-1/m-w1_decrypted-secret.png") as scrambled_image:
                    print("UN-SCRAMBLING ARNOLD'S CAT MAP [THIS MIGHT TAKE A WHILE]")
                    secret_image = arnolds_cat_transform(scrambled_image, iterations, 0)
                
                image_list[1] = secret_image
                secret_display = ImageTk.PhotoImage(secret_image)

                print("DISPLAYING SECRET & COVER [WITH 0 LSB]")
                display_list[1] = secret_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
                
                display_list[0] = ImageTk.PhotoImage(zero_last_bit(temp_image_path[2]).resize((500,500)))
                Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)
        
                print("SAVING SECRET...")
                if secret_image_path:
                    secret_image.save(stego_image_path+"/method-w1_descrambled-secret.png")
                else:
                    secret_image.save("method-w1/m-w1_descrambled-secret.png")
                print("DONE")

        elif selected_method == "W2 - HUFFMAN + PVD":
            pvd_obj = pvd_lib()
            if endec_mode == "CONCEAL":
                pvd_obj.pvd_embed(temp_image_path[0], temp_image_path[1], "method-w2/m-w2_stego-image.png")

                with Image.open("method-w2/m-w2_stego-image.png").convert("RGB") as stego_image:
                    stego_display = stego_image.resize((500, 500))
                    stego_display = ImageTk.PhotoImage(stego_display)

                print("DISPLAYING STEGO-IMAGE")
                display_list[2] = stego_display
                Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)

                display_list[0] = ImageTk.PhotoImage(zero_last_bit(temp_image_path[2]).resize((500,500)))
                Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)
        

                print("SAVING STEGO-IMAGE...")
                if stego_image_path:
                    stego_image.save(stego_image_path+"/method-w2_stego-image.png")
                else:
                    stego_image.save("method-w2/m-w2_stego-image.png")
                
                print("DONE")


            elif endec_mode == "REVEAL":
                print("REVEALING SECRET FROM COVER USING LSB...")
                pvd_obj.pvd_extract(temp_image_path[0], "method-w2/m-w2_secret-image.png", temp_image_path[2])
                print("SAVING SECRET...")
                print("PADDING DATA...")
                print("CONVERTING SECRET FROM BYTES...")
                print("DISPLAYING SECRET & COVER [WITH 0 LSB]")
                with Image.open("method-w2/m-w2_secret-image.png").convert("RGB") as secret_image:
                    secret_display = secret_image.resize((350, 350))
                    secret_display = ImageTk.PhotoImage(secret_display)
                    if secret_image_path:
                        secret_image.save(secret_image_path)
                print("DISPLAYING SECRET")
                display_list[1] = secret_display
                Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)

                print("SAVING SECRET...")
                if secret_image_path:
                    secret_image.save(stego_image_path+"/method-w2_extracted-secret.png")
                else:
                    secret_image.save("method-w2/m-w2_extracted-secret.png")
                print("DONE")
        
        print("SELECT NEW IMAGES TO RUN AGAIN")
    except NameError:
        print("SELECT METHOD, MODE AND IMAGES")



def help_info():
    if selected_method == "v CHOOSE METHOD v": 
        help_popup= Toplevel(root)
        help_popup.minsize(500, 320)  # width, height
        help_popup.maxsize(500, 320)
        help_popup.geometry("500x320+500+280")
        help_popup.title("HELP & INFO")
        Label(help_popup, text="""\n
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            [CHOOSE METHOD] - drop-down list contains the available methods.
            [CHOOSE MODE] - toggles between concealing/revealing the secret.
            [+RUN+] - runs the selected method in the selected mode.
            [-CLEAR-] - clears all displayed images. \n
            To select images to use, click on the button above each frame:\n
            In 'CONCEAL' mode you select the cover & secret file,
            and optionally the save location for the stego-image.\n
            In 'REVEAL' mode you select the stego-image file,
            and optionally the save location for the revealed secret.\n
            Window app design & programming by Konrad Mięsowski""",
             justify="left").place(relx=-0.05, rely=0.45, anchor=W)
    
    elif selected_method == "M1 - AES + BLOWFISH ENCRYPTION":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 230)  # width, height
        help_popup.maxsize(500, 230)
        help_popup.geometry("500x230+500+280")
        help_popup.title("HELP & INFO - Method 1")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            Method 1: AES + Blowfish encryption
            Implemented by Konrad Mięsowski\n
            This method encrypts the secret image using AES and Blowfish.
            The secret is concealed within the cover using typical LSB methods.\n
            Based on: M. Alanzy, R. Alomrani, B. Alqarni, S. Almutairi;
            “Image Steganography Using LSB and Hybrid Encryption Algorithms”
            Appl. Sci. 2023, 13, 11771; DOI:10.3390/app132111771""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "M2 - ARNOLD'S CAT MAP":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 240)  # width, height
        help_popup.maxsize(500, 240)
        help_popup.geometry("500x240+500+280")
        help_popup.title("HELP & INFO - Method 2")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            Method 2: Arnold's Cat Map
            Implemented by Konrad Mięsowski\n
            This method scrambles the secret using Arnold's cat map.
            The secret is concealed within the cover using typical LSB methods.\n
            Based on: S. Ali Al-Taweel, M. Husain Al-Hada, A. Mahmoud Nasser;
            “Image in image Steganography Technique based on Arnold Transform 
            and LSB Algorithms”; International Journal of Computer Applications 
            (0975–8887), Vol. 181 – No. 10, Aug. 2018; DOI:10.5120/ijca2018917652""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    
    elif selected_method == "M3 - PIXEL VALUE DIFFERENCE":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 240)  # width, height
        help_popup.maxsize(500, 240)
        help_popup.geometry("500x240+500+280")
        help_popup.title("HELP & INFO - Method 3")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            Method 3: Pixel Value Difference LSB
            Implemented by Szymon Maciejewski\n
            This method utilizes Pixel Value Difference LSB, which conceals more
            of the secret's data within areas of higher contrast in the cover.
            IMPORTANT: TO REVEAL SECRET FROM STEGO-IMAGE, PROVIDE COVER!\n
            Based on: Prof. Sridhar R., Sahana S. U., Ananya Desai S., Aishwarya MS.,  
            Akshitha S.; “The Image Steganography Using LSB And PVD Algorithms”; 
            IJRAR May 2023, Volume 10, Issue 2""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "M4 - HUFFMAN COMPRESSION":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 260)  # width, height
        help_popup.maxsize(500, 260)
        help_popup.geometry("500x260+500+280")
        help_popup.title("HELP & INFO - Method 4")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            Method 4: HUFFMAN COMPRESSION
            Implemented by Szymon Maciejewski\n
            This method uses Huffman encoding to efficiently encode secret data 
            before embedding it into an image, reducing the size of the secret 
            image and improving data integrity. \n
            Based on: R. Das and T. Tuithung, "A novel steganography method for
            image based on Huffman Encoding", 2012 3rd National Conference 
            on Emerging Trends and Applications in Computer Science, 
            Shillong, India, 2012, pp. 14-18, doi: 10.1109/NCETACS.2012.6203290.""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "M5 - K-LEAST SIGNIFICANT BITS ENCODING":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 280)  # width, height
        help_popup.maxsize(500, 280)
        help_popup.geometry("500x280+500+280")
        help_popup.title("HELP & INFO - Method 5")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            Method 5: K-LEAST SIGNIFICANT BITS ENCODING
            Implemented by Szymon Maciejewski\n
            This image steganography technique is based on embedding secret
            data in the k-least significant bits (k-LSB) of an image.\n
            Based on: O. Elharrouss, N. Almaadeed and S. Al-Maadeed,
            "An image steganography approach based on k-least significant 
            bits (k-LSB)", 2020 IEEE International Conference on Informatics, 
            IoT, and Enabling Technologies (ICIoT), Doha, Qatar, 2020, pp. 131-135, 
            doi: 10.1109/ICIoT48696.2020.9089566.""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "W1 - ARNOLD'S CAT MAP + ENCRYPTION":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 240)  # width, height
        help_popup.maxsize(500, 240)
        help_popup.geometry("500x240+500+280")
        help_popup.title("HELP & INFO - Method W1")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            Method W1: Encryption + Arnold's Cat Map
            Implemented by Konrad Mięsowski\n
            This method is a combination of Method 1 & 2; the secret is first
            scrambled using Arnold's cat map, then encrypted using AES & Blowfish.
            The secret is concealed within the cover using typical LSB methods.\n
            Based on the respective papers from Methods 1 & 2.""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "W2 - HUFFMAN + PVD":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 230)  # width, height
        help_popup.maxsize(500, 230)
        help_popup.geometry("500x230+500+280")
        help_popup.title("HELP & INFO - Method W2")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by Konrad Mięsowski & Szymon Maciejewski\n
            Method W2: HUFFMAN + PVD
            Implemented by Szymon Maciejewski\n
            This method is a combination of Method 3 & 4; the secret image is first
            compressed with Huffman encoding and then concealed using PVD.\n
            Based on the respective papers from Methods 3 & 4""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    


# WINDOW SETUP
root = Tk()  # create a root widget
root.title("Image-in-Image StegoAPP")
root.configure(background="gray")
root.minsize(1406, 560)  # width, height
root.maxsize(1406, 560)
root.geometry("1406x560+50+50")  # width x height + x + y


# LEFT SECTION - COVER IMAGE
left_frame = Frame(root, width=510, height=510)
left_frame.grid(row=0, column=0, padx=5, pady=5)

cover_select_frame = Frame(left_frame, width=50, height=10)
cover_select_frame.grid(row=1, column=0, padx=0, pady=(5, 0))
cover_select_button = Button(cover_select_frame, 
                             text="1000x1000px COVER IMAGE (HALF SCALE DISPLAY)", bg="white",
                             command=pick_cover)
cover_select_button.pack()

cover_frame = Frame(left_frame, width=502, height=502, bg="gray")
cover_frame.grid(row=2, column=0, padx=5, pady=5)


# MIDDLE SECTION - METHOD + SECRET IMAGE
middle_frame = Frame(root, width=360, height=360)
middle_frame.grid(row=0, column=1, padx=0, pady=5)

stego_info_frame = Frame(middle_frame, width=50, height=10)
stego_info_frame.grid(row=1, column=0, padx=0, pady=5)
stego_info_button = Button(stego_info_frame, text="[HELP & INFO]", bg="white",
                           command=help_info)
stego_info_button.pack()

method_frame = Frame(middle_frame, width=350, height=20, bg="gray")
method_frame.grid(row=2, column=0, padx=5, pady=0)

method_set = ["v CHOOSE METHOD v", 
              "M1 - AES + BLOWFISH ENCRYPTION", 
              "M2 - ARNOLD'S CAT MAP", 
              "M3 - PIXEL VALUE DIFFERENCE",
              "M4 - HUFFMAN COMPRESSION",
              "M5 - K-LEAST SIGNIFICANT BITS ENCODING",
              "W1 - ARNOLD'S CAT MAP + ENCRYPTION",
              "W2 - HUFFMAN + PVD"] 

method = StringVar(root)
method.set(method_set[0]) # default value
global selected_method
selected_method = (method_set[0])

method_options = OptionMenu(method_frame, method, *method_set,
                            command=method_select)
method_options.pack()

## ENCRYPT / DECRYPT TOGGLE
endec_frame = Frame(middle_frame, width=50, height=10)
endec_frame.grid(row=3, column=0, padx=0, pady=5)

endec_set = ["v CHOOSE MODE",
             "CONCEAL", 
             "REVEAL"] 
endec = StringVar(root)
endec.set(endec_set[0]) # default value
endec_options = OptionMenu(endec_frame, endec, *endec_set, command=endec_mode_select)
endec_options.pack()

## BUTTONS
button_frame = Frame(middle_frame, width=50, height=10)
button_frame.grid(row=4, column=0, padx=0, pady=1)

action_button = Button(button_frame, text="+ RUN +", bg="green",
                       command=go_activate)
action_button.pack(side=LEFT, padx=10)

reset_button = Button(button_frame, text="- CLEAR -", bg="red",
                       command=reset_frames)
reset_button.pack(side=RIGHT, padx=10)


## SECRET
secret_select_frame = Frame(middle_frame, width=50, height=10)
secret_select_frame.grid(row=5, column=0, padx=0, pady=(5, 0))
stego_select_button = Button(secret_select_frame, 
                             text="350x350px SECRET IMAGE (FULL SCALE DISPLAY)", bg="white",
                             command=pick_secret)
stego_select_button.pack()

secret_frame = Frame(middle_frame, width=352, height=352, bg="gray")
secret_frame.grid(row=6, column=0, padx=5, pady=5)


# RIGHT SECTION - STEGO-IMAGE
right_frame = Frame(root, width=510, height=510)
right_frame.grid(row=0, column=2, padx=5, pady=5)

stego_select_frame = Frame(right_frame, width=50, height=10)
stego_select_frame.grid(row=1, column=0, padx=0, pady=(5, 0))
stego_select_button = Button(stego_select_frame, 
                             text="1000x1000px STEGO IMAGE (HALF SCALE DISPLAY)", bg="white",
                             command=pick_stego)
stego_select_button.pack()

stego_frame = Frame(right_frame, width=502, height=502, bg="gray")
stego_frame.grid(row=2, column=0, padx=5, pady=5)

global blank350, blank500
blank350 = PhotoImage(file="temp/blank350.png")
blank500 = PhotoImage(file="temp/blank500.png")

Label(cover_frame, image=blank500).grid(row=0, column=0, padx=0, pady=0)
Label(secret_frame, image=blank350).grid(row=0, column=0, padx=0, pady=0)
Label(stego_frame, image=blank500).grid(row=0, column=0, padx=0, pady=0)

root.mainloop()

