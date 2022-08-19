""" Books urls """
from django import views
from django.urls import path

from . import views

urlpatterns = [
    # home
    path('', views.books, name="home"),
    # book detail
    path('book_detail/<int:pk>/', views.book_detail, name="book-detail"),
]
