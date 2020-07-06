""" Utils """

import arabic_reshaper
from bidi.algorithm import get_display


def persian(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))


    FONTS = {
        'vazir': 'Vazir.ttf',
        'bvaizr': 'Vazir-Bold.ttf'
    }

    BACKGROUND_COLOR = {
        'white': (255, 255, 255),
        'blue': (36,52,71),
    }

