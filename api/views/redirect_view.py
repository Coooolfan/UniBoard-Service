from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache


from api.models import ShortUrl


def redirect_view(request, short_code):
    cache_key = f"short_url_{short_code}"
    long_url = cache.get(cache_key)
    if long_url is None:
        long_url = get_object_or_404(ShortUrl, short_url=short_code).long_url
        cache.set(cache_key, long_url, 60)
    # TODO: 重构统计逻辑：在redis中使用原子操作递增计数，使用 qcluster 异步入库count
    # 更新短链跳转次数，原子化操作，防止并发问题
    # ShortUrl.objects.filter(pk=long_url).update(count=F("count") + 1)
    return redirect(long_url)
