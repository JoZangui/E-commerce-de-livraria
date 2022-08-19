from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Books

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


def book_detail(request, pk):
    book = Books.objects.get(pk=pk)

    return render(request, 'books/book_detail.html', {'book': book})
