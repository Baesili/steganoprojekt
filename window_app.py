from tkinter import *


# WINDOW SETUP
root = Tk()  # create a root widget
root.title("Image-in-Image StegoAPP")
root.configure(background="gray")
root.minsize(1400, 560)  # width, height
root.maxsize(1400, 560)
root.geometry("1400x550+50+50")  # width x height + x + y


# LEFT SECTION - COVER IMAGE
left_frame = Frame(root, width=510, height=510)
left_frame.grid(row=0, column=0, padx=5, pady=5)

cover_select_frame = Frame(left_frame, width=50, height=10)
cover_select_frame.grid(row=1, column=0, padx=0, pady=(5, 0))
cover_select_button = Button(cover_select_frame, 
                             text="1000x1000px COVER IMAGE (HALF SCALE DISPLAY)", bg="white")
cover_select_button.pack()

cover_frame = Frame(left_frame, width=500, height=500, bg="gray")
cover_frame.grid(row=2, column=0, padx=5, pady=5)


# MIDDLE SECTION - METHOD + SECRET IMAGE
middle_frame = Frame(root, width=360, height=360)
middle_frame.grid(row=0, column=1, padx=0, pady=5)

stego_info_frame = Frame(middle_frame, width=50, height=10)
stego_info_frame.grid(row=1, column=0, padx=0, pady=5)
stego_info_button = Button(stego_info_frame, text="[HELP & INFO]", bg="white")
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

method_options = OptionMenu(method_frame, method, *method_set)
method_options.pack()

## ENCRYPT / DECRYPT TOGGLE
endec_frame = Frame(middle_frame, width=50, height=10)
endec_frame.grid(row=3, column=0, padx=0, pady=5)

endec_set = ["CONCEAL", "REVEAL "] 
endec = StringVar(root)
endec.set(endec_set[0]) # default value
endec_options = OptionMenu(endec_frame, endec, *endec_set)
endec_options.pack()

## ACTION BUTTON
action_frame = Frame(middle_frame, width=50, height=10)
action_frame.grid(row=4, column=0, padx=0, pady=1)
action_button = Button(action_frame, text="GO", bg="yellow")
action_button.pack()

## SECRET
secret_select_frame = Frame(middle_frame, width=50, height=10)
secret_select_frame.grid(row=5, column=0, padx=0, pady=(5, 0))
stego_select_button = Button(secret_select_frame, 
                             text="350x350px SECRET IMAGE (FULL SCALE DISPLAY)", bg="white")
stego_select_button.pack()

hidden_frame = Frame(middle_frame, width=350, height=350, bg="gray")
hidden_frame.grid(row=6, column=0, padx=5, pady=5)


# RIGHT SECTION - STEGO-IMAGE
right_frame = Frame(root, width=510, height=510)
right_frame.grid(row=0, column=2, padx=5, pady=5)

stego_select_frame = Frame(right_frame, width=50, height=10)
stego_select_frame.grid(row=1, column=0, padx=0, pady=(5, 0))
stego_select_button = Button(stego_select_frame, 
                             text="1000x1000px STEGO IMAGE (HALF SCALE DISPLAY)", bg="white")
stego_select_button.pack()

stego_frame = Frame(right_frame, width=500, height=500, bg="gray")
stego_frame.grid(row=2, column=0, padx=5, pady=5)

root.mainloop()
