from django.contrib import admin

from .models import Books, Category, BookLists, Announcement


class BooksAdmin(admin.ModelAdmin):

    search_fields = ['title']
    # search_fields: Isso adiciona uma caixa de pesquisa no topo da lista de alterações. Quando alguém insere termos de pesquisa, o Django pesquisará o campo "title". Você pode usar quantos campos quiser - embora, como ele usa uma LIKE consulta nos bastidores, limitar o número de campos de pesquisa a um número razoável facilitará a pesquisa do seu banco de dados.
    # ----------------------------------------------
    #  font: https://docs.djangoproject.com/en/4.0/intro/tutorial07/#customize-the-admin-change-list

    fieldsets = [
        (None, {'fields': [
            'title',
            'file',
            'description',
            'comment',
            'cover',
            'date_posted',
            'price',
            'is_sale',
            'sale_price',
            'category']}),
        ('Autor do livro', {'fields': ['author']}),
        ('Quem está a publicar', {'fields': ['uploaded_by']})
    ]

    list_display = (
        'title',
        'file',
        'cover',
        'date_posted',
        'author',
        'uploaded_by',
        'price',
        'is_sale',
        'sale_price')


admin.site.register(Books, BooksAdmin)
admin.site.register(Category)
admin.site.register(BookLists)
admin.site.register(Announcement)
