from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_view, name="list_view"),
    path("query_view/", views.query_view, name="query_view"),
	path("detail_view/", views.detail_view, name="detail_view"),
	path('transcribe_audio/', views.transcribe_audio, name='transcribe_audio'),
]
