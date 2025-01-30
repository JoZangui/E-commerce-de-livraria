# E-commerce de livraria
 * [Books](#books-app)
   * [views](#views-de-books)
   * [models](#models-de-books)
   * [forms]()
   * [signals]()
   * [announcement]()
   * [context_processors]()
   * [pdf_file_validator]()

 * [Users]()
   * [views]()
   * [models]()
   * [forms]()
   * [signal]()
   * [tokens]()
 * [Payment]()
   * [views]()
   * [models]()
   * [forms]()
   * [signal]()
   * [create_invoices]()
 * [Cart]()
   * [views]()
   * [models]()
   * [cart]()
   * [context_processors]()


## Books app

Na app **Books** encontramos tudo relacionado ao livro, desde modelos, formulários de validação até views, nesta app também reside a view para a página home.

### Views de books

Logo no início encontraremos a função **_user_is_superuser** que é usado pelo decorador *__@user_passes_test__* para verificar se o usuário que está tentando aceder a view em questão é um **super_user**. Esta função recebe como argumento o **user** o qual é usado para verificar se o usuário é ou não um **super_user**, a função retorna *__True__* se o usuário for um **super_user** e *__False__* se não for. Se o usuário não for um **super_user** então *__@user_passes_test__* retorna o usuário para a página home.

A view **home** retorna uma página com alguns destaques como: livros em promoção (*__books_on_sale__*), as novidades (*__recent_books__*), a escolha do editor (*__editor_choice__*) e por fim algumas listas de recomendações de leitura (*__book_lists__*).

A view **books** retorna um página com todos os livros começando pelo que foi adicionado recentemente. Está views usa **Paginator** para organizar o conteudo em páginas.

A view **books_on_sale** é semelhante a view **books** mas apenas para livros em promoção.

A view **books_from_list** retorna uma página com os livros de uma determinada lista das listas de recomendações.

A view **book_detail** retorna uma página com os detalhes de um determinado livro, nele também podemos ver se o livro já se encontra ou não no nosso carrinho de compras, e algumas recomendações de livros que pertencem a mesma categoria.

A view **book_lists** retorna uma página com as listas de remendação de livros.

A view **upload_book** retorna uma página com o formulário de upload de livro. É nesta mesma view onde ocorre a validação do formulário caso o método http seja POST, neste contexto ele verifica se o formulário é válido, caso seja, a view redireciona o usuário para a página de detalhes deste mesmo livro, caso o formulário não seja válido ele apresenta uma mensagem de erro na mesma página do formulário.

A view **update_book** é semelhante a view **upload_book** mas como o nome sugere, ela serve para atualizar os dados de um determinado livro

A view **delete_book** retorna uma página com um formulário de confirmação para a remoção de um determinado livro, quão a remoção é confirmada o usuário é redirecionado para a página com todos os livros

### Models de books
A função **val_cannot_be_negative** verifica se o valor inserido no campo é negativo, ele é usado em campos do tipo numérico como por exemplo **_price_** e **_sale\_price_** como valor para o parâmetro **_validators_**

A função **books_pdf_file_path** configura o diretório dos arquivos de PDF dos livros quando um novo modelo **Books** for salvo. Ele é usado no campo **_file_** de **Books** como valor do parâmetro **_upload\_to_**

A função **books_image_file_path** configura o diretório dos arquivos de imagem dos livros quando um novo modelo **Books** for salvo. Ele é usado no campo **_cover_** de **Books** como valor do parâmetro **_upload\_to_**

O model **Books** armazena as informações do livro e ele contém os seguintes campos:

 * **_author_** um campo ForeignKey que faz refêrencia ao modelo **_Auhtor_** de **books.models**.
 
 * **_file_** campo do tipo FileField que contém uma refêrencia ao arquivo PDF do livro.

 * **_title_** campo do tipo CharField que armazena o título do livro.

 * **_description_** campo do tipo TextField que armazena a descrição (sinopse) do livro.
 
 * **_comment_** campo do tipo TextField que armazena a descrição do administrador da página sobre o livro.
 
 * **_cover_** campo do tipo ImageField que contém uma refêrencia ao arquivo de imagem do livro.
 
 * **_date\_posted_** campo do tipo DateTimeField que contém a data e hora de upload do livro.
 
 * **_uploaded\_by_** campo do tipo ForeignKey que faz refêrencia ao modelo **User** do Django. Este campo é responsável por armazenar os dados do responsável pelo upload do livro.
 
 * **_category_** campo do tipo ManyToManyField que faz refêrencia ao modelo **Category**. Este campo é responsável por armazenar as categorias a qual o livro pertence.

 * **_price_** campo do tipo DecimalField armazena o preço do livro.

 * **_is\_sale_** campo do tipo BooleanField armazena o estado actual do livro, se está em promoção ou não, (**True** para livro em promoção e **False** para livros que não estão em promoção).

 * **_sale\_price_** campo do tipo DecimalField armazena o preço de promoção do livro.

Nós subscrevemos o método **_save_** deste **Model** para alterar o tamanho da imagem da capa do livro quando este for salvo na base de dados.

O model **BookLists** armazena as informações das listas de livros criadas pelo administrador e ele contém os seguintes campos:

  * **_list\_name_** campo do tipo CharField que armazena o nome da lista.

  * **_books_** campo do tipo ManyToManyField que faz refêrencia ao **Books** de **_books.models_**.

  * **_list\_description_** campo do tipo TextField armazena a descrição da lista.

  * **_update\_date_** campo do tipo DateTimeField armazena a data e a hora da ultima actualização da lista, seja a adição de algum livro ou actualização dos dados da mesma lista como o nome e a descrição.

O model **Category** armazena as informações de categorias de livros e ele contém o seguinte campos:

  * **_name_** campo do tipo CharField que armazena o nome da categoria.

O model **Announcement** armazena as informações de anúncios e novidades e ele contém o seguinte campos:

  * **_title_** campo do tipo CharField que armazena o título do anúncio.

  * **_description_** campo do tipo TextField que armazena a descrição do anúncio.

  * **_image_** campo do tipo ImageField que contém uma refêrencia ao arquivo de imagem do anúncio.
  
  * **_date\_posted_** campo do tipo DateTimeField que armazena a data e hora da postagem do anúncio.