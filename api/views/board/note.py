from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    if request.method == "POST":
        return post(request)
    else:
        return get(request)


def get(request):
    return HttpResponse("一个Get请求")


def post(request):
    return HttpResponse("一个Post请求")
