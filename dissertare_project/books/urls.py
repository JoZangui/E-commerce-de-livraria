""" Books urls """
from django.urls import path

from . import views

urlpatterns = [
    # home
    path('', views.home, name="home"),
    # books
    path('books', views.books, name="books"),
    # book detail
    path('book/book_detail/<int:book_id>/', views.book_detail, name="book-detail"),
    # upload book form
    path('book/upload_book/', views.upload_book, name="upload-book"),
    # update book form
    path('book/update_book/<int:book_id>/', views.update_book, name='book-update'),
    # delete book
    path('book/delete_book/<int:book_id>/', views.delete_book, name='book-delete'),
    # books on sale
    path('books_on_sale', views.books_on_sale, name='books-on-sale'),
    # book lists
    path('book_lists', views.book_lists, name='book-lists'),
    # books from list
    path('books_from_list/<int:list_id>', views.books_from_list, name='books-from-lists'),
]
