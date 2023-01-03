from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import Books,  Authors


class BooksViewsTemplateTestCase(TestCase):
    """ Teste para templates relacionadas aos livros dos livros """

    def setUp(self) -> None:
        self.user = User.objects.create(username='KimZangui')
        self.user.set_password('testing321')
        self.user.is_superuser = True
        self.user.save()

        self.client.login(username='KimZangui', password='testing321')

        self.author = Authors.objects.create(name='Quim', biography='Lorem ipsum')

        self.image_path = './media/books/images/arquivos_de_Teste/Assassins_Creed_The_Chain_Cover.jpg'

        self.pdf_path = './media/books/pdfs/arquivos_de_Teste/caelum-csharp-dotnet-fn13.pdf'

        pdf_file = self.upload_file(self.pdf_path, 'application/pdf')
        
        image_file = self.upload_file(self.image_path, 'image/jpg')

        self.book = Books.objects.create(
            author=self.author,
            title='Lorem',
            file=pdf_file,
            cover=image_file,
            description='Lorem ipsum',
            uploaded_by=self.user
        )

    def upload_file(self, path:str, file_type:str) -> SimpleUploadedFile:
        """ simula o upload de um arquivo """

        with open(path, 'rb') as file:
            final_file = SimpleUploadedFile(file.name, file.read(), content_type=file_type)

        return final_file

    def get_views_response(self, view:str, **kwargs):
        """ Simula uma solicitação get para uma determinada view """

        return self.client.get(
            reverse(view, kwargs=kwargs)
        )

    def test_books_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('books')

        self.assertTemplateUsed(response, 'books/books.html')

    def test_book_detail_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('book-detail', book_id=self.book.id)

        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_upload_book_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('upload-book')

        self.assertTemplateUsed(response, 'books/book_create_form.html')

    def test_update_book_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('book-update', book_id=self.book.id)

        self.assertTemplateUsed(response, 'books/book_create_form.html')

    def test_delete_book_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('book-delete', book_id=self.book.id)

        self.assertTemplateUsed(response, 'books/delete_book_form.html')


class AuthorsViewsTemplateTestCase(TestCase):

    def setUp(self) -> None:

        self.user = User.objects.create(username='KimZangui')
        self.user.set_password('testing321')
        self.user.is_superuser = True
        self.user.save()

        self.client.login(username='KimZangui', password='testing321')

        self.author = Authors.objects.create(name='Quim', biography='Lorem ipsum')

        self.image_path = './media/books/images/arquivos_de_Teste/Assassins_Creed_The_Chain_Cover.jpg'

    def get_views_response(self, view:str, **kwargs):
        """ Simula uma solicitação get para uma determinada view """

        return self.client.get(
            reverse(view, kwargs=kwargs)
        )

    def test_author_detail_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('author-detail', author_name=self.author.name)

        self.assertTemplateUsed(response, 'books/author_detail.html')

    def test_register_author_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('register-author')

        self.assertTemplateUsed(response, 'books/author_registration_form.html')

    def test_update_author_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('author-update', author_name=self.author.name)

        self.assertTemplateUsed(response, 'books/author_registration_form.html')

    def test_author_delete_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('author-delete', author_name=self.author.name)

        self.assertTemplateUsed(response, 'books/delete_author_form.html')
