import tkinter
import customtkinter
from PIL import Image, ImageTk
import numpy
import os


def resize_array(arr):
    return arr.repeat(2, axis=0).repeat(2, axis=1)


def blended_color(source, target, m_strength):
    def blend_element(e):
        return [round((1 - m_strength) * e[0] + m_strength * target[0]),
                round((1 - m_strength) * e[1] + m_strength * target[1]),
                round((1 - m_strength) * e[2] + m_strength * target[2]),
                255]

    return numpy.array([blend_element(si) for si in source])


# Value from slider will be between 0 - 255,
# need to convert to 0 - 1
def convert_to_proper_strength(val):
    return val / 255

#
# red = [255, 0, 0]
# strength = 0.5
#
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# pic = Image.open(os.path.join(parent_dir, 'transparent_background.png'))
# # print(pic)
# pix = numpy.array(pic)
# pix = numpy.array([blended_color(xi, red, strength) for xi in pix]).astype(numpy.uint8)
# pix = resize_array(pix)
# pix = resize_array(pix)
# pix = resize_array(pix)
# pix = resize_array(pix)
#
# base_height = 900
# base_width = 500
#
# root = tkinter.Tk()
# root.geometry(f"{base_width}x{base_height}")
#
# # --- Convert to CTK label image ---
# ctk_img = Image.fromarray(pix)
# button_image = customtkinter.CTkImage(ctk_img, size=(ctk_img.width, ctk_img.height))
# my_img = customtkinter.CTkLabel(master=root, image=button_image, text="")
# my_img.pack()
# # --- Convert to CTK label image ---
#
# img = ImageTk.PhotoImage(image=Image.fromarray(pix))
# canvas = tkinter.Canvas(root)
# canvas.pack()
# canvas.create_image(100, 0, anchor="nw", image=img)
# canvas.place(x=0, y=500)
#
# base = tkinter.Canvas(root)
# base.configure(bg="#ffffff")
# base.pack()
# base.place(x=250, y=500)
#
# textbox = HexCustomCTkTextbox(master=base, text_color="#000000",
#                               height=int(base_height * 0.05),
#                               set_color=None,
#                               fg_color="#ffffff",
#                               corner_radius=None)
# textbox.pack(fill="both", padx=10, pady=5)
# textbox.insert("end-1c", "#")
#
# root.mainloop()
