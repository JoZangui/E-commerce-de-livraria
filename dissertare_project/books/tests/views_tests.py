from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import Books,  Authors


class BooksViewTestCase(TestCase):

    def setUp(self) -> None:

        self.user = User.objects.create(username='KimZangui')
        self.user.set_password('testing321')
        self.user.is_superuser = True
        self.user.save()

        self.client.login(username='KimZangui', password='testing321')

        self.author = Authors.objects.create(name='Quim', biography='Lorem ipsum')

        image_path = './media/books/images/joaquim/Assassins_Creed_The_Chain_Cover.jpg'

        self.new_cover_image = SimpleUploadedFile(
            name='Assassins_Creed_The_Chain_Cover.jpg',
            content=open(image_path, 'rb').read(),
            content_type='image/jpg'
        )

        self.book = Books.objects.create(
            author=self.author,
            title='Lorem',
            cover=self.new_cover_image,
            description='Lorem ipsum',
            uploaded_by=self.user
        )

    def get_views_response(self, view=str, **kwargs):
        """ Simula uma requisição get para uma determinada view """

        return self.client.get(
            reverse(view, kwargs={key: value for key, value in kwargs.items()})
        )

    def post_views_response(self, view=str, post_values=dict, **kwargs):
        """ Simula uma requisição post para uma determinada view """

        result = self.client.post(
            # path
            reverse(view, kwargs={key: value for key, value in kwargs.items()}),
            # values
            {key: value for key, value in post_values.items()}
        )

        return result

    # books
    def test_books_view_status_200(self):
        """ testa o status code de uma requisição get para a view books """
        
        response = self.get_views_response('books')

        self.assertEqual(response.status_code, 200)

    def test_books_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('books')

        self.assertTemplateUsed(response, 'books/books.html')

    # book detail
    def test_book_detail_status_200(self):
        """ testa o status code de uma requisição get para a view book detail """

        response = self.get_views_response('book-detail', book_id=self.book.id)

        self.assertEqual(response.status_code, 200)

    def test_book_detail_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('book-detail', book_id=self.book.id)
        
        self.assertTemplateUsed(response, 'books/book_detail.html')

    # upload book
    def test_upload_book_status_200__get(self):
        """ testa o status code de uma requisição get para a view upload book """

        # solicitação get
        response = self.get_views_response('upload-book')
        self.assertEqual(response.status_code, 200)

    def test_upload_book_status_200__post(self):
        book_data = {
            'author': self.author,
            'title': 'Lorem',
            'cover': self.new_cover_image,
            'description': 'Lorem ipsum',
            'uploaded_by': self.user
        }

        response = self.post_views_response('upload-book', book_data)
        self.assertEqual(response.status_code, 200)

    def test_upload_book_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('upload-book')

        self.assertTemplateUsed(response, 'books/book_create_form.html')

    # update book
    def test_update_book_status_200__get(self):
        """ testa o status code de uma requisição get para a view update book """

        # solicitação get
        response = self.get_views_response('book-update', book_id=self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_update_book_status_200__post(self):

        book_data = {
            'author': self.author,
            'title': 'Lorem',
            'cover': self.new_cover_image,
            'description': 'Lorem ipsum',
            'uploaded_by': self.user
        }

        response = self.post_views_response('book-update', book_data, book_id=self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_update_book_view_template_used(self):
        """ testa se está a retornar um template e se o template retornado é o template esperado """

        response = self.get_views_response('book-update', book_id=self.book.id)

        self.assertTemplateUsed(response, 'books/book_create_form.html')
