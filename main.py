from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import os

## Global Variables to store image data
filename = None
image = None

## Constants
TKINTER_FONT=("Arial", 14)

def upload_file():
    """Opens a file dialog, loads the image, stores it as a global variable"""
    global filename, image

    file = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file:
        filename = os.path.basename(file)
        image = Image.open(file)
        print(f"Selected: {file}")

def save_image(image, filename):
    """Saves the watermarked image with a new filename."""
    try:
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_watermarked{ext}"
        image.save(new_filename)
        messagebox.showinfo(title="Success!", message=f"Image saved as {new_filename}")
    except Exception as e:
        messagebox.showerror(title="Save Error", message=f"Could not save the image.\nError: {e}")

def watermark_image(image, text, filename):
    """Applies the text watermark to the image and saves it"""
    ## Create a copy to avoid marking the original drawing
    img_to_watermark = image.copy()
    draw = ImageDraw.Draw(img_to_watermark)
    ## Define font, text, color
    font = ImageFont.truetype("arial.ttf",96)
    text = text
    text_color = (255, 255, 255)

    text_width, text_height = draw.textbbox((0,0), text, font=font)[2:4]
    width, height = img_to_watermark.size
    x = width - text_width - 10
    y = height - text_height - 10
    text_position = (x, y)

    # Add a shadow for better readability
    draw.text((x + 1, y + 1), text, font=font, fill=(0,0,0))

    # Draw the main text
    draw.text(text_position, text, font=font, fill=text_color)
    save_image(img_to_watermark, filename)

def apply_watermark():
    """This function is the command for the "Watermark it!" button.
    It gathers all necessary variables and calls the main watermarking function."""
    ## Get text from the Entry widget
    watermark_text = text_entry.get()

    ## Check if an image has been loaded and text has been entered
    if image and watermark_text:
        watermark_image(image=image, text=watermark_text, filename=filename)
    elif not image:
        messagebox.showerror(title="Error", message="Please select an image first.")
    else:
        messagebox.showerror(title="Error", message="Please enter the watermark text.")




window = Tk()
window.title("Anthony's Simple Image Watermarker")
window.config(padx=50, pady=50)

logo = PhotoImage(file="logo.png")
canvas = Canvas(width=332,height=331)
canvas.create_image(166,166, image=logo)
canvas.grid(column=0, row=0, columnspan=2)

#Labels
#image_label = Label(text = "Image to Watermark:", font=FONT)
#image_label.grid(column=0, row=1)
text_label = Label(text = "Watermark Text:", font=TKINTER_FONT)
text_label.grid(column=0,row=2)

#Entries
text_entry = Entry(width=50, font=TKINTER_FONT)
text_entry.grid(column=1, row=2)

#Buttons
image_button = Button(text="Select Image to Watermark", font=TKINTER_FONT, width=70, command=upload_file)
image_button.grid(column=0, row=1, pady=(0,10), columnspan=2)
action_button = Button(text="Watermark It!", font=TKINTER_FONT, width=70, command=apply_watermark)
action_button.grid(column=0, row=3, pady=(10,0), columnspan=2)

window.mainloop()