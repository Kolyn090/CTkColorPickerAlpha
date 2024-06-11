# CTk Color Picker widget for customtkinteralpha
# Author: Kolyn Lin (Kolyn090), Akash Bora (Akascape)

import tkinter
import random

import customtkinter
from PIL import Image, ImageTk
import sys
import os
import math
from ctk_color_picker_alpha.components import HexCustomCTkTextbox, ColorPreviewer
from ctk_color_picker_alpha.util import rgb_to_hsv, convert_to_value_100_rgb

# PATH = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IMAGES = [
    'target.png',
    'color_wheel.png',
]


class CTkColorPicker(customtkinter.CTkFrame):

    def __init__(self, master: any = None, width: int = 300, initial_color: str = None,
                 bg_color: str = None, fg_color: str = None, button_color: str = None, button_hover_color: str = None,
                 text: str = "OK", corner_radius: int = 24, slider_border: int = 1, enable_previewer: bool = True,
                 enable_alpha: bool = True, allow_hexcode_modification: bool = True, enable_random_button: bool = True,
                 **button_kwargs):

        # self.title(title)
        super().__init__(master=master,
                         corner_radius=corner_radius)
        WIDTH = width if width >= 300 else 300
        HEIGHT = WIDTH - 200
        self.image_dimension = int(self._apply_widget_scaling(WIDTH - 100))
        self.target_dimension = int(self._apply_widget_scaling(20))
        self.target_y = self.image_dimension / 2
        self.target_x = self.image_dimension / 2
        # self.maxsize(WIDTH, HEIGHT)
        # self.minsize(WIDTH, HEIGHT)
        # self.resizable(width=False, height=False)
        # self.transient(self.master)
        self.lift()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.after(10)
        # self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.enable_alpha = enable_alpha
        self.allow_hexcode_modification = allow_hexcode_modification
        self.curr_code = "#ffffffff" if enable_alpha else "#ffffff"
        self.default_hex_color = "#ffffffff" if enable_alpha else "#ffffff"
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

        self.configure(fg_color=self.fg_color)
        self.ok_button_text = text
        self.corner_radius = corner_radius
        self.slider_border = 10 if slider_border >= 10 else slider_border
        self.frame = customtkinter.CTkFrame(master=self, fg_color=self.fg_color, bg_color=self.bg_color)
        self.frame.grid(padx=20, pady=20, sticky="nswe")
        self.canvas = tkinter.Canvas(self.frame, height=self.image_dimension, width=self.image_dimension,
                                     highlightthickness=0, bg=self.fg_color)
        self.canvas.pack(pady=20)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        def open_image(img_name, d):
            return Image.open(os.path.join(parent_dir, img_name)).resize((d, d), Image.Resampling.LANCZOS)

        self.img1 = open_image(IMAGES[1], self.image_dimension)
        self.img2 = open_image(IMAGES[0], self.target_dimension)
        self.wheel = ImageTk.PhotoImage(self.img1)
        self.target = ImageTk.PhotoImage(self.img2)
        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)
        self.set_initial_color(initial_color)
        self.stack1 = customtkinter.CTkFrame(master=self.frame, fg_color='transparent')
        self.stack2 = customtkinter.CTkFrame(master=self.frame, fg_color='transparent')

        def create_brightness_slider_and_value(parent):
            brightness_slider_value = customtkinter.IntVar()
            brightness_slider_value.set(255)
            brightness_slider = customtkinter.CTkSlider(master=parent, height=20, border_width=self.slider_border,
                                                        button_length=15, progress_color=self.default_hex_color[:7],
                                                        from_=0, to=255,
                                                        variable=brightness_slider_value, number_of_steps=256,
                                                        button_corner_radius=self.corner_radius,
                                                        corner_radius=self.corner_radius,
                                                        button_color=self.button_color,
                                                        button_hover_color=self.button_hover_color,
                                                        command=lambda x: self.update_colors())
            brightness_slider.pack(fill="both", pady=(0, 15), padx=20 - self.slider_border)
            return brightness_slider, brightness_slider_value

        def create_alpha_slider_and_value(parent):
            alpha_slider_value = customtkinter.IntVar()
            alpha_slider_value.set(255)
            alpha_slider = customtkinter.CTkSlider(master=parent, height=20, border_width=self.slider_border,
                                                   button_length=15, progress_color="#ffffff",
                                                   from_=0, to=255,
                                                   variable=alpha_slider_value, number_of_steps=256,
                                                   button_corner_radius=self.corner_radius,
                                                   corner_radius=self.corner_radius,
                                                   button_color=self.button_color,
                                                   button_hover_color=self.button_hover_color,
                                                   command=lambda x: self.update_colors(), bg_color='transparent',
                                                   border_color='transparent')
            alpha_slider.pack(fill="both", pady=(0, 15), padx=20 - self.slider_border)
            return alpha_slider, alpha_slider_value

        def create_color_previewer(parent):
            previewer = ColorPreviewer(master=parent, corner_radius=self.corner_radius)
            previewer.pack(fill="both", padx=0, pady=5, side='left')
            previewer.render_with_hex(self.default_hex_color, 255)
            return previewer

        def create_hex_textbox(parent):
            hex_textbox = HexCustomCTkTextbox(master=parent,
                                              height=50,
                                              set_color=self.set_color,
                                              is_alpha=enable_alpha,
                                              fg_color=self.default_hex_color[:7],
                                              text_color='#000000',
                                              corner_radius=self.corner_radius)
            hex_textbox.pack(fill="both", padx=0, pady=5, side='right')
            hex_textbox.insert("end-1c", "#")
            if not self.allow_hexcode_modification:
                hex_textbox.configure(state='disable')

            return hex_textbox

        def create_random_button(parent):
            random_button = customtkinter.CTkButton(master=parent, text="Random",
                                                    height=50,
                                                    corner_radius=self.corner_radius, fg_color=self.button_color,
                                                    hover_color=self.button_hover_color, command=self._random_event,
                                                    **button_kwargs)
            random_button.pack(fill="both", padx=5, pady=10, side='left')
            return random_button

        def create_ok_button(parent):
            ok_button = customtkinter.CTkButton(master=parent, text=self.ok_button_text,
                                                height=50,
                                                corner_radius=self.corner_radius, fg_color=self.button_color,
                                                hover_color=self.button_hover_color, command=self._ok_event,
                                                **button_kwargs)
            ok_button.pack(fill="both", padx=5, pady=10, side='right')
            return ok_button

        # --- Here is where all essential components are created ---
        (self.brightness_slider, self.brightness_slider_value) = create_brightness_slider_and_value(self.frame)
        (self.alpha_slider, self.alpha_slider_value) = create_alpha_slider_and_value(self.frame)
        self.previewer = create_color_previewer(self.stack1)
        self.hex_textbox = create_hex_textbox(self.stack1)
        self.random_button = create_random_button(self.stack2)
        self.ok_button = create_ok_button(self.stack2)
        # --- Here is where all essential components are created ---

        if not self.enable_alpha:
            self.alpha_slider.pack_forget()
            self.hex_textbox.pack(pady=20)
        if not enable_previewer:
            self.previewer.pack_forget()
            self.hex_textbox.pack(side="top")
        if not enable_random_button:
            self.random_button.pack_forget()
            self.ok_button.pack(side="top")

        self.update_hexbox_label(self.default_hex_color)
        self.stack2.pack(fill="both", pady=0, side="bottom")
        self.stack1.pack(fill="both", pady=0)
        self.grab_set()

    def get(self):
        self.master.wait_window(self)
        return self.curr_code

    def _ok_event(self, event=None):
        self.grab_release()
        self.destroy()
        del self.img1
        del self.img2
        del self.wheel
        del self.target

    def _random_event(self, event=None):
        def generate_random_color():
            def random_hex_255():
                result = hex(random.randint(0, 255))[2:]
                if len(result) < 2:
                    result = "0" + result
                return result

            return ("#" + random_hex_255() +
                    random_hex_255() +
                    random_hex_255() +
                    (random_hex_255() if self.enable_alpha else ''))

        new_color = generate_random_color()
        self.set_color(new_color)
        self.update_hexbox_label(new_color)

    def _on_closing(self):
        self.curr_code = None
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

    def update_hexbox_label(self, content):
        if not self.allow_hexcode_modification:
            self.hex_textbox.configure(state='normal')
            self.hex_textbox.set_content_to(content)
            self.hex_textbox.configure(state='disable')
        else:
            self.hex_textbox.set_content_to(content)

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
        alpha = self.alpha_slider_value.get()
        self.get_target_color()
        r = int(self.rgb_color[0] * (brightness / 255))
        g = int(self.rgb_color[1] * (brightness / 255))
        b = int(self.rgb_color[2] * (brightness / 255))
        self.rgb_color = [r, g, b]
        self.default_hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
        self.brightness_slider.configure(progress_color=self.default_hex_color)

        def determine_alpha_slider_color_value():
            color = hex(alpha)[2:]
            if len(color) < 2:
                color = "0" + color
            return "#" + color + color + color

        self.alpha_slider.configure(progress_color=determine_alpha_slider_color_value())
        self.previewer.render_with_hex(self.default_hex_color, alpha)

        def get_alpha():
            result = hex(alpha)[2:]
            if len(result) < 2:
                result = "0" + result
            return result

        self.update_hexbox_label(self.default_hex_color + (get_alpha() if self.enable_alpha else ''))

    def update_colors2(self, code):
        r, g, b = tuple(int(code.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
        hsv = rgb_to_hsv(r, g, b)
        self.brightness_slider_value.set(hsv[2] * 255 / 100)
        self.rgb_color = [r, g, b]
        self.default_hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
        self.brightness_slider.configure(progress_color=self.default_hex_color)

        def get_strength():
            return int("0x" + code[7:], 0)

        def determine_alpha_slider_color():
            color = code[7:]
            if len(color) == 0:
                color = "ff"
            elif len(color) == 1:
                color = "f" + color
            return color

        def determine_alpha_slider_color_value():
            color = determine_alpha_slider_color()
            return "#" + color + color + color

        self.previewer.render_with_hex(self.default_hex_color, get_strength() if self.enable_alpha else 255)

        if self.enable_alpha:
            self.alpha_slider.configure(progress_color=determine_alpha_slider_color_value())
            self.alpha_slider_value.set(int("0x" + determine_alpha_slider_color(), 0))

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
                    if color_dist(self.rgb_color[0:3], convert_to_value_100_rgb(r, g, b)) < 3:
                        self.target_x = i
                        self.target_y = j
                        refresh()
                        break
