# encoding:utf-8
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

numbers = ''.join(map(str, range(10)))  # map将str作用于后面序列的每一个元素
_chars = ''.join((numbers))


def create_validate_code(size=(120, 30), chars=_chars, mode='RGB', bg_color=(255, 255, 255), fg_color=(255, 0, 0),
                         font_size=18, font_type="arial.ttf", length=4, draw_points=True, point_chance=2):
    '''
    :param size: 图片的大小（宽，高）默认120,30
    :param chars: 允许的字符集合，格式字符串
    :param mode: 图片格式，默认RGB
    :param bg_color: 背景色，默认为白色
    :param fg_color: 前景色，验证码字符颜色
    :param font_size: 验证码字体大小
    :param font_type: 验证码字体
    :param length: 验证码字符个数
    :param draw_points: 是否画干扰点
    :param point_chance: 干扰点出现频率，大小范围[0,50]
    :return:
    '''
    width, height = size
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)

    def create_point():
        chance = min(50, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        c_chars = random.sample(chars, length)  # 从指定内容中生成指定长度的list
        strs = '%s' % ''.join(c_chars)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 3, (height - font_height) / 4), strs, font=font, fill=fg_color)
        return strs

    if draw_points:
        create_point()

    strs = create_strs()
    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500, 0.001, float(random.randint(1, 2)) / 500]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    return img, strs
