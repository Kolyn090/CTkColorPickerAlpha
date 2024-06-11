from ctk_color_picker_alpha.widget.ctk_color_picker_widget import CTkColorPicker
import customtkinter


if __name__ == "__main__":
    # print(rgb_to_hsv(68, 68, 68))
    # print(hsv_to_rgb(0, 0, 27))
    # print(convert_to_value_100_rgb(97, 48, 48))
    root = customtkinter.CTk()
    colorpicker = CTkColorPicker(master=root)
    colorpicker.pack(padx=10, pady=10)
    root.mainloop()
