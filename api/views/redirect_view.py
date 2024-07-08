from django.shortcuts import get_object_or_404, redirect

from api.models import ShortUrl


def redirect_view(request, short_code):
    short_url = get_object_or_404(ShortUrl, short_url=short_code)
    return redirect(short_url.long_url)
