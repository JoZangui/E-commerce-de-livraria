from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Books
from .forms import BookForm


def books(request):
    all_books = Books.objects.all().order_by('-date_posted')

    # classe para separar os itens por páginas (12 item por página)
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


@login_required
def upload_book(request):
    """ Apenas admin devem usar essa página """
    if request.method == 'POST':
        book_form = BookForm(
            request.POST,
            request.FILES)
        
        if book_form.is_valid():
            final_form = book_form.save(commit=False)
            final_form.book_owner = request.user
            final_form.save()
            
            return HttpResponseRedirect(reverse(
                'book-detail',
                kwargs={'book_id': final_form.pk}
            ))

    book_form = BookForm()

    return render(request, 'books/book_create_form.html', {'book_form': book_form})


@login_required
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
    else:
        book_form = BookForm(instance=book)

        return render(request, 'books/book_create_form.html', {'book_form': book_form})


@login_required
def delete_book(request, book_id):
    """ Apenas admin deven usar essa página """
    book = Books.objects.get(pk=book_id)

    if request.method == 'POST':
        book.delete()

        return HttpResponseRedirect(reverse('books'))

    return render(request, 'books/delete_book_form.html', {'book': book})
