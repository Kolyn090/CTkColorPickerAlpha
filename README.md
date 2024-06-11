# CTkColorPickerAlpha
**A special color picker that supports picking transparent color (8-digits hex code)**

![default](https://github.com/Kolyn090/CTkColorPickerAlpha/blob/main/readme_img/screenshot-ui.png?raw=true)
![colored](https://github.com/Kolyn090/CTkColorPickerAlpha/blob/main/readme_img/screenshot-color.png?raw=true)

## Download

```
pip install ctk-color-picker-alpha
```

## Requirements
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [pillow](https://pypi.org/project/Pillow/)
- [numpy](https://numpy.org)

### How to use?

```python
import customtkinter as ctk
from ctk_color_picker_alpha import *


def ask_color():
    pick_color = AskColor()  # open the color picker
    color = pick_color.get()  # get the color string
    button.configure(fg_color=color)


root = ctk.CTk()

button = ctk.CTkButton(master=root, text="CHOOSE COLOR", text_color="black", command=ask_color)
button.pack(padx=30, pady=20)
root.mainloop()
```

## Options
| Arguments                   | Description                                                                                                   |
|-----------------------------|---------------------------------------------------------------------------------------------------------------|
| width                       | set the overall size of the color picker window, always greater than 300 pixels                               |
| title                       | change the title of color picker window                                                                       |
| fg_color                    | change foreground color of the color picker frame                                                             |
| bg_color                    | change background color of the color picker frame                                                             |
| button_color                | change the color of the button and slider                                                                     |
| button_hover_color          | change the hover color of the buttons                                                                         |
| text                        | change the default text of the 'OK' button                                                                    |
| initial_color               | set the default color of color picker (currently in beta stage)                                               |
| slider_border               | change the border width of slider                                                                             |
| corner_radius               | change the corner radius of all the widgets inside color picker                                               |
| enable_previewer            | if True, display the color previewer                                                                          |
| enable_alpha                | if True, enable 8-digits hex code and transparency. Otherwise, use 6-digits hex code and disable transparency |
| allow_hexcode_modification  | if True, enable modifications to hex code textbox                                                             |
| enable_random_button        | if True, display the 'Random' button                                                                          |
| _**other button parameters_ | pass other button arguments if required                                                                       |

# ColorPickerWidget
**This is a new color picker widget that can be placed inside a customtkinter frame.**

![widget](https://github.com/Kolyn090/CTkColorPickerAlpha/blob/main/readme_img/screenshot-widget.png?raw=true)

### Usage

```python
from ctk_color_picker_alpha import *
import customtkinter

root = customtkinter.CTk()
colorpicker = CTkColorPicker(master=root)
colorpicker.pack(padx=10, pady=10)
root.mainloop()
```

## Options
| Arguments                   | Description                                                                                                   |
|-----------------------------|---------------------------------------------------------------------------------------------------------------|
| master                      | parent widget                                                                                                 |
| width                       | set the overall size of the color picker window, always greater than 300 pixels                               |
| title                       | change the title of color picker window                                                                       |
| fg_color                    | change foreground color of the color picker frame                                                             |
| bg_color                    | change background color of the color picker frame                                                             |
| button_color                | change the color of the button and slider                                                                     |
| button_hover_color          | change the hover color of the buttons                                                                         |
| text                        | change the default text of the 'OK' button                                                                    |
| initial_color               | set the default color of color picker (currently in beta stage)                                               |
| slider_border               | change the border width of slider                                                                             |
| corner_radius               | change the corner radius of all the widgets inside color picker                                               |
| enable_previewer            | if True, display the color previewer                                                                          |
| enable_alpha                | if True, enable 8-digits hex code and transparency. Otherwise, use 6-digits hex code and disable transparency |
| allow_hexcode_modification  | if True, enable modifications to hex code textbox                                                             |
| enable_random_button        | if True, display the 'Random' button                                                                          |
| _**other button parameters_ | pass other button arguments if required                                                                       |

**Forked from https://github.com/Akascape/CTkColorPicker**
