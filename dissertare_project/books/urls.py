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
    # download book
    path('book/download/<int:book_id>', views.download_book, name='download-book'),
    # register author form
    path('author/register_author/', views.register_author, name="register-author"),
    # author detail
    path('author/author_detail/<str:author_name>/', views.author_detail, name='author-detail'),
    # author update
    path('author/author_update/<str:author_name>/', views.author_update, name='author-update'),
    # delete author
    path('author/delete_author/<str:author_name>/', views.delete_author, name='author-delete'),
    path("author/all_authors/", views.all_authors, name="all-authors"),
    # all author books
    path('author/all_author_books/<str:author_name>/', views.all_author_books, name='all-author-books'),
    # books_on_sale
    path('books_on_sale', views.books_on_sale, name='books-on-sale')
]
