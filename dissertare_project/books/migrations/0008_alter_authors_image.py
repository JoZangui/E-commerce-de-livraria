# Generated by Django 4.1 on 2022-08-31 12:11

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_remove_books_upload_by_authors_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='image',
            field=models.ImageField(blank=True, default='author_default_img.jpg', verbose_name='Imagem do autor'),
        ),
    ]
