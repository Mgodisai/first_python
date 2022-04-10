import os
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageTk import PhotoImage


def create_image(folder, filename, text):
    font = ImageFont.load_default()
    text_size = font.getsize(text)

    img = Image.new('RGB', (text_size[0], text_size[1]), 40)
    d = ImageDraw.Draw(img)
    d.text((0, 0), text, font=font, fill=(255, 0, 0))
    img.save(folder+"/"+filename)


def show_image(canvas, folder, filename):
    image_load = Image.open(folder+"/"+filename)
    ratio = min(canvas.winfo_width()/image_load.width, canvas.winfo_height()/image_load.height)
    image_load = image_load.resize(
        (max(int(image_load.width*ratio), 1), max(int(image_load.height*ratio), 1)), Image.ANTIALIAS)
    image = PhotoImage(image_load)
    canvas.image = image
    canvas.create_image(canvas.winfo_width()/2, canvas.winfo_height()/2, image=image, anchor='center')


def list_to_text(s, delimiter):
    str_out = ""
    for i in range(len(s)-1):
        str_out += str(s[i])+delimiter
    str_out += str(s[len(s)-1])
    return str_out


def is_image_exists(folder, filename):
    return os.path.isfile(folder+"/"+filename)
