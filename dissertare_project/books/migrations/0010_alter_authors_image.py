# Generated by Django 4.1 on 2022-08-31 12:30

import books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_books_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authors',
            name='image',
            field=models.ImageField(blank=True, verbose_name='Imagem do autor'),
        ),
    ]
