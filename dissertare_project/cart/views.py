""" Cart Views """
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from .cart import Cart
from books.models import Books


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_books = cart.get_books
    quantities = cart.get_quantities
    totals = cart.cart_total()

    return render(request, 'cart/cart_summary.html', {'cart_books': cart_books, 'quantities': quantities, 'totals': totals, 'title': 'cart_summary'})

def cart_add(request):
    # Get the cart
    cart = Cart(request)

    # test for POST
    if request.POST.get('action') == 'post':
        #  Get stuff
        book_id = int(request.POST.get('book_id'))
        book_quantity = int(request.POST.get('book_qty'))

        # lookup book in DB
        book = get_object_or_404(Books, id=book_id)

        # Save to session
        cart.add(book=book.id, quantity=book_quantity)

        # Get Cart quantity
        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        book_id = int(request.POST.get('book_id'))
        # Call delete Function in Cart
        cart.delete(book=book_id)

        response = JsonResponse({'book': book_id})
        messages.warning(request, ("Item Deleted From Shopping Cart..."))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        book_id = int(request.POST.get('book_id'))
        book_quantity = int(request.POST.get('book_qty'))

        cart.update(book=book_id, quantity=book_quantity)

        response = JsonResponse({'qty': book_quantity})
        messages.success(request, ("Your Cart Has Been Updated..."))
        return response
