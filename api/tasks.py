# myapp/tasks.py
import chardet
import requests
from bs4 import BeautifulSoup
from celery import shared_task
from django.core.files.base import ContentFile

from api.models import HyperLinkCache


@shared_task
def fetch_page_info_task(task_id):
    hyper_link_cache = HyperLinkCache.objects.get(id=task_id)
    url = hyper_link_cache.url

    try:
        response = requests.get(url, timeout=5)
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

        if icon_link:
            if not icon_link.startswith(('http://', 'https://')):
                icon_link = url + icon_link
            print("!!! " + icon_link)

            icon_response = requests.get(icon_link, timeout=5)
            if icon_response.status_code == 200:
                icon_name = icon_link.split("/")[-1]
                print(icon_name)
                hyper_link_cache.icon.save(icon_name, ContentFile(icon_response.content), save=False)

        hyper_link_cache.finished = True
    except Exception as e:
        print(e)
        hyper_link_cache.desc = f"Error: {str(e)}"
        hyper_link_cache.finished = True

    hyper_link_cache.save()
