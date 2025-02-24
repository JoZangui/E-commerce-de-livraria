from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import Books


class BooksViewTestCase(TestCase):
    """ Teste para views relacionadas aos autores dos livros """

    def setUp(self) -> None:

        self.user = User.objects.create(username='KimZangui')
        self.user.set_password('testing321')
        self.user.is_superuser = True
        self.user.save()

        self.client.login(username='KimZangui', password='testing321')

        self.image_path = './media/books/images/arquivos_de_Teste/Assassins_Creed_The_Chain_Cover.jpg'

        self.pdf_path = './media/books/pdfs/arquivos_de_Teste/caelum-csharp-dotnet-fn13.pdf'

        pdf_file = self.upload_file(self.pdf_path, 'application/pdf')
        
        image_file = self.upload_file(self.image_path, 'image/jpg')

        self.book = Books.objects.create(
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

    def post_views_response(self, view:str, post_values:dict, **kwargs):
        """ Simula uma solicitação post para uma determinada view """

        return self.client.post(
            # url
            reverse(view, kwargs=kwargs),
            # valor
            post_values,
            # aceitar o redirecionamento
            follow=True)

    # books
    def test_books_view_status_200(self):
        """ testa o status code de uma requisição get para a view books """
        
        response = self.get_views_response('books')

        self.assertEqual(response.status_code, 200)

    # book detail
    def test_book_detail_status_200(self):
        """ testa o status code de uma requisição get para a view book detail """

        response = self.get_views_response('book-detail', book_id=self.book.id)

        self.assertEqual(response.status_code, 200)

    # upload book
    def test_upload_book_status_200__get(self):
        """ testa o status code de uma requisição get para a view upload book """

        # solicitação get
        response = self.get_views_response('upload-book')
        self.assertEqual(response.status_code, 200)

    def test_upload_book_status_302__post(self):

        pdf_file = self.upload_file(self.pdf_path, 'application/pdf')
        
        image_file = self.upload_file(self.image_path, 'image/jpg')

        book_data = {
            'author': self.author,
            'file': pdf_file,
            'title': 'Lorem 1',
            'description': 'Lorem ipsum',
            'cover': image_file,
            'uploaded_by': self.user
        }

        response = self.post_views_response('upload-book', book_data)
        self.assertEqual(response.redirect_chain[0][1], 302)

    # update book
    def test_update_book_status_200__get(self):
        """ testa o status code de uma requisição get para a view update book """

        # solicitação get
        response = self.get_views_response('book-update', book_id=self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_update_book_status_302__post(self):

        pdf_file = self.upload_file(self.pdf_path, 'application/pdf')

        image_file = self.upload_file(self.image_path, 'image/jpg')

        book_data = {
            'author': self.author,
            'file': pdf_file,
            'title': 'Lorem Lorem',
            'description': 'Lorem ipsum',
            'cover': image_file,
            'uploaded_by': self.user
        }

        response = self.post_views_response('book-update', book_data, book_id=self.book.id)
        self.assertEqual(response.redirect_chain[0], (f'/book/book_detail/{self.book.id}/', 302))

    # delete book
    def test_delete_book_status_200__get(self):
        """ testa o status code de uma requisição get para a view update book """

        # solicitação get
        response = self.get_views_response('book-delete', book_id=self.book.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_book_status_302__post(self):

        # a view book-delete não recebe qual quer valor no post,
        # por isso enviamos um dicionário vazio, porque o método de teste post exige que passemos um dicionário
        empty_post = dict()

        response = self.post_views_response('book-delete', empty_post, book_id=self.book.id)
        self.assertEqual(response.redirect_chain[0], ('/', 302))
