"""
   Color class - rgb values as a string
"""


class Color:

    def __init__(self, rgb):
        self.rgb_hex = rgb

    def get_color_string(self):
        return self.rgb_hex
