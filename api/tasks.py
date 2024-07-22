# myapp/tasks.py
import logging
from io import BytesIO
from urllib.parse import urlparse

import PIL
import chardet
import requests
from PIL import Image, ImageFilter
from bs4 import BeautifulSoup
from celery import shared_task
from django.core.files.base import ContentFile

from api.models import HyperLinkCache

logger = logging.getLogger('celery')


@shared_task
def fetch_page_info_task(task_id):
    hyper_link_cache = HyperLinkCache.objects.get(id=task_id)
    url = hyper_link_cache.url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }

    response = requests.get(url, headers=headers, timeout=3)
    response.raise_for_status()
    # 检测页面编码并设置正确的编码
    detected_encoding = chardet.detect(response.content)['encoding']
    response.encoding = detected_encoding
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No title found'
    description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={
        'name': 'description'}) else 'No description found'
    icon_link = soup.find('link', rel='icon')['href'] if soup.find('link', rel='icon') else None

    hyper_link_cache.title = title
    hyper_link_cache.desc = description

    try:
        if not icon_link.startswith(('http://', 'https://')):
            parsed_url = urlparse(url)
            icon_link = parsed_url.scheme + "://" + parsed_url.netloc + "/" + icon_link

        icon_response = requests.get(icon_link, headers=headers, timeout=3)
        icon_name = icon_link.split("/")[-1]
        logger.info(f"Icon found for {url}: {icon_name}")
        hyper_link_cache.icon.save(icon_name, ContentFile(icon_response.content), save=False)
        # 将响应内容转换为BytesIO对象
        icon_data = BytesIO(icon_response.content)
        # 使用PIL打开图片
        icon_image = Image.open(icon_data)
        # 获取主色调
        color = get_dominant_color(icon_image)
        # 取前7位
        color = color[:7]
        hyper_link_cache.color = color
        hyper_link_cache.finished = True
    except PIL.UnidentifiedImageError as e:
        logger.warning(f"cannot identify image file: {icon_link}; {e}")
        hyper_link_cache.finished = True
        hyper_link_cache.color = "#f2f2f2"

    hyper_link_cache.save()


def rgba_to_hex(rgba):
    return '#{:02x}{:02x}{:02x}{:02x}'.format(rgba[0], rgba[1], rgba[2], rgba[3])


def lighten_color(rgba, factor=0.5):
    r, g, b, a = rgba
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return r, g, b, a


def get_dominant_color(img: Image):
    # 将图像进行极度模糊处理
    width, height = img.size
    radius = min(width, height) // 10  # 模糊半径为较小边长的10%
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=radius))
    # 获取模糊图像的像素数据
    pixels = blurred_img.getdata()
    # 初始化颜色累加器
    r_total, g_total, b_total, a_total = 0, 0, 0, 0
    num_pixels = len(pixels)
    # 累加所有像素的颜色值
    for pixel in pixels:
        if len(pixel) == 4:  # RGBA
            r, g, b, a = pixel
        else:  # RGB
            r, g, b = pixel
            a = 255
        r_total += r
        g_total += g
        b_total += b
        a_total += a
    # 计算平均颜色值
    r_avg = r_total // num_pixels
    g_avg = g_total // num_pixels
    b_avg = b_total // num_pixels
    a_avg = a_total // num_pixels
    # 调整颜色使其变淡
    dominant_color = lighten_color((r_avg, g_avg, b_avg, a_avg))
    # 转换为16进制颜色值
    return rgba_to_hex(dominant_color)
