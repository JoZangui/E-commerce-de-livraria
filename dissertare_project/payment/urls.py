""" Payment urls """
from django.urls import path

from . import views

urlpatterns = [
    path('orders/<int:pk>', views.orders, name="orders"),
    path('checkout/', views.checkout, name="checkout"),
    path('billing_info', views.billing_info, name='billing_info'),
    path('process_order', views.process_order, name='process_order'),
    path('ordered_books/<int:pk>', views.ordered_books, name='ordered_books'),
    path('book_download/<int:pk>', views.download_book, name='download_book'),
]