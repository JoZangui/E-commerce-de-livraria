""" payment views """
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import FileResponse, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods

from .models import Order, OrderItem, ShippingAddress, Invoices
from .forms import ShippingForm, PaymentForm
from users.models import Profile
from cart.cart import Cart
from books.models import Books


def order_conclusion(request):
    """
    Resumo do pedido do cliente

    Essa pagina é exibida quando o cliente finaliza o pedido
    """

    return render(request, 'payment/order_conclusion.html')

@login_required
def not_shipped_dash(request):
    """ Página com uma lista dos pedidos não entregues """
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=False).order_by('-date_ordered')

        pagtr = Paginator(orders, 5)

        page_number = request.GET.get('page')
        page_obj = pagtr.get_page(page_number)
        
        return render(request, 'payment/not_shipped_dash.html', {'page_obj': page_obj})
    else:
        messages.warning(request, "Access Denied")
        return redirect('books')

@login_required
def not_shipped_to_shipped(request, order_id):
    """ Página para definir um pedido não entregue como entregue """
    if request.user.is_superuser:
        order = Order.objects.filter(id=order_id).first()

        if request.POST:
            # grab Date and time
            # Obtem o tempoe data
            now = timezone.now()
            # grab the order
            # Obtem Order
            order = Order.objects.filter(id=order_id)
            # update order
            # Actualiza Order
            order.update(shipped=True, date_shipped=now)

            messages.success(request, f"Pedido nº {order.first().id}, marcado como entregue com sucesso")
            return redirect('not-shipped-dash')

        if order.shipped:
            # If the order has already been delivered, it raises an Http404
            # se o pedido em causa já tiver sido entregue ele levanta uma Http404
            messages.warning(request, "Este artigo não existe ou já foi entregue")
            raise Http404
        else:
            return render(request, 'payment/not_shipped_to_shipped.html', {'order': order})
    else:
        messages.warning(request, "Acesso negado")
        return redirect('books')


@login_required
def shipped_dash(request):
    """ Lista de pedidos entregues """
    if request.user.is_superuser:
        orders = Order.objects.filter(shipped=True).order_by('-date_shipped')

        pagtr = Paginator(orders, 5)

        page_number = request.GET.get('page')
        page_obj = pagtr.get_page(page_number)

        return render(request, 'payment/shipped_dash.html', {'page_obj': page_obj})
    else:
        messages.warning(request, "Access Denied")
        return redirect('books')

@require_http_methods(["POST"])
def process_order(request):
    """
    Processa o pedido do cliente, desde validação de formulários até a criação de faturas
    Se tudo estiver conforme ele termina enviando um email para o cliente...
    ...com as informações necessárias sobre o compra
    """

    # get the cart
    # Obtem o cart
    cart = Cart(request)
    # Get books that are in the cart
    # Obtem os livros que estão presentes em cart
    cart_books = cart.get_books
    # Get cart items quantities
    # Obtem a quantidade de items em cart
    quantities = cart.get_quantities
    # Get total price
    # Obtem o valor total a pagar
    totals = cart.cart_total()

    # Get Billing Info from the last page
    # Obtem as informações de pagamento da última página
    payment_form = PaymentForm(request.POST or None)
    # obtem o método de pagamento escolhido pelo cliente por meio do payment_form
    payment_mode = str(payment_form['payment_mode'].value())
    # Get Shipping Session data
    # Obtem os dados de entrega do usuário por meio do Session
    my_shipping = request.session.get('my_shipping')

    # Gather Order Info
    # Reúne as informações do pedido
    full_name = my_shipping['shipping_full_name']
    shipping_email = my_shipping['shipping_email']
    # Create Shipping Address from session info
    # Cria um endereço de entrega por meio das informações vinda de Session
    shipping_address = json.dumps({"shipping_address1": my_shipping['shipping_address1'], "shipping_address2": my_shipping['shipping_address2'], "shipping_city":my_shipping['shipping_city'], "shipping_phone_number": my_shipping['shipping_phone_number'], "shipping_mode": my_shipping['shipping_mode']})
    amount_paid = totals

    """
    EN: Create an Order
    PT: Cria um pedido
    """
    # logged in
    # para usuários logados
    if request.user.is_authenticated:
        user = request.user
        # Create Order
        # Cria um pedido
        create_oder = Order(
            user=user,
            full_name=full_name,
            email=shipping_email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
        create_oder.save()

        """ 
        EN: Add order items
        PT: Adicionando items ao pedido
        """

        # Get the order ID
        # Obtem o ID do pedido
        order_id = create_oder.pk

        # Get cart books Info
        # Obtem as informações do livro que estão no carrinho
        for book in cart_books():
            # Get book ID
            # ID do livro
            book_id = book.id
            # Get book price
            # Preço do livro
            if book.is_sale: # se estiver em promoção
                # Get sale price
                # obtem o preço de promoção
                price = book.sale_price
            else: # se não
                # Get normal price
                # obtem o preço normal
                price = book.price

            # Get quantity items {'item_id': quantity} {1: 5}
            # obtem os items em quantities {'item_id': quantity} {1: 5}
            for key, value in quantities().items():
                # If the item id is the same as the book id,
                # then create an OrderItem with the information of that book and its quantity
                # se o id do item for igual ao id do livro então...
                # ... cria um OrderItem com as informações desse livro e a respetiva quantidade
                if int(key) == book.id: 
                    # create order item
                    # Cria um objecto OrderItem com os itens de cart
                    create_oder_item = OrderItem(order_id=order_id, book_id=book_id, user=user, quantity=value, price=price)
                    # Save the object in the database
                    # Salva o objeto na base de dados
                    create_oder_item.save()

        # create invoice
        # Cria uma fatura
        invoice_number = f'E_Books_{order_id}'
        invoice = Invoices(order_id=order_id, invoice_number=invoice_number, payment_mode=payment_mode)
        invoice.save()

        """
        EN: Send an email to the customer with the invoice and book
        PT: Enviar um email para o cliente com a fatura e o livro
        """
        # pega o endereço actual do site
        current_site = get_current_site(request)
        # Email subject
        # Assunto do email
        mail_subject = 'Obrigado por comprar na livraria Dissertare'
        # renders an html template to string form
        # renderiza um template html para a forma de string
        message = render_to_string(
            'payment/payment_email_template.html',
            {
                'domain': current_site.domain,
                'order_id': order_id
            }
        )
        to_email = shipping_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.attach_file(invoice.invoice_file.path)
        email.send(fail_silently=False)

        # Delete our cart
        # Exclui o nosso carrinho
        for key in list(request.session.keys()):
            if key == 'session_key':
                # Delete the key
                # Elimina a chave
                del request.session[key]

        """
        EN: Delete Cart from Database (user_cart field)
        PT: Elimina o carrinho da base de dados (campo user_cart)
        """
        current_user = Profile.objects.filter(user__id=request.user.id)
        # Delete shopping cart in Database (user_cart field)
        # Remove as informações do carrinho de compras da base de dados (campo user_cart)
        current_user.update(user_cart="")


        messages.success(request, "Pedido concluido com sucesso!")
        return redirect('order-conclusion')
    else:
        # Not looged in
        # Para usuários não logados

        # Create Order
        create_oder = Order(
            full_name=full_name,
            email=shipping_email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
        create_oder.save()
        # Add order items
        # Get the order ID
        order_id = create_oder.pk

        # Get book Info
        for book in cart_books():
            # Get book ID
            book_id = book.id
            # Get book price
            if book.is_sale:
                price = book.sale_price
            else:
                price = book.price

            # Get quantity
            for key, value in quantities().items():
                if int(key) == book.id:
                    # create order item
                    create_oder_item = OrderItem(order_id=order_id, book_id=book_id, quantity=value, price=price)
                    create_oder_item.save()

        # create invoice
        invoice_number = f'E_Books_{order_id}'
        invoice = Invoices(order_id=order_id, invoice_number=invoice_number, payment_mode=payment_mode)
        invoice.save()

        # pega o endereço actual do site
        current_site = get_current_site(request)
        # Enviar um email para o cliente com a fatura e o livro
        mail_subject = 'Obrigado por comprar na livraria Dissertare'
        # renderiza um template html para a forma de string
        message = render_to_string(
            'payment/payment_email_template.html',
            {
                'domain': current_site.domain,
                'order_id': order_id
            }
        )
        to_email = shipping_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.attach_file(invoice.invoice_file.path)
        email.send(fail_silently=False)

        # Delete our cart
        for key in list(request.session.keys()):
            if key == 'session_key':
                # Delete the key
                del request.session[key]

        messages.success(request, 'Order Placed!')
        return redirect('order-conclusion')


@require_http_methods(["POST"])
def billing_info(request):
    """ Página com o formulário de método de pagamento """

    # Get the cart
    # Obter as informações do carrinho
    cart = Cart(request)
    cart_books = cart.get_books
    quantities = cart.get_quantities
    totals = cart.cart_total()

    # create a session with shipping info
    # Cria uma session com as informações de entrega
    my_shipping = request.POST
    request.session['my_shipping'] = my_shipping

    # check to see if user is logged in
    # Verifica se o usuário está logado
    if request.user.is_authenticated:
        # Get the billing form
        # Obtem o formulário de pagamento
        billing_form = PaymentForm()
        return render(request, 'payment/billing_info.html', {
            'cart_books': cart_books,
            'quantities': quantities,
            'totals': totals,
            'shipping_info': request.POST,
            'billing_form': billing_form
        })
    else:
        # Not logged in
        # Para usuários não logados

        # Get the billing form
        # Obtem o formulário de pagamento
        billing_form = PaymentForm()
        return render(request, 'payment/billing_info.html', {
            'cart_books': cart_books,
            'quantities': quantities,
            'totals': totals,
            'shipping_info': request.POST,
            'billing_form': billing_form
        })

def checkout(request):
    """ Inicio do processo de compra """
    
    # Get the cart
    # Obter as informações do carrinho
    cart = Cart(request)
    cart_books = cart.get_books
    quantities = cart.get_quantities
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as logged in user
        # Checkout para usuários logados

        # Shipping User
        # Endereço de entrega do User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # shipping form
        # Formulário de entrega
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {
            'cart_books': cart_books,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        })
    else:
        # Checkout as guest
        # Checkout para usuários não logados
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {
            'cart_books': cart_books,
            'quantities': quantities,
            'totals': totals,
            'shipping_form': shipping_form
        })

def ordered_books(request, pk):
    """ 
    Página com os livros que o cliente comprou
    Está pagina é acessada pelo link enviado ao email do cliente apos o fim de uma compra
    """
    order = Order.objects.get(id=pk)
    order_items = order.orderitem_set.all()

    return render(request, 'payment/ordered_books.html', {'order_items': order_items})

def download_book(request, pk):
    """ View para download do livro """
    book = get_object_or_404(Books, pk=pk)
    book_path = book.file.path
    response = FileResponse(open(book_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'

    return response
