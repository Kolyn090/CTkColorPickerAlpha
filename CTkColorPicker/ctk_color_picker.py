# CTk Color Picker for customtkinter
# Original Author: Akash Bora (Akascape)
# Contributers: Victor Vimbert-Guerlais (helloHackYnow)

import tkinter
import customtkinter
from PIL import Image, ImageTk
import os
import math
from my_ctk_components import HexCustomCTkTextbox
from my_ctk_components import ColorPreviewer
from my_util import rgb_to_hsv
from my_util import convert_to_value_100_rgb

PATH = os.path.dirname(os.path.realpath(__file__))


class AskColor(customtkinter.CTkToplevel):

    def __init__(self,
                 width: int = 500,
                 title: str = "Choose Color",
                 initial_color: str = None,
                 bg_color: str = None,
                 fg_color: str = None,
                 button_color: str = None,
                 button_hover_color: str = None,
                 text: str = "OK",
                 corner_radius: int = 24,
                 slider_border: int = 1,
                 **button_kwargs):

        super().__init__()

        self._color = "#FFFFFF"
        self.curr_code = "#FFFFFF"
        self.title(title)
        WIDTH = width if width >= 200 else 200
        HEIGHT = WIDTH + 200
        self.image_dimension = self._apply_window_scaling(WIDTH - 100)
        self.target_dimension = self._apply_window_scaling(20)
        self.target_y = self.image_dimension / 2
        self.target_x = self.image_dimension / 2

        self.maxsize(WIDTH, HEIGHT)
        self.minsize(WIDTH, HEIGHT)
        self.resizable(width=False, height=False)
        # self.transient(self.master)
        self.lift()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.after(10)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.default_hex_color = "#ffffff"
        self.default_rgb = [255, 255, 255]
        self.rgb_color = self.default_rgb[:]

        def choose_from(default_color, custom_color):
            return default_color if custom_color is None else custom_color

        self.bg_color = self._apply_appearance_mode(
            choose_from(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"], bg_color))

        self.fg_color = self._apply_appearance_mode(
            choose_from(customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"], fg_color))

        self.button_color = self._apply_appearance_mode(
            choose_from(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"], button_color))

        self.button_hover_color = self._apply_appearance_mode(
            choose_from(customtkinter.ThemeManager.theme["CTkButton"]["hover_color"], button_hover_color))

        self.button_text = text
        self.corner_radius = corner_radius
        self.slider_border = 10 if slider_border >= 10 else slider_border

        self.config(bg=self.bg_color)

        self.frame = customtkinter.CTkFrame(master=self, fg_color=self.fg_color, bg_color=self.bg_color)
        self.frame.grid(padx=20, pady=20, sticky="nswe")

        self.canvas = tkinter.Canvas(self.frame, height=self.image_dimension, width=self.image_dimension,
                                     highlightthickness=0, bg=self.fg_color)
        self.canvas.pack(pady=20)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        def open_image(image_name, dimension):
            return Image.open(os.path.join(PATH, image_name)).resize(
                (dimension, dimension), Image.Resampling.LANCZOS)

        self.img1 = open_image('color_wheel.png', self.image_dimension)
        self.img2 = open_image('target.png', self.target_dimension)

        self.wheel = ImageTk.PhotoImage(self.img1)
        self.target = ImageTk.PhotoImage(self.img2)

        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)
        self.set_initial_color(initial_color)

        self.brightness_slider_value = customtkinter.IntVar()
        self.brightness_slider_value.set(255)

        self.brightness_slider = customtkinter.CTkSlider(master=self.frame, height=20, border_width=self.slider_border,
                                                         button_length=15, progress_color=self.default_hex_color, from_=0, to=255,
                                                         variable=self.brightness_slider_value, number_of_steps=256,
                                                         button_corner_radius=self.corner_radius, corner_radius=self.corner_radius,
                                                         button_color=self.button_color,
                                                         button_hover_color=self.button_hover_color,
                                                         command=lambda x: self.update_colors())
        self.brightness_slider.pack(fill="both", pady=(0, 15), padx=20 - self.slider_border)

        self.alpha_slider_value = customtkinter.IntVar()
        self.alpha_slider_value.set(255)

        # ------
        self.alpha_slider = customtkinter.CTkSlider(master=self.frame, height=20, border_width=self.slider_border,
                                                    button_length=15, progress_color=self.default_hex_color,
                                                    from_=0, to=255,
                                                    variable=self.alpha_slider_value, number_of_steps=256,
                                                    button_corner_radius=self.corner_radius,
                                                    corner_radius=self.corner_radius,
                                                    button_color=self.button_color,
                                                    button_hover_color=self.button_hover_color,
                                                    command=None, bg_color='transparent',
                                                    border_color='transparent')
        self.alpha_slider.pack(fill="both", pady=(0, 15), padx=20 - self.slider_border)
        # ------

        # self.previewer = ColorPreviewer(master=self.frame)
        # self.previewer.pack()

        self.stack1 = customtkinter.CTkFrame(master=self.frame, fg_color='transparent', bg_color='transparent')

        self.label = customtkinter.CTkLabel(master=self.stack1, text_color="#000000", height=int(HEIGHT * 0.05),
                                            width=int(WIDTH * 0.5), fg_color=self.default_hex_color,
                                            corner_radius=self.corner_radius, text=self.default_hex_color)
        self.label.pack(fill="both", padx=10, pady=5, side='left')

        self.textbox = HexCustomCTkTextbox(master=self.stack1, text_color="#000000", height=int(HEIGHT * 0.05),
                                           set_color=self.set_color,
                                           fg_color=self.default_hex_color,
                                           corner_radius=self.corner_radius)
        self.textbox.pack(fill="both", padx=10, pady=5, side='right')
        self.textbox.insert("end-1c", "#")

        self.stack1.pack(fill="both")

        self.button = customtkinter.CTkButton(master=self.frame, text=self.button_text, height=int(HEIGHT * 0.1),
                                              corner_radius=self.corner_radius, fg_color=self.button_color,
                                              hover_color=self.button_hover_color, command=self._ok_event,
                                              **button_kwargs)
        self.button.pack(fill="both", padx=10, pady=5)

        self.after(150, lambda: self.label.focus())

        self.grab_set()

    def get(self):
        self._color = self.label._fg_color
        self.master.wait_window(self)
        return self._color

    def _ok_event(self, event=None):
        self._color = self.label._fg_color
        self.grab_release()
        self.destroy()
        del self.img1
        del self.img2
        del self.wheel
        del self.target

    def _on_closing(self):
        self._color = None
        self.grab_release()
        self.destroy()
        del self.img1
        del self.img2
        del self.wheel
        del self.target

    def on_mouse_drag(self, event):
        x = event.x
        y = event.y
        self.canvas.delete("all")
        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)

        d_from_center = math.sqrt(((self.image_dimension / 2) - x) ** 2 + ((self.image_dimension / 2) - y) ** 2)

        if d_from_center < self.image_dimension / 2:
            self.target_x, self.target_y = x, y
        else:
            self.target_x, self.target_y = self.projection_on_circle(x, y, self.image_dimension / 2,
                                                                     self.image_dimension / 2,
                                                                     self.image_dimension / 2 - 1)

        self.canvas.create_image(self.target_x, self.target_y, image=self.target)

        self.get_target_color()
        self.update_colors()

    def get_target_color(self):
        try:
            self.rgb_color = self.img1.getpixel((int(self.target_x), int(self.target_y)))

            r = self.rgb_color[0]
            g = self.rgb_color[1]
            b = self.rgb_color[2]
            self.rgb_color = [r, g, b]

        except AttributeError:
            self.rgb_color = self.default_rgb

    def update_colors(self):
        brightness = self.brightness_slider_value.get()
        # print(self.brightness_slider_value.get())

        self.get_target_color()

        r = int(self.rgb_color[0] * (brightness / 255))
        g = int(self.rgb_color[1] * (brightness / 255))
        b = int(self.rgb_color[2] * (brightness / 255))

        self.rgb_color = [r, g, b]

        self.default_hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
        # self.default_hex_color = "#ffffff77"

        self.brightness_slider.configure(progress_color=self.default_hex_color)
        self.label.configure(fg_color=self.default_hex_color)

        # Controls the label text
        self.label.configure(text=str(self.default_hex_color))
        self.textbox.set_content_to(self.default_hex_color)

        if self.brightness_slider_value.get() < 70:
            self.label.configure(text_color="white")
        else:
            self.label.configure(text_color="black")

        if str(self.label._fg_color) == "black":
            self.label.configure(text_color="white")

    def update_colors2(self, code):
        # brightness = self.brightness_slider_value.get()
        # print(self.brightness_slider_value.get())

        # r = int(self.rgb_color[0] * (brightness / 255))
        # g = int(self.rgb_color[1] * (brightness / 255))
        # b = int(self.rgb_color[2] * (brightness / 255))

        r, g, b = tuple(int(code.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        hsv = rgb_to_hsv(r, g, b)
        # print(r, g, b)
        # print(hsv[2] * 255 / 100)
        self.brightness_slider_value.set(hsv[2] * 255 / 100)

        self.rgb_color = [r, g, b]
        # print(code)

        self.default_hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)

        self.brightness_slider.configure(progress_color=self.default_hex_color)
        self.label.configure(fg_color=self.default_hex_color)

        # Controls the label text
        self.label.configure(text=str(self.default_hex_color))
        #self.textbox.set_content_to(self.default_hex_color)

        if self.brightness_slider_value.get() < 70:
            self.label.configure(text_color="white")
        else:
            self.label.configure(text_color="black")

        if str(self.label._fg_color) == "black":
            self.label.configure(text_color="white")

    @staticmethod
    def projection_on_circle(point_x, point_y, circle_x, circle_y, radius):
        angle = math.atan2(point_y - circle_y, point_x - circle_x)
        projection_x = circle_x + radius * math.cos(angle)
        projection_y = circle_y + radius * math.sin(angle)

        return projection_x, projection_y

    def set_initial_color(self, initial_color):
        # set_initial_color is in beta stage, cannot seek all colors accurately

        if initial_color and initial_color.startswith("#"):
            try:
                r, g, b = tuple(int(initial_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                return

            self.default_hex_color = initial_color
            for i in range(0, self.image_dimension):
                for j in range(0, self.image_dimension):
                    self.rgb_color = self.img1.getpixel((i, j))
                    if (self.rgb_color[0], self.rgb_color[1], self.rgb_color[2]) == (r, g, b):
                        self.canvas.create_image(i, j, image=self.target)
                        self.target_x = i
                        self.target_y = j
                        return

        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.target)

    def set_color(self, code):
        if code and code.startswith("#"):
            try:
                r, g, b = tuple(int(code.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                return

            self.update_colors2(code)

            def color_dist(rgb1, rgb2):
                rmean = (rgb1[0] + rgb2[0]) / 2
                r = rgb1[0] - rgb2[0]
                g = rgb1[1] - rgb2[1]
                b = rgb1[2] - rgb2[2]
                return (((512 + rmean) * r * r) / 256 + 4 * g * g + ((767 - rmean) * b * b) / 256) ** 0.5

            def refresh():
                self.canvas.delete("all")
                self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)

                d_from_center = math.sqrt(
                    ((self.image_dimension / 2) - self.target_x) ** 2 + (
                            (self.image_dimension / 2) - self.target_y) ** 2)

                if d_from_center < self.image_dimension / 2:
                    self.target_x, self.target_y = self.target_x, self.target_y
                else:
                    self.target_x, self.target_y = self.projection_on_circle(self.target_x, self.target_y,
                                                                             self.image_dimension / 2,
                                                                             self.image_dimension / 2,
                                                                             self.image_dimension / 2 - 1)

                self.canvas.create_image(self.target_x, self.target_y, image=self.target)

                # self.get_target_color()
                # self.update_colors()

            if code.startswith(self.curr_code.lower()):
                return
            self.curr_code = code

            # edge case
            if code.startswith("#ffffff"):
                self.target_x = self.image_dimension / 2
                self.target_y = self.image_dimension / 2
                refresh()
                return

            # self.default_hex_color = color
            for i in range(0, self.image_dimension):
                for j in range(0, self.image_dimension):
                    self.rgb_color = self.img1.getpixel((i, j))
                    # print([r, g, b])
                    # print([i, j])
                    # print(self.rgb_color[0:3])
                    # luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
                    # This is the shading value
                    # print(r * luma / 255, g * luma / 255, b * luma / 255)
                    # print(rgb_to_hsv(r, g, b))
                    # print(convert_to_value_100_rgb(r, g, b))
                    if color_dist(self.rgb_color[0:3], convert_to_value_100_rgb(r, g, b)) < 3:
                        self.target_x = i
                        self.target_y = j
                        refresh()
                        # print([r, g, b])
                        # luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
                        # print(luma)
                        break


if __name__ == "__main__":
    app = AskColor()
    app.mainloop()
