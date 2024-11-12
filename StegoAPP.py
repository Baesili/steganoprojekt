from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from stegano import lsb
from random import randrange
from method_2 import arnolds_cat_transform
from pvd_lib import pvd_lib
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
import base64
import io
import time


global image_list
image_list = ["cover-image", "secret-image", "stego-image"]

global temp_image_path
temp_image_path = ["cover-image-temp.png", "secret-image-temp.png", "stego-image-temp.png"]

global display_list
display_list = ["cover-display", "secret-display", "stego-display"]

global cover_image_path, secret_image_path, stego_image_path
cover_image_path = 0
secret_image_path = 0
stego_image_path = 0

global cover_path, secret_path, stego_path


def zero_last_bit(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load() 
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            r &= 0xFE
            g &= 0xFE
            b &= 0xFE
            pixels[x, y] = (r, g, b)
    return img 

def method_select(selection):
    global selected_method
    selected_method = selection

def endec_mode_select(selection):
    global endec_mode
    endec_mode = selection

def pick_cover():
    global cover_image_path, cover_path
    if endec_mode == "CONCEAL" or (selected_method == "M3 - PIXEL VALUE DIFFERENCE LSB" and endec_mode == "REVEAL"):
        cover_path = askopenfilename()
        cover_image = cover_path
        with Image.open(cover_image).convert("RGB") as cover_image:
            if cover_image.size != (1000, 1000):
                cover_image = cover_image.resize((1000, 1000))
        cover_image.save("cover-image_temp.png")
        global image_list
        image_list[0] = cover_image 
        cover_display = cover_image.resize((500, 500))
        cover_display = ImageTk.PhotoImage(cover_display)
        global display_list
        display_list[0] = cover_display
        Label(cover_frame, image=display_list[0]).grid(row=0, column=0, padx=0, pady=0)
    elif endec_mode == "REVEAL" and selected_method != "M3 - PIXEL VALUE DIFFERENCE LSB":
        cover_image_path = filedialog.askdirectory()    

def pick_secret():
    if endec_mode == "CONCEAL": 
        global secret_path
        secret_path = askopenfilename()
        secret_image = secret_path
        with Image.open(secret_image).convert("RGB") as secret_image:
            if secret_image.size != (350, 350):
                secret_image = secret_image.resize((350, 350))
        secret_image.save("secret-image_temp.png")
        global image_list
        image_list[1] = secret_image
        secret_display = ImageTk.PhotoImage(secret_image)
        global display_list
        display_list[1] = secret_display
        Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
    elif endec_mode == "REVEAL":
        global secret_image_path
        secret_image_path = filedialog.askdirectory() 

def pick_stego():
    if endec_mode == "REVEAL": 
        global stego_path
        stego_path = askopenfilename()
        stego_image = stego_path
        with Image.open(stego_image).convert("RGB") as stego_image:
            if stego_image.size != (1000, 1000):
                stego_image = stego_image.resize((1000, 1000))
        stego_image.save("stego-image_temp.png")
        global image_list
        image_list[2] = stego_image 
        stego_display = stego_image.resize((500, 500))
        stego_display = ImageTk.PhotoImage(stego_display)
        global display_list
        display_list[2] = stego_display
        Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
    elif endec_mode == "CONCEAL":
        global stego_image_path
        stego_image_path = filedialog.askdirectory() 

def go_activate():
    global image_list
    global display_list
    global stego_image_path, secret_image_path, cover_image_path
    global cover_path, secret_path, stego_path

    if selected_method == "v CHOOSE METHOD v": 
        return
    
    elif selected_method == "M1 - AES + BLOWFISH ENCRYPTION":
        if endec_mode == "CONCEAL":
            image = Image.open(secret_path)
            img_byte_array = io.BytesIO()
            image.save(img_byte_array, format=image.format)
            img_bytes = img_byte_array.getvalue()
            iv = bytearray(16)
            keyaes = 'UZ4i59vPgLRT16s8FZ4i81vPgLRT16qk'
            keyaes = bytes(keyaes, encoding="utf-8")
            print("encrypt with AES")
            cipher_aes= AES.new(keyaes, AES.MODE_CBC, iv)
            padded_data = pad(img_bytes, AES.block_size)
            encrypted_data = iv + cipher_aes.encrypt(padded_data)
            output_image_path = "method-1_encrypted-AES.png"
            with open(output_image_path, 'wb') as f:
                f.write(encrypted_data)

            print("encrypt with Blowfish")
            keyb = bytearray(10)
            cipher_b = Blowfish.new(keyb, Blowfish.MODE_CBC)
            with open("method-1_encrypted-AES.png", 'rb') as f:
                plaintext = f.read()
            padded_text = pad(plaintext, Blowfish.block_size)
            iv = cipher_b.iv
            ciphertext_bf = iv + cipher_b.encrypt(padded_text)
            
            output_blowfish = "method-1_encrypted-AES-BFSH.png"
            with open(output_blowfish, 'wb') as f:
                f.write(ciphertext_bf)

            with open("method-1_encrypted-AES-BFSH.png", "rb") as image:
                fully_encrypted_string = base64.b64encode(image.read())
            
            stego_image = lsb.hide(image_list[0], fully_encrypted_string)

            print("display")
            stego_display = stego_image.resize((500, 500))
            stego_display = ImageTk.PhotoImage(stego_display)
            display_list[2] = stego_display
            Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)

            if stego_image_path:
                stego_image.save(stego_image_path+"/method-1_stego-image.png")
            else:
                stego_image.save("method-1_stego-image.png")

        elif endec_mode == "REVEAL":
            print("put function(stego) here")
    
    elif selected_method == "M2 - ARNOLD'S CAT MAP":
        if endec_mode == "CONCEAL":
            iterations = 1
            scrambled_secret = arnolds_cat_transform(image_list[1], iterations, 0)
            
            scrambled_display = ImageTk.PhotoImage(scrambled_secret)
            display_list[1] = scrambled_display
            Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
            
            scrambled_secret.save("method-2_scrambled-secret.png")
            with open("method-2_scrambled-secret.png", "rb") as image:
                scrambled_secret_string = base64.b64encode(image.read())
            
            stego_image = lsb.hide(image_list[0], scrambled_secret_string)
            
            stego_display = stego_image.resize((500, 500))
            stego_display = ImageTk.PhotoImage(stego_display)
            display_list[2] = stego_display
            Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
            
            if stego_image_path:
                stego_image.save(stego_image_path+"/method-2_stego-image.png")
            else:
                stego_image.save("method-2_stego-image.png")


        elif endec_mode == "REVEAL":
            iterations = 599
            scrambled_secret_string = lsb.reveal(image_list[2])

            # print(scrambled_secret_string)
            # print(len(scrambled_secret_string))

            # scrambled_secret_string = base64.b64encode(bytes(scrambled_secret_string, 'utf-8'))
            scrambled_secret_string = scrambled_secret_string[2:]

            missing_padding = len(scrambled_secret_string) % 4
            if missing_padding:
                scrambled_secret_string += '=' * (4 - missing_padding)

            imgdata = base64.b64decode(scrambled_secret_string)
            scrambled_image = "method-2_extracted-secret.png"
            
            with open(scrambled_image, 'wb') as f:
                f.write(imgdata)

            secret_image = arnolds_cat_transform(scrambled_image, iterations, 1)
            image_list[1] = secret_image
            secret_image.save("method-2_extracted-unscrambled-image.png")

            secret_display = ImageTk.PhotoImage(secret_image)
            display_list[1] = secret_display
            Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
            Label(cover_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)
    

    elif selected_method == "M3 - PIXEL VALUE DIFFERENCE LSB":
        pvd_obj = pvd_lib()
        if endec_mode == "CONCEAL":
            print("put function(cover, secret) here")
            pvd_obj.pvd_embed("cover-image_temp.png", "secret-image_temp.png", "method-3_stego-image.png")
            
            with Image.open("method-3_stego-image.png").convert("RGB") as stego_image:
                stego_display = stego_image.resize((500, 500))
                stego_display = ImageTk.PhotoImage(stego_display)
                if stego_image_path:
                    stego_image.save(stego_image_path)
            display_list[2] = stego_display
            Label(stego_frame, image=display_list[2]).grid(row=0, column=0, padx=0, pady=0)

        elif endec_mode == "REVEAL":
            print("put function(stego) here")
            pvd_obj.pvd_extract("cover-image_temp.png", "method-3_secret-image.png", "stego-image_temp.png")

            with Image.open("method-3_secret-image.png").convert("RGB") as secret_image:
                secret_display = secret_image.resize((350, 350))
                secret_display = ImageTk.PhotoImage(secret_display)
                if secret_image_path:
                    secret_image.save(secret_image_path)
            display_list[1] = secret_display
            Label(secret_frame, image=display_list[1]).grid(row=0, column=0, padx=0, pady=0)
            
    
    elif selected_method == "M4 - DCT TABLE MODIFICATION":
        if endec_mode == "CONCEAL":
            print("put function(cover, secret) here")
        elif endec_mode == "REVEAL":
            print("put function(stego) here")
    
    elif selected_method == "M5 - STEGO-IMAGE DECOLORIZATION":
        if endec_mode == "CONCEAL":
            print("put function(cover, secret) here")
        elif endec_mode == "REVEAL":
            print("put function(stego) here")
    
    elif selected_method == "W1 - ENCRYPTION + ARNOLD'S CAT MAP":
        if endec_mode == "CONCEAL":
            print("put function(cover, secret) here")
        elif endec_mode == "REVEAL":
            print("put function(stego) here")
    
    elif selected_method == "W2 - ???":
        if endec_mode == "CONCEAL":
            print("put function(cover, secret) here")
        elif endec_mode == "REVEAL":
            print("put function(stego) here")
    
    if endec_mode == "CONCEAL":
        print("save stego image and display in frame") 
    elif endec_mode == "REVEAL":
        print("save cover & secret and display them in frames")


def help_info():
    if selected_method == "v CHOOSE METHOD v": 
        help_popup= Toplevel(root)
        help_popup.minsize(500, 300)  # width, height
        help_popup.maxsize(500, 300)
        help_popup.geometry("500x300+500+280")
        help_popup.title("HELP & INFO")
        Label(help_popup, text="""\n
            This is a programme for Image-in-Image steganography. 
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            'CHOOSE METHOD' drop-down list contains the available methods.
            'CHOOSE MODE' toggles between concealing/revealing the secret.
            'GO' runs the selected method in the selected mode.\n
            To select images to use, click on the button above each frame:\n
            In 'CONCEAL' mode you select the cover & secret file,
            and optionally the save location for the stego-image.\n
            In 'REVEAL' mode you select the stego-image file,
            and optionally the save location for the cover & revealed secret.\n
            Window app design & programming by Konrad Mięsowski.""",
             justify="left").place(relx=-0.05, rely=0.45, anchor=W)
    
    elif selected_method == "M1 - AES + BLOWFISH ENCRYPTION":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 230)  # width, height
        help_popup.maxsize(500, 230)
        help_popup.geometry("500x230+500+280")
        help_popup.title("HELP & INFO - Method 1")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            Method 1: 'AES + Blowfish encryption'
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
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            Method 2: Arnold's cat map
            Implemented by Konrad Mięsowski\n
            This method scrambles the secret using Arnold's cat map.
            The secret is concealed within the cover using typical LSB methods.\n
            Based on: S. Ali Al-Taweel, M. Husain Al-Hada, A. Mahmoud Nasser;
            “Image in image Steganography Technique based on Arnold Transform 
            and LSB Algorithms”; International Journal of Computer Applications 
            (0975–8887), Vol. 181 – No. 10, Aug. 2018; DOI:10.5120/ijca2018917652""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    
    elif selected_method == "M3 - PIXEL VALUE DIFFERENCE LSB":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 240)  # width, height
        help_popup.maxsize(500, 240)
        help_popup.geometry("500x240+500+280")
        help_popup.title("HELP & INFO - Method 3")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            Method 3: Pixel Value Difference LSB
            Implemented by Szymon Maciejewski\n
            This method utilizes Pixel Value Difference LSB, which conceals more
            of the secret's data within areas of higher contrast in the cover.\n
            Based on: Prof. Sridhar R., Sahana S. U., Ananya Desai S., Aishwarya MS.,  
            Akshitha S.; “The Image Steganography Using LSB And PVD Algorithms”; 
            IJRAR May 2023, Volume 10, Issue 2""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "M4 - DCT TABLE MODIFICATION":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 260)  # width, height
        help_popup.maxsize(500, 260)
        help_popup.geometry("500x260+500+280")
        help_popup.title("HELP & INFO - Method 4")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            Method 5: Decolorization [& Recolorization]
            Implemented by Szymon Maciejewski\n
            This method uses modified DCT on pre-divided sections of the secret, 
            then quantizes the fragments before concealing the secret within 
            the frequency domain; hiding more data in certain sections of the cover.\n
            Based on: Chin-Chen Chang, Tung-Shou Chen, Lou-Zo Chung; 
            “A steganographic method based upon JPEG and quantization 
            table modification”; Information Sciences 141 (2002) 123–138;
            DOI:10.1016/S0020-0255(01)00194-3""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "M5 - STEGO-IMAGE DECOLORIZATION":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 260)  # width, height
        help_popup.maxsize(500, 260)
        help_popup.geometry("500x260+500+280")
        help_popup.title("HELP & INFO - Method 5")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            Method 5: Decolorization & Recolorization
            Implemented by Szymon Maciejewski\n
            The secret is concealed within the cover using typical LSB methods;
            then a neural network decolorizes the stego-image, which is shared
            in grayscale and recolorized before extracting the secret.\n
            Based on: Qi Li, Bin Ma, Member IEEE, Xiaoyu Wang, Chunpeng Wang, 
            Member IEEE, Suo Gao; “Image Steganography in Color Conversion”; 
            IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—II: EXPRESS BRIEFS, 
            VOL. 71, NO. 1, JANUARY 2024; DOI:10.1109/TCSII.2023.3300330""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "W1 - ENCRYPTION + ARNOLD'S CAT MAP":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 240)  # width, height
        help_popup.maxsize(500, 240)
        help_popup.geometry("500x240+500+280")
        help_popup.title("HELP & INFO - Method W1")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            Method W1: Encryption + Arnold's cat map
            Implemented by Konrad Mięsowski\n
            This method is a combination of Method 1 & 2; the secret is first
            encrypted using AES & Blowfish, then scrambled using Arnold's cat map.
            The secret is concealed within the cover using typical LSB methods.\n
            Based on the respective papers from Methods 1 & 2.""",
             justify="left").place(relx=-0.07, rely=0.45, anchor=W)
    
    elif selected_method == "W2 - ???":
        help_popup= Toplevel(root)
        help_popup.minsize(500, 260)  # width, height
        help_popup.maxsize(500, 260)
        help_popup.geometry("500x260+500+280")
        help_popup.title("HELP & INFO - Method W2")
        Label(help_popup, text="""
            This is a programme for Image-in-Image steganography. 
            Programmed by: Konrad Mięsowski & Szymon Maciejewski\n
            Method 5: Decolorization [& Recolorization]
            Implemented by Szymon Maciejewski\n
            TEXT GOES HERE""",
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
              "M3 - PIXEL VALUE DIFFERENCE LSB",
              "M4 - DCT TABLE MODIFICATION",
              "M5 - STEGO-IMAGE DECOLORIZATION",
              "W1 - ENCRYPTION + ARNOLD'S CAT MAP",
              "W2 - ???"] 

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

## ACTION BUTTON
action_frame = Frame(middle_frame, width=50, height=10)
action_frame.grid(row=4, column=0, padx=0, pady=1)
action_button = Button(action_frame, text="GO", bg="yellow",
                       command=go_activate)
action_button.pack()

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

root.mainloop()

