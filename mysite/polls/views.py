from django.http import HttpResponse
import datetime

# Create your views here.

def index(request):
	return HttpResponse("Hello, world. You're at the polls index")


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now {}.</body></html>".format(now)
    return HttpResponse(html)

# def home_page(request):
# 	pg = "<html><head></head><body><h5>Homepage</h5></body></html>"
# 	return HttpResponse(pg)