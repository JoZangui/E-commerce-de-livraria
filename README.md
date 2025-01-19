# E-commerce de livraria
 * [Books](#books-app)
   * [views](#views-de-books)
   * [models]()
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
