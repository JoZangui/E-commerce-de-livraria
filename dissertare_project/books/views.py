import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from .models import Authors, Books, BookLists
from .forms import AuthorsForm, BookForm
from dissertare_project.settings import BASE_DIR
from cart.cart import Cart

# from .rename_dir import rename_dir


def _user_is_superuser(user):
    """
    retorna True se o usuário
    é um super usuário, se não, retorna False
    """
    return user.is_superuser


def home(request):
    """página home """
    
    # retorna apenas 5 livros dos livros em promoção
    books_on_sale = Books.objects.filter(is_sale=True)[:5]
    # calcula a percentagem de desconto e adiciona ao atributo (discount_percentage) que foi criado dentro do loop
    for book in books_on_sale:
        book.discount_percentage = ((book.price - book.sale_price) / book.price) * 100
    # retorna os últimos 5 livros adicionados
    recent_books = Books.objects.all().order_by('-date_posted')[:5]
    # a escolha do editor
    editor_choice = Books.objects.filter(category__name='A escolha do editor').order_by('-date_posted').first()
    # lista de livros
    book_lists = BookLists.objects.all()[:3]

    return render(request, 'books/home.html', {
        'books_on_sale': books_on_sale,
        'recent_books': recent_books,
        'editor_choice':editor_choice,
        'book_lists': book_lists,
        'title': 'home'
        }
    )


# books
def books(request):
    """
    página com todos os livros em ordem de postagem começando do mais recente
    """

    all_books = Books.objects.all().order_by('-date_posted')
    # calcula a percentagem de desconto e adiciona ao atributo (discount_percentage) que foi criado dentro do loop
    for book in all_books:
        if book.is_sale:
            book.discount_percentage = ((book.price - book.sale_price) / book.price) * 100

    # classe para separar os itens por páginas (10 itens por página)
    pagtr = Paginator(all_books, 10)

    # número da página a ser apresentada
    page_number = request.GET.get('page')
    # objecto com o número e link das páginas
    page_obj = pagtr.get_page(page_number)

    return render(
        request,
        'books/books.html',
        {
            'books': all_books,
            'page_obj': page_obj,
            'title': 'books'
        }
    )

def books_on_sale(request):
    """ página com os livros em promoção """

    all_books_on_sale = Books.objects.filter(is_sale=True).order_by('-date_posted')
    # calcula a percentagem de desconto e adiciona ao atributo criado (discount_percentage)
    for book in all_books_on_sale:
        book.discount_percentage = ((book.price - book.sale_price) / book.price) * 100

    # classe para separar os itens por páginas (8 itens por página)
    pagtr = Paginator(all_books_on_sale, 10)

    # número da página a ser apresentada
    page_number = request.GET.get('page')
    # objecto com o número e link das páginas
    page_obj = pagtr.get_page(page_number)

    return render(
        request,
        'books/books.html',
        {
            'books': all_books_on_sale,
            'page_obj': page_obj,
            'title': 'books'
        }
    )


def books_from_list(request, list_id):
    """ página de uma lista de livros """

    # Lista de livros
    books_list = BookLists.objects.get(id=list_id)
    # livros da lista
    books = books_list.books.all().order_by('-date_posted')
    # calcula a percentagem de desconto e adiciona ao atributo criado (discount_percentage)
    for book in books:
        if book.is_sale:
            book.discount_percentage = ((book.price - book.sale_price) / book.price) * 100

    # classe para separar os itens por páginas (8 itens por página)
    pagtr = Paginator(books, 10)
    # número da página a ser apresentada
    page_number = request.GET.get('page')
    # objecto com o número e link das páginas
    page_obj = pagtr.get_page(page_number)

    return render(
        request,
        'books/books.html',
        {
            'books': books,
            'page_obj': page_obj,
            'title': 'books'
        }
    )

def book_detail(request, book_id):
    """ Página de detalhes de um livro """
    # livro
    book = Books.objects.get(pk=book_id)
    # carrinho
    cart = Cart(request)
    # verifica se o livro já está no carrinho
    book_is_in_cart = str(book_id) in cart.cart.keys()
    # Retorna uma das categorias do livro
    category = book.category.first()
    # Retorna outros livros que pertencem a mesma categoria do livro pesquisado, excepto o livro pesquisado
    books_in_the_same_category = Books.objects.filter(category=category).exclude(pk=book_id)[:4]

    return render(
        request,
        'books/book_detail.html',
        {
            'book': book,
            'title': 'detail',
            'book_is_in_cart': book_is_in_cart,
            'books_in_the_same_category': books_in_the_same_category
        }
    )


def book_lists(request):
    """ Página com as listas de livros """

    # Listas de livros ordernado por data de actualização
    lists = BookLists.objects.all().order_by('-update_date')

    # classe para separar os itens por páginas (8 itens por página)
    pagtr = Paginator(lists, 10)
    # número da página a ser apresentada
    page_number = request.GET.get('page')
    # objecto com o número e link das páginas
    page_obj = pagtr.get_page(page_number)

    return render(
        request,
        'books/book_lists.html',
        {
            'lists': lists,
            'title': 'book_lists',
            'page_obj': page_obj,
        })

@user_passes_test(_user_is_superuser, login_url='home')
def upload_book(request):
    """
    página de upload de livros
    """

    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES)

        if book_form.is_valid():
            final_form = book_form.save(commit=False)
            final_form.uploaded_by = request.user
            final_form.save()

            messages.success(request, 'Livro adicionado com sucesso')
            return HttpResponseRedirect(reverse(
                'book-detail',
                kwargs={'book_id': final_form.pk}
            ))

        messages.warning(request, 'Algo deu errado')
        return render(
            request,
            'books/book_create_form.html',
            {
                'book_form': book_form,
                'book_form_erros': book_form.errors,
                'title': 'carregar livro'
            }
        )

    book_form = BookForm()

    return render(
        request,
        'books/book_create_form.html',
        {'book_form': book_form, 'title': 'carregar livro'}
    )


@user_passes_test(_user_is_superuser, login_url='home')
def update_book(request, book_id):
    """ página de actualização de livros """

    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES,
            instance=book)

        if book_form.is_valid():
            book_form.save()

            messages.success(request, 'Livro actualizado com sucesso')
            return HttpResponseRedirect(reverse(
                'book-detail',
                kwargs={'book_id': book_id}
                )
            )
        messages.warning(request, 'Algo deu errado')
    else:
        book_form = BookForm(instance=book)

    title = f'editar livro {book.title}'

    return render(
        request,
        'books/book_create_form.html',
        {
            'book_form': book_form,
            'book_form_erros': book_form.errors,
            'title': title
        }
    )


@user_passes_test(_user_is_superuser, login_url='home')
def delete_book(request, book_id):
    """ Página para remoção de livros """

    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book.delete()

        return HttpResponseRedirect(reverse('books'))

    title = f'remover o livro {book.title}'

    return render(request, 'books/delete_book_form.html', {'book': book, 'title': title})


# Authors
@user_passes_test(_user_is_superuser, login_url='home')
def register_author(request):
    """ Apenas admin devem usar essa página """
    if request.method == 'POST':
        author_form = AuthorsForm(
            request.POST,
            request.FILES)
        
        if author_form.is_valid():
            author_form.save()

            return HttpResponseRedirect(reverse(
                'author-detail',
                kwargs={'author_name': author_form.instance.name}
            ))
        return render(
            request,
            'books/author_registration_form.html',
            {
                'author_form': author_form,
                'author_form_erros': author_form.errors,
                'title': 'Registar novo autor'
            }
        )

    author_form = AuthorsForm()

    return render(
        request,
        'books/author_registration_form.html',
        {'author_form': author_form, 'title': 'Registar novo autor'}
    )


def author_detail(request, author_id):

    author = Authors.objects.get(id=author_id)
    author_books = author.books_set.all().order_by('-date_posted')

    title = author.name

    return render(
        request,
        'books/author_detail.html',
        {
            'author': author,
            'title': title,
            'author_books': author_books[:4]
        }
    )


def all_authors(request):
    """ todos os autores """

    authors = Authors.objects.all().order_by('-registration_date')

    pagtr = Paginator(authors, 14)
    page_number = request.GET.get('page')
    page_obj = pagtr.get_page(page_number)

    title = 'autores'

    return render (
        request,
        'books/all_authors.html',
        {
            'title': title,
            'page_obj': page_obj
        }
    )


def all_author_books(request, author_name):
    """ todos os livros de um autor """

    author = Authors.objects.get(name=author_name)
    author_books = author.books_set.all().order_by('-date_posted')

    pagtr = Paginator(author_books, 8)
    page_number = request.GET.get('page')
    page_obj = pagtr.get_page(page_number)

    title = f"todos os livros de {author.name}"

    return render(
        request,
        'books/all_author_books.html',
        {
            'author': author,
            'title': title,
            'author_books': author_books,
            'page_obj': page_obj
        }
    )


@user_passes_test(_user_is_superuser, login_url='home')
def author_update(request, author_name):
    """ Apenas admin deven usar essa página """
    author = Authors.objects.get(name=author_name)


    if request.method == 'POST':
        old_dirname = author.name
        path = os.path.abspath(f'{BASE_DIR}/media/authors/images/')

        author_form = AuthorsForm(
            request.POST,
            request.FILES,
            instance=author)

        if author_form.is_valid():
            # new_dirname = author_form.cleaned_data.get('name')
            # rename_dir(path, old_dirname, new_dirname)

            print(author_form.cleaned_data.get('image'))

            author_form.save()

            return HttpResponseRedirect(reverse(
                'author-detail',
                kwargs={'author_name': author.name}))

    author_form = AuthorsForm(instance=author)
    title = f'actualizar autor {author.name}'
    return render(
        request,
        'books/author_registration_form.html',
        {'author_form': author_form, 'title': title})


@user_passes_test(_user_is_superuser, login_url='home')
def delete_author(request, author_name):
    """ Apenas admin deven usar essa página """
    author = Authors.objects.get(name=author_name)

    if request.method == 'POST':
        author.delete()

        return HttpResponseRedirect(reverse('books'))

    title = f'remover autor {author.name}'
    return render(request, 'books/delete_author_form.html', {'author': author, 'title': title})
