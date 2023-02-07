from fractions import Fraction
from PIL import Image, ImageDraw, ImageFont
import PIL
import os
fontPath = "/System/Library/Fonts/"
bold_font = os.path.join(fontPath, "Supplemental/Arial Bold.ttf")
regular_font = os.path.join(fontPath, "Supplemental/Arial.ttf")
# Supplemental/
scale = 10
benchmark_bold_font_size = 18
benchmark_regular_font_size = 12
benchmark_width = 800
benchmark_padding = 24
benchmark_margin = 8
sony = Image.open('./logo/sony.png').convert("RGBA")


def create_watermark(im_target, exif):
    device_type = exif.get('Model')
    time = exif.get('DateTimeOriginal')
    metadata = str(exif.get('FocalLength')) + 'mm ' + 'f/' + str(exif.get('FNumber')) + ' ' + str(Fraction(exif.get('ExposureTime'))) + ' ISO ' + str(exif.get('ISOSpeedRatings'))
    print(metadata)
    t_size = im_target.size
    scale = t_size[0] // benchmark_width
    bold_font_size =  scale * benchmark_bold_font_size
    regular_font_size =  scale * benchmark_regular_font_size
    margin = scale * benchmark_margin
    padding = scale * benchmark_padding
    b_font = ImageFont.truetype(bold_font, bold_font_size)
    r_font = ImageFont.truetype(regular_font, regular_font_size)
    device_type_textsize = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text = device_type, font=b_font) ## 拿到字体大小 计算白边高度
    time_textsize = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text = time, font=r_font)
    metadata_textsize = ImageDraw.Draw(Image.new("RGB", (1, 1))).textsize(text = metadata, font=b_font)
    im_white = Image.new('RGBA', size=(t_size[0], device_type_textsize[1] + padding * 2 + time_textsize[1] + margin), color=(255, 255, 255))
    im_white_draw = ImageDraw.Draw(im_white)
    # device
    im_white_draw.text((padding, padding), device_type, fill=(0, 0, 0), font=b_font)
    # time
    im_white_draw.text((padding, padding + device_type_textsize[1] + margin), time, fill=(170, 170, 170), font=r_font)
    # metadata
    metadata_x = t_size[0] - metadata_textsize[0] - padding
    metadata_y = padding + metadata_textsize[1] // 2
    im_white_draw.text((metadata_x, metadata_y), metadata, fill=(0, 0, 0), font=b_font)
    # line scale 线条宽度
    line_x = metadata_x - margin - scale
    im_white_draw.line((line_x, padding, line_x, im_white.size[1] - padding), fill=(221, 221, 221), width=2*scale)
    im_white__logo_height = im_white.size[1] - padding * 2
    im_white__logo_width = sony.size[0] // sony.size[1] * im_white__logo_height
    # 0.6 sony logo 调整系数
    sony_resized = sony.resize((int(im_white__logo_width), int (im_white__logo_height)), Image.LANCZOS)
    # 第三个参数蒙版 让 sony 背景变透明
    sony_x = metadata_x - margin * 2 - sony_resized.size[0]
    sony_y =  padding
    im_white.paste(sony_resized, (sony_x, sony_y), sony_resized)

    return im_white


def create_white(im, name, output_path): 
    x, y = im.size
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    white = create_watermark(im, exif)
    target = Image.new('RGB', size=(x, y + white.size[1]), color=(255, 255, 255))
    # white.show()
    target.paste(im, (0, 0))
    target.paste(white, (0, y))
    op = output_path or './output/'
    print(op)
    target.save(op + name, quality=80)

if __name__ == '__main__':
    create_white()


