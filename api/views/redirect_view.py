from django.db.models import F
from django.shortcuts import get_object_or_404, redirect

from api.models import ShortUrl


def redirect_view(request, short_code):
    short_url = get_object_or_404(ShortUrl, short_url=short_code)
    # 更新短链跳转次数，原子化操作，防止并发问题
    # 例子： FileRecord.objects.filter(pk=file_id).update(count=F('count') + 1)
    ShortUrl.objects.filter(pk=short_url.pk).update(count=F('count') + 1)
    return redirect(short_url.long_url)
