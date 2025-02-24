from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from books.forms import BookForm


class BookFormTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create(username='KimZangui')
        self.user.set_password('testing321')
        self.user.save()

        self.client.login(username='KimZangui', password='testing321')

        self.image_path = './media/books/images/arquivos_de_Teste/Assassins_Creed_The_Chain_Cover.jpg'

        self.pdf_path = './media/books/pdfs/arquivos_de_Teste/caelum-csharp-dotnet-fn13.pdf'

    def upload_file(self, path:str, file_type:str) -> SimpleUploadedFile:
        """ simula o upload de um arquivo """

        with open(path, 'rb') as file:
            final_file = SimpleUploadedFile(file.name, file.read(), content_type=file_type)

        return final_file

    def test_bookform_is_valid(self):
        """ testa se os dados enviados para o formulário são válidos """

        pdf_file = self.upload_file(self.pdf_path, 'application/pdf')
        image_file = self.upload_file(self.image_path, 'image/jpg')

        book_data = {
            'author': self.author,
            'title': 'Lorem Lorem',
            'description': 'Lorem ipsum',
            'uploaded_by': self.user
        }

        book_files = {
            'file': pdf_file,
            'cover': image_file,
        }

        book_form = BookForm(data=book_data, files=book_files)
        self.assertTrue(book_form.is_valid(), book_form.errors.as_data())
