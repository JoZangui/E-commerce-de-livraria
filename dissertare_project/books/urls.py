""" Books urls """
from django import views
from django.urls import path

from . import views

urlpatterns = [
    # home
    path('', views.books, name="books"),
    # book detail
    path('book_detail/<int:book_id>/', views.book_detail, name="book-detail"),
    # upload book form
    path('upload_book/', views.upload_book, name="upload-book"),
    # update book form
    path('update_book/<int:book_id>', views.update_book, name='book-update'),
    # delete book
    path('delete_book/<int:book_id>', views.delete_book, name='book-delete'),
]
