from django.urls import path

from . import views

urlpatterns = [
	path('test/', views.current_datetime, name = 'test'),
]