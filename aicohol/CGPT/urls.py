from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.category_view, name="category_view"),
    path("query_view/", views.query_view, name="query_view"),
]
