from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.http import JsonResponse, Http404
from django.utils.translation import gettext_lazy as _

from .models import Authors, Books
from .forms import AuthorsForm, BookForm


def _user_is_superuser(user):
    """
    retorna True se o usuário
    é um super usuário, se não, retorna False
    """
    return user.is_superuser


def books(request):
    all_books = Books.objects.all().order_by('-date_posted')

    # classe para separar os itens por páginas (8 itens por página)
    pagtr = Paginator(all_books, 8)

    # número da página a ser apresentada
    page_number = request.GET.get('page')
    # objecto com o número e link das páginas
    page_obj = pagtr.get_page(page_number)

    return render(
        request,
        'books/books.html',
        {
            'books': all_books,
            'page_obj': page_obj})


def book_detail(request, book_id):
    book = Books.objects.get(pk=book_id)

    return render(request, 'books/book_detail.html', {'book': book})


@user_passes_test(_user_is_superuser)
def upload_book(request):
    """ Apenas admin devem usar essa página """
    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES)

        if book_form.is_valid():
            final_form = book_form.save(commit=False)
            final_form.uploaded_by = request.user
            final_form.save()


            return HttpResponseRedirect(reverse(
                'book-detail',
                kwargs={'book_id': final_form.pk}
            ))
        else:
            print(book_form.errors.as_data())
            return render(request, 'books/book_create_form.html', {'book_form': book_form, 'book_form_erros': book_form.errors})

    book_form = BookForm()

    return render(request, 'books/book_create_form.html', {'book_form': book_form})


@user_passes_test(_user_is_superuser)
def update_book(request, book_id):
    """ Apenas admin deven usar essa página """

    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES,
            instance=book)

        if book_form.is_valid():
            book_form.save()

            return HttpResponseRedirect(reverse(
                'book-detail',
                kwargs={'book_id': book_id}))

    book_form = BookForm(instance=book)

    return render(request, 'books/book_create_form.html', {'book_form': book_form})


@user_passes_test(_user_is_superuser)
def delete_book(request, book_id):
    """ Apenas admin deven usar essa página """
    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book.delete()

        return HttpResponseRedirect(reverse('books'))

    return render(request, 'books/delete_book_form.html', {'book': book})


@user_passes_test(_user_is_superuser)
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
            {'author_form': author_form, 'author_form_erros': author_form.errors})

    author_form = AuthorsForm()

    return render(request, 'books/author_registration_form.html', {'author_form': author_form})


def author_detail(request, author_name):
    author = Authors.objects.get(name=author_name)

    return render(request, 'books/author_detail.html', {'author': author})


@user_passes_test(_user_is_superuser)
def author_update(request, author_name):
    """ Apenas admin deven usar essa página """
    author = Authors.objects.get(name=author_name)

    if request.method == 'POST':
        author_form = AuthorsForm(
            request.POST,
            request.FILES,
            instance=author)

        if author_form.is_valid():
            author_form.save()

            return HttpResponseRedirect(reverse(
                'author-detail',
                kwargs={'author_name': author.name}))
    else:
        author_form = AuthorsForm(instance=author)

        return render(request, 'books/author_registration_form.html', {'author_form': author_form})


@user_passes_test(_user_is_superuser)
def delete_author(request, author_name):
    """ Apenas admin deven usar essa página """
    author = Authors.objects.get(name=author_name)

    if request.method == 'POST':
        author.delete()

        return HttpResponseRedirect(reverse('books'))

    return render(request, 'books/delete_author_form.html', {'author': author})
