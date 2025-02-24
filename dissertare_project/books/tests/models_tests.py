from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import Books


class BooksTestCase(TestCase):
    """ testes para o model Books """

    def setUp(self) -> None:
        image_path = './media/books/images/joaquim/Assassins_Creed_The_Chain_Cover.jpg'

        new_cover_image = SimpleUploadedFile(
            name='Assassins_Creed_The_Chain_Cover.jpg',
            content=open(image_path, 'rb').read(),
            content_type='image/jpg'
        )

        user = User.objects.create(username='KimZangui')

        self.book = Books.objects.create(
            title='Lorem',
            cover=new_cover_image,
            description='Lorem ipsum',
            uploaded_by=user
        )

    def test_title_equal_book_title(self):
        self.assertEqual(str(self.book), 'Lorem')
