""" users views """
import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


from .forms import UserRegisterForm
from .tokens import account_activation_token
from users.models import Profile
from cart.cart import Cart


def register(request):
    """ view para registro de usuário """

    if request.user.is_active:
        return redirect('books')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # pega o endereço do actual do site
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
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserRegisterForm()
    return render(
        request,
        'users/register.html',
        {'form': form, 'title': 'cadastrar'}
    )


def activate(request, uidb64, token):
    """
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
        return HttpResponse('Thank you for your email confirmation. Now you can login account. go to <a href="/">livros<a>')
    else:
        return HttpResponse('Activation link is invalid!')


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
            return redirect('books')
        else:
            messages.warning(request, 'There was an error, please try again...')
            return redirect('login')
    else:
        return render(request, 'users/login.html')