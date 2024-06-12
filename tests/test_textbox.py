import unittest
from ctk_color_picker_alpha.components.my_ctk_components import HexCustomCTkTextbox
import tkinter as tk
import customtkinter
from pyautogui import press

# def set_focus(m_textbox):
#     print("Hello")
#     entry = tk.Entry(m_textbox)
#     # entry.pack()
#     entry.grid(row=0, column=0)
#     # entry.focus_set()
#     # print(m_textbox.focus_get())
#     print("World")
#
#
# def handle_focus(event):
#     print("return: event.widget is", event.widget)
#     print("focus is:", textbox.focus_get())
#     press('f')


# root = customtkinter.CTk()
# textbox = HexCustomCTkTextbox(master=root, set_color=set_color, is_alpha=True)
# textbox.pack(padx=10, pady=10)
# set_focus(textbox)
#
# root.bind("<Enter>", handle_focus)
#
# root.mainloop()


class TestHexTextbox(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_code = "#ffffffff"

    def set_color(self, code):
        self.current_code = code

    def test_widget_creation(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        self.assertIsInstance(textbox, HexCustomCTkTextbox)

    def test_textbox_set_content(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        textbox.set_content_to("#12345678")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#12345678")


class TestSetContent(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_code = "#ffffffff"

    def set_color(self, code):
        self.current_code = code

    def test_invalid_code(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        textbox.set_content_to("")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#ffffffff")
        textbox.set_content_to("#")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#ffffffff")

    def test_5bits_invalid_code(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        textbox.set_content_to("#12345")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#12345fff")

    def test_6bits_valid_code(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        textbox.set_content_to("#123456")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#123456ff")
        textbox.set_content_to("#bbbBBB")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#bbbbbbff")

    def test_8bits_valid_code(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        textbox.set_content_to("#12345678")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#12345678")
        textbox.set_content_to("#d5e5fcff")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#d5e5fcff")
        textbox.set_content_to("#1b9E3500")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#1b9e3500")

    def test_8bits_invalid_code(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        textbox.set_content_to("#wq1234hf")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#1234ffff")
        textbox.set_content_to("#hello WORLD")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#edffffff")
        textbox.set_content_to("#kolyn090")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#090fffff")

    def test_10bits_invalid_code(self):
        root = customtkinter.CTk()
        textbox = HexCustomCTkTextbox(master=root,
                                      set_color=self.set_color,
                                      is_alpha=True)
        textbox.set_content_to("#1234567890")
        textbox.on_key_released()
        self.assertEqual(self.current_code, "#12345678")
        self.assertNotEqual(self.current_code, "1234567890")
