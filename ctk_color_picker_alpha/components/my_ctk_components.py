import string
import customtkinter
from PIL import Image
import numpy
import os


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IMAGES = [
    'transparent_background.png'
]


class HexCustomCTkTextbox(customtkinter.CTkTextbox):
    # Test variables, copy-paste these into the textbox
    # Valid:
    #    #d5e5fcff
    #    #bc865aaa
    #    #9C36A77f
    #    #1b9E3500
    # Invalid but attempt to convert to hex:
    #    #wq1234hf   -> #1234f
    #    #@f$r23af   -> #f23af
    #    hello WORLD -> #ed
    #    #kolyn090   -> #090

    """
    | A custom ctk textbox that is specialized to receive hex code
    | text input. Allows the user to directly copy from the
    | hex code from textfield. Handles invalid inputs both from
    | typing and pasting. All lower case.
    """

    def __init__(self, set_color, is_alpha=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_color = set_color
        self.max_len = 9 if is_alpha else 7
        self.bind("<KeyRelease>", self.on_key_released)
        my_font = customtkinter.CTkFont(family="Courier", size=12)
        self.configure(font=my_font)

    def set_content_to(self, text):
        """
        |  Set content to given text
        :param text: String
        :return: Void
        """

        # Deletes the entire content
        self.delete(1.0, "end")
        # assign text to content
        self.insert("end-1c", text)

    def on_key_released(self, event=None):
        """
        |  Called each time the user releases a key.
        |  On release, do the following:
        |    1. Validifies the current content in the following ways:
        |    2. After validification, convert content to code and change
        |  the color of palette to code. Fill missing characters in
        |  code with 'f'. The content is not modified during this process.
        :param event: Event for key-binding
        :return: Void
        """

        def validify_content():
            """
            |  Validifies the current content in the following ways:
            |    1. each character in the content must be hex ('0' - 'f')
            |       except the first hashtag
            |    2. the storing content always starts with a hashtag
            |    3. the storing content must be one line
            |    4. the string content cannot exceed max_len characters
            :return: Void
            """

            # Save the current text cursor position
            cursor_pos = self.index(customtkinter.INSERT).split(".")[1]

            # 1. each character in the content must be hex ('0' - 'f')
            #    except the first hashtag. Delete any character that is not
            #    ('0' - 'f') except the first hashtag
            curr_content = self.get('1.0', "end-1c")
            table = str.maketrans(dict.fromkeys('0123456789abcdefABCDEF'))
            if not all(c in string.hexdigits for c in curr_content):
                s_ = curr_content.translate(table)
                s = curr_content.translate(str.maketrans(dict.fromkeys(s_)))
                if len(curr_content) == 0 or curr_content[:1] != '#':
                    s = '#' + s
                curr_content = s
                self.set_content_to(curr_content.lower())

            # 2. the storing content always starts with a hashtag
            if len(curr_content) == 0 or curr_content[:1] != '#':
                curr_content = '#' + curr_content
                self.set_content_to(curr_content.lower())

            # 3. the storing content must be one line
            if "\n" in curr_content:
                curr_content = curr_content.split("\n")[0]
                self.set_content_to(curr_content.lower())

            # 4. the string content cannot exceed max_len characters
            if len(curr_content) > self.max_len:
                curr_content = curr_content[0:self.max_len]
                self.set_content_to(curr_content.lower())

            # Revert the cursor position
            self.mark_set("insert", "%d.%d" % (1, int(cursor_pos)))

        def change_palette_color():
            """
            |  Convert content to code and change the color of palette to code.
            |  Fill missing characters in code with 'f'. The content is not
            |  modified during this process.
            :return: Void
            """
            curr_content = self.get('1.0', "end-1c")
            code = curr_content.ljust(self.max_len, 'f')
            self.set_color(code)
            # print("change color to " + code)

        validify_content()
        change_palette_color()

    def on_focus_lost(self, event=None):
        """
        |   Called each time focus is lost on this component.
        |   On lost, do the following:
        |     1. fill 'f' for missing characters
        :param event: Event for key-binding
        :return: Void
        """
        curr_content = self.get('1.0', "end-1c")
        # content must have max_len characters
        # if not, fill the missing ones with 'f'
        curr_content = curr_content.ljust(self.max_len, 'f')
        self.set_content_to(curr_content)


class ColorPreviewer(customtkinter.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def make_default_trans_bg_arr():
            def resize_array(arr):
                return arr.repeat(2, axis=0).repeat(2, axis=1)

            pic = Image.open(os.path.join(parent_dir, IMAGES[0]))
            result = numpy.array(pic)
            result = resize_array(result)
            result = resize_array(result)
            result = resize_array(result)
            result = resize_array(result)

            return result

        self.pix = make_default_trans_bg_arr()
        trans_bg_img = Image.fromarray(self.pix)
        self.configure(image=customtkinter.CTkImage(trans_bg_img, size=trans_bg_img.size),
                       text="")

    def render_with_hex(self, hex_code, a):
        if hex_code and hex_code.startswith("#"):
            try:
                r, g, b = tuple(int(hex_code.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                self.render_with(r, g, b, a)
            except ValueError:
                return

    def render_with(self, r, g, b, a):
        def blended_color(source, target, m_strength):
            def blend_element(e):
                return [round((1 - m_strength) * e[0] + m_strength * target[0]),
                        round((1 - m_strength) * e[1] + m_strength * target[1]),
                        round((1 - m_strength) * e[2] + m_strength * target[2]),
                        255]

            return numpy.array([blend_element(si) for si in source])

        re_render_arr = numpy.array([blended_color(xi, [r, g, b], a/255) for xi in self.pix]).astype(numpy.uint8)
        re_render_img = Image.fromarray(re_render_arr)

        self.configure(image=customtkinter.CTkImage(re_render_img, size=re_render_img.size),
                       text="")
