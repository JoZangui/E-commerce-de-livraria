from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from books.models import Books,  Authors


class BooksTestCase(TestCase):
    """ testes para o model Books """

    def setUp(self) -> None:
        image_path = './media/books/images/joaquim/Assassins_Creed_The_Chain_Cover.jpg'

        new_cover_image = SimpleUploadedFile(
            name='Assassins_Creed_The_Chain_Cover.jpg',
            content=open(image_path, 'rb').read(),
            content_type='image/jpg'
        )

        author = Authors.objects.create(name='Quim', biography='Lorem ipsum')

        user = User.objects.create(username='KimZangui')

        self.book = Books.objects.create(
            author=author,
            title='Lorem',
            cover=new_cover_image,
            description='Lorem ipsum',
            uploaded_by=user
        )

    def test_title_equal_book_title(self):
        self.assertEqual(str(self.book), 'Lorem')


class AuthorsTestCase(TestCase):
    """ testes para o model Authors """

    def setUp(self) -> None:
        self.author = Authors.objects.create(name='Quim', biography='Lorem ipsum')

    
    def test_name_equal_author_name(self):
        self.assertEqual(str(self.author), 'Quim')
