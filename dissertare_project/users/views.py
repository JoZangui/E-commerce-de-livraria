""" users views """
import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import Http404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from payment.forms import ShippingForm
from cart.cart import Cart
from .forms import UserRegisterForm
from .tokens import account_activation_token
from users.models import Profile
from payment.models import ShippingAddress, Order, OrderItem
from books.models import Books
from books.forms import AnnouncementForm


def register(request):
    """ view para registro de usuário """

    # redireciona para a página home se o usuário já estiver activo no site
    if request.user.is_active:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            """ Mensagem de confirmação de e-mail """
            # pega o endereço actual do site
            current_site = get_current_site(request)
            # assunto do email que será enviado
            mail_subject = 'Activate your blog account.'
            # renderiza um template html para a forma de string
            message = render_to_string(
                'users/email_template.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                }
            )
            # destinatário do email
            to_email = form.cleaned_data.get('email')
            # objecto responsável pelo envio do email
            email = EmailMessage(mail_subject, message, to=[to_email])
            # envio do email
            email.send(fail_silently=False)
            # renderiza uma página com a mensagem abaixo
            # indicando que o cliente deve ver em seu o email uma mensagem com um link de confirmação
            return HttpResponse('Por favor confirme o seu endereço de email para completar o registro')
    else:
        form = UserRegisterForm()
    return render(
        request,
        'users/register.html',
        {'form': form, 'title': 'cadastrar'}
    )


def activate(request, uidb64, token):
    """
    View de activação de conta
    
    VIEW ACESSADA COM O LINK DE ACTIVAÇAO DE CONTA
    QUE FOI ENVIADA PARA O EMAIL DO NOVO USUÁRIO
    """

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # se o user for diferente de 'None'
        # e as informções do token geradas estiverem de acordo 
        # ele define a propriedade de usuário activado como sendo 'True'
        user.is_active = True
        # e depois salva essa informação do usuário
        user.save()
        # faz o login do novo usuário
        login(request, user)
        messages.success(request, 'Registro feito com sucesso')
        # Redireciona o usuário para a página do formulário de entrega
        return redirect('user-shipping-address')
    else:
        # Activation link is invalid
        return HttpResponse('Link de activação inválido!')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=user.id)
            # Get their saved cart from database
            saved_cart = current_user.user_cart
            # Convert database string to python dictionary
            if saved_cart:
                # Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # Loop thru the cart and add the items from the database
                for key, value in converted_cart.items():
                    cart.add(book=key, quantity=value)
            messages.success(request, 'You Have Been Logged In!')
            return redirect('home')
        else:
            messages.warning(request, 'There was an error, please try again...')
            return redirect('login')
    else:
        return render(request, 'users/login.html')


@login_required
def user_shipping_address(request):
    """
    Página de registo dos dados de endereço de entrega do usuário.
    Apenas para usuários logados.
    """
    
    if request.POST:
        shipping_addres = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_addres)
        if shipping_form.is_valid():
            shipping_form.save()

            messages.success(request, 'Registro feito com sucesso')
            return redirect('home')
        return render(request, 'users/user_shipping_address.html', {'shipping_form': shipping_form})

    shipping_form = ShippingForm()
    return render(request, 'users/user_shipping_address.html', {'shipping_form': shipping_form})


@login_required
def update_user_shipping_address(request):
    """
    Página de actualização dos dados de endereço de entrega.
    Apenas para usuários logados.
    """
    shipping_addres = ShippingAddress.objects.get(user__id=request.user.id)
    if request.POST:
        shipping_form = ShippingForm(request.POST or None, instance=shipping_addres)
        if shipping_form.is_valid():
            shipping_form.save()

            messages.success(request, 'Registro feito com sucesso')
            return redirect('profile')
        messages.warning('Algo deu errado!')
        return render(request, 'users/user_shipping_address.html', {'shipping_form': shipping_form})

    if shipping_addres:
        shipping_form = ShippingForm(instance=shipping_addres)
    else:
        shipping_form = ShippingForm()
    return render(request, 'users/update_user_shipping_address.html', {'shipping_form': shipping_form})


@login_required
def user_books(request):
    """ Página com os livros do usuário """
    ordered_items = OrderItem.objects.all().filter(user=request.user)

    books = []
    for item in ordered_items:
        books.append(item.book)

    pagtr = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = pagtr.get_page(page_number)

    return render(
        request,
        'users/user_books.html',
        {
            'book': ordered_items,
            'page_obj': page_obj,
            'title': 'books'
        }
    )

def user_books_details(request, book_id):
    """ Página de detalhes de um livro do usuário """
    # livro
    book = Books.objects.get(pk=book_id)
    # Retorna uma das categorias do livro
    category = book.category.first()
    # Retorna outros livros que pertencem a mesma categoria do livro pesquisado, excepto o livro pesquisado
    books_in_the_same_category = Books.objects.filter(category=category).exclude(pk=book_id)[:4]

    return render(
        request,
        'users/user_books_detail.html',
        {
            'book': book,
            'title': 'detail',
            'books_in_the_same_category': books_in_the_same_category
        }
    )

@login_required
def profile(request):
    ordered_items = OrderItem.objects.all().filter(user=request.user)[:4]
    shipping_addres = ShippingAddress.objects.get(user__id=request.user.id)
    return render(request, 'users/profile.html', {'ordered_items': ordered_items, 'shipping_addres': shipping_addres})

@login_required
def staff_profile(request):
    """ Página de administração para os membros do staff """
    if request.user.is_superuser:
        last_book_uploaded = Books.objects.last()
        # número de livros entregues
        shipped_quantity = Order.objects.filter(shipped=True).count()
        # número de livros não entregues
        not_shipped_quantity = Order.objects.filter(shipped=False).count()

        return render(
            request,
            'users/staff_profile.html',
            {
                'last_book_uploaded': last_book_uploaded,
                'shipped_quantity': shipped_quantity,
                'not_shipped_quantity': not_shipped_quantity,
            }
        )
    else:
        raise Http404


@login_required
def upload_announcement(request):
    """ Página para upload de anúncios """
    if request.user.is_superuser:
        announcement_form = AnnouncementForm()

        if request.POST:
            announcement_form = AnnouncementForm(request.POST, request.FILES or None)

            if announcement_form.is_valid():
                announcement_form.save()
                messages.success(request, 'anúncio adicionado com sucesso')
                return redirect('staff-profile')
            messages.warning(request, 'Algo deu errado!')
        return render(request, 'users/announcement_form.html', {'announcement_form': announcement_form})
    else:
        raise Http404
