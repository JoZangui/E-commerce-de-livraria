""" Payment urls """
from django.urls import path

from . import views

urlpatterns = [
    # checkout
    path('checkout/', views.checkout, name="checkout"),
    # método de pagamento
    path('billing_info', views.billing_info, name='billing_info'),
    # processamento do pedido
    path('process_order', views.process_order, name='process_order'),
    # livros adquiridos
    path('ordered_books/<int:pk>', views.ordered_books, name='ordered_books'),
    # download do livro
    path('book_download/<int:pk>', views.download_book, name='download_book'),
    # conclusão do pedido
    path('order_conclusion/', views.order_conclusion, name='order-conclusion'),
    # pedidos entregues
    path('shipped_dash/', views.shipped_dash, name='shipped-dash'),
    # pedidos não entregues
    path('not_shipped_dash/', views.not_shipped_dash, name='not-shipped-dash'),
    # mudar pedidos de não entregues para entregues
    path('not_shipped_to_shipped/<int:order_id>', views.not_shipped_to_shipped, name='not-shipped-to-shipped'),
]