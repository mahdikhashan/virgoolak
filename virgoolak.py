import os
import textwrap
from PIL import (Image,
                 ImageFont,
                 ImageDraw,
                 ImageOps)

from virgool import Virgool
from reshape.reshape import persian


URL = "https://virgool.io/startup-playbook/%D8%AE%D8%AF%D9%85%D8%A7%D8%AA-%D9%85%D8%B4%D8%AA%D8%B1%DB%8C-%D8%AE%D9%88%D8%A8-%D8%A8%D8%B1%D8%A7%DB%8C-%DA%A9%D8%A7%D8%B1%D8%A8%D8%B1%D8%A7%D9%86-%D8%A7%D9%88%D9%84%DB%8C%D9%87-%D8%AC%D8%B0%D8%A7%D8%A8-%D8%A7%D8%B3%D8%AA-vvbt16lmu68v"

virgool = Virgool(URL)


img = Image.new('RGB', (600, 600), color=(36,52,71))
# img.save('back.png')

# img = Image.open('rback.png')

fnt = ImageFont.truetype('Vazir-Bold.ttf', 23)
fnt2 = ImageFont.truetype('Vazir.ttf', 15)
fnt3 = ImageFont.truetype('Vazir-Bold.ttf', 30)
d = ImageDraw.Draw(img)

name = virgool.get_name()
# reshaped_name = arabic_reshaper.reshape(name)
# bidi_name = get_display(reshaped_name)

bio = virgool.get_bio()
# reshaped_bio = arabic_reshaper.reshape(bio)
# bidi_bio = get_display(reshaped_bio)

title = virgool.get_title()
# reshaped_title = arabic_reshaper.reshape(title)
# bidi_title = get_display(reshaped_title)

d.text((600-fnt.getsize(persian(virgool.get_name()))[0]-190, 95),
        persian(virgool.get_name()),
        font=fnt, fill=(223, 230, 233))

if fnt2.getsize(persian(virgool.get_bio()))[0] > 48:
    nbidi_bio = persian(virgool.get_bio())[-48:]

d.text((600-fnt2.getsize(nbidi_bio)[0]-190, 130), nbidi_bio, font=fnt2, fill=(223, 230, 233))

title_lines = textwrap.wrap(title, width=32)
h = 190
for line in title_lines:
    text = persian(line)
    width, height = fnt3.getsize(text)
    d.text((600-width-90, h), text, font=fnt3, fill=(223, 230, 233))
    h += height

mask = Image.open('mask2.png').convert('L')
round_mask = Image.open('rback.png').convert('L')

avatar = Image.open(virgool.get_avatar())

poster = Image.open(virgool.get_poster())
poster = poster.resize((420, 250), Image.ANTIALIAS)


output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
output.putalpha(mask)
# output.save('masked.png')

# poutput = ImageOps.fit(poster, (50, 10), centering=(0.5, 0.5))
# poutput.putalpha(mask)

img.paste(output, (420, 75), mask)
img.paste(poster, (90, h+25))

img.save('vigoolak323.png')


from abc import ABCMeta, abstractmethod
import copy
from io import BytesIO


class Tag(metaclass = ABCMeta):
    """Tag"""
    def __init__(self, *args, **kwargs):
        self.id = None
        self.type = None
        self.font_default_size = 15
        self.font_small = 10
        self.font_medium = 25
        self.font_title = 30
        self.font_big = 40
        self.font_vazir = ImageFont.truetype('Vazir.ttf', self.font_medium)
        self.font_vazir_default = ImageFont.truetype('Vazir.ttf', self.font_default_size)
        self.font_vazir_bold = ImageFont.truetype('Vazir-Bold.ttf', self.font_medium)
        self.font_vazir_title = ImageFont.truetype('Vazir-Bold.ttf', self.font_title)
        self.background = None
        self.background_color = None
        self.background_round = False
        self.background_size = (600, 600)
        self.mask = None
        self.mask_small = Image.open(os.path.join(os.getcwd(), 'mask2.png')).convert('L')
        self.mask_medium = Image.open(os.path.join(os.getcwd(), 'mask3.jpg')).convert('L')
        self.mask_big = Image.open(os.path.join(os.getcwd(), 'mask3.png')).convert('L')
        self.avatar = None
        self.avatar_pos = (0, 0)
        self.name = None
        self.name_pos = (0, 0)
        self.name_font = self.font_vazir
        self.name_color = (0, 0, 0)
        self.title = None
        self.title_pos = (0, 0)
        self.title_font = None
        self.title_color = None
        self.title_multiline_height = 0
        self.username = None
        self.username_pos = (0, 0)
        self.username_color = None
        self.username_font = None
        self.bio = None
        self.bio_pos = (0, 0)
        self.bio_color = None
        self.bio_font = None
        self.poster = None
        self.poster_pos = (0, 0)
        self.poster_size = (420, 250)

    def set_background(self):
        return Image.new('RGB', self.background_size, self.background_color)

    def set_avatar(self):
        if self.avatar:
            output = ImageOps.fit(self.avatar, self.mask.size, centering=(0.5, 0.5))
            output.putalpha(self.mask)
            self.background.paste(output, self.avatar_pos, self.mask)
        else:
            return None

    def set_name(self):
        if self.name:
            drawable = ImageDraw.Draw(self.background)
            drawable.text(self.name_pos, self.name, font=self.name_font, fill=self.name_color)
        else:
            return None

    def set_bio(self):
        if self.bio:
            drawable = ImageDraw.Draw(self.background)
            drawable.text(self.bio_pos, self.bio, font=self.bio_font, fill=self.bio_color)
        else:
            return None

    def set_title(self, multiline=True):
        if self.title:
            if self.font_vazir_title.getsize(self.title)[0] > 32:
                title_lines = textwrap.wrap(self.title, width=32)
                h = 190
                title_lines.reverse()
                for line in title_lines:
                    text = persian(line)
                    width, height = self.font_vazir_title.getsize(text)
                    drawable = ImageDraw.Draw(self.background)
                    drawable.text((600-width-90, h), persian(text), font=self.font_vazir_title, fill=self.title_color)
                    h += height
                self.title_multiline_height = h
            else:
                drawable = ImageDraw.Draw(self.background)
                drawable.text(self.title_pos, persian(self.title), font=self.title_font, fill=self.title_color)
                self.title_multiline_height = 190 + 25
        else:
            return None

    def set_poster(self):
        if self.poster:
            poster = self.poster
            poster = poster.resize(self.poster_size, Image.ANTIALIAS)
            self.background.paste(poster, self.poster_pos)
        else:
            return None

    def clone(self):
        return copy.copy(self)

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def byte_array(self):
        pass


class Type1(Tag):
    def __init__(self, avatar, name, bio, title, poster, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = self.clone()
        self.obj.id = 1
        self.obj.type = "virgool"
        self.obj.background_size = (600, 600)
        self.obj.background_color = (36, 52, 71)
        self.obj.background = self.obj.set_background()
        self.obj.avatar = Image.open(avatar)
        self.obj.mask = self.obj.mask_small
        self.obj.avatar_pos = (420, 75)
        self.obj.set_avatar()
        self.obj.name = persian(name)
        self.obj.name_font = self.obj.font_vazir_bold
        self.obj.name_color = (223, 230, 233)
        self.obj.name_pos = (600-self.obj.name_font.getsize(self.obj.name)[0]-190, 95)
        self.obj.set_name()
        self.obj.bio = persian(bio)
        self.obj.bio_font = self.obj.font_vazir_default
        self.obj.bio_color = (223, 230, 233)
        self.obj.bio_pos = (600-self.obj.bio_font.getsize(self.obj.bio)[0]-190, 130)
        self.obj.set_bio()
        self.obj.title = persian(title)
        self.obj.title_font = self.obj.font_vazir_title
        self.obj.title_color = (223, 230, 233)
        self.obj.title_pos = (600-self.obj.title_font.getsize(self.obj.title)[0]-90, 190)
        self.obj.set_title(multiline=False)
        self.obj.poster = Image.open(poster)
        self.obj.poster_pos = (90, self.obj.title_multiline_height+25)
        self.obj.set_poster()

    def save(self):
        self.obj.background.save(os.path.join(os.getcwd(), 'sample_type2.png'))

    def byte_array(self):
        io = BytesIO()
        self.obj.background.save(io, format='PNG')
        return io.getvalue()


class Type2(Tag):
    def __init__(self, avatar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = 1
        self.type = "virgool"
        self.background_color = (0, 255, 0)
        self.background_size = (920, 1080)
        self.background = self.set_background()
        self.avatar = None #Image.open(avatar)
        self.mask = self.mask_big
        self.set_avatar()
        self.avatar_pos = (420, 75)

    def build(self):
        pass

    def save(self):
        self.background.save(os.path.join(os.getcwd(), 'sample2_type2.png'))

    def byte_array(self):
        io = BytesIO()
        self.background.save(io, format='PNG')
        return io.getvalue()


class Type3(Tag):
    def __init__(self, avatar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = self.clone()
        self.obj.id = 1
        self.obj.type = "virgool"
        self.obj.background_color = (255, 255, 255)
        self.obj.background_size = (128, 128)
        self.obj.background = self.obj.set_background()
        self.obj.avatar = None #Image.open(avatar)
        self.obj.mask = self.obj.mask_big
        self.obj.set_avatar()
        self.obj.avatar_pos = (420, 75)

    def build(self):
        pass

    def save(self, name: str = 'sample', format: str = 'PNG'):
        self.obj.background.save(os.path.join(os.getcwd(), name), format=format)

    def byte_array(self):
        io = BytesIO()
        self.obj.background.save(io, format='PNG')
        return io.getvalue()


if __name__ == "__main__":
    v = Virgool(URL)
    virgoolak1 = Type1(v.get_avatar(), v.get_name(), v.get_bio(), v.get_title())
    virgoolak1.save()
