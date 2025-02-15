# E-commerce de livraria

<h4 align="center"> 
    :construction:  Projeto em construção  :construction:
</h4>

* [Books](#books-app)
  * [views](#views-de-books)
  * [models](#models-de-books)
  * [signals](#signals-de-books)
  * [announcement](#announcement-de-books)
  * [pdf_file_validator](#pdf_file_validator-de-books)
* [Users](#users-app)
  * [views](#views-de-users)
  * [models](#models-de-users)
  * [signal](#signals-de-users)
  * [tokens](#tokengenerator)
* [Payment](#payment-app)
  * [views](#views-de-payment)
  * [models]()
  * [signal]()
  * [create_invoices]()
* [Cart]()
  * [views]()
  * [models]()
  * [cart]()
* [context_processors](#context_processors)
* [Forms](#forms)


## Books app

Na app **Books** encontramos tudo relacionado ao livro, desde modelos, formulários de validação até views, nesta app também reside a view para a página home.

### Views de books

Logo no início encontraremos a função **_user_is_superuser** que é usado pelo decorador *__@user_passes_test__* para verificar se o usuário que está tentando aceder a view em questão é um **super_user**. Esta função recebe como argumento o **user** o qual é usado para verificar se o usuário é ou não um **super_user**, a função retorna *__True__* se o usuário for um **super_user** e *__False__* se não for. Se o usuário não for um **super_user** então *__@user_passes_test__* retorna o usuário para a página home.
```python
def _user_is_superuser(user):
    """
    retorna True se o usuário
    é um super usuário, se não, retorna False
    """
    return user.is_superuser
```
```python
@user_passes_test(_user_is_superuser, login_url='home')
def upload_book(request):
  ...
```

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

### Signals de Books
O Signal **delete_book_files_signal** elimina do sistema de ficheiros o arquivo, seja este PDF ou imagem, do livro em questão, quando o mesmo for removido da base de dados.

O signal **delete_old_book_image_file_signal** elimina o arquivo de imagem quando carregarmos uma nova imagem para um livro que já se encontra na base de dados.

O signal **delete_old_book_pdf_file_signal** elimina o arquivo PDF quando carregarmos um novo arquivo PDF para um livro que já se encontra na base de dados.

### Announcement de Books
**Announcement** é usado pelo **_context\_processors_** de books para disponibilizar anúncios e novidades de página, sem que este tenha que recorrer a **views**.

### pdf_file_validator de Books
A função **pdf_format_validator** verifica se o ficheiro carregado pelo formulário é um PDF, se não, ela levanta um ValidationError. ele é usado em **_validators_** de models.

## Users app

Na app **Users** encontramos tudo relacionado ao usuário seja este **_super\_user_** ou um usuário comum, desde modelos, formulários de validação até views.

### Views de Users
A view **register** é responsável pela página de registo de usuários. Em caso de sucesso ela envia um email para o usuário com um link de confirmação e redireciona o usuário para uma página com a mensagem **_"Por favor confirme o seu endereço de email para completar o registro"_**.

A view **activate** é uma view de ativação de conta, ela é acessada pelo link enviado pela view **register**
```python
  def register(request):
    """ view para registro de usuário """
    ...
    """ Mensagem de confirmação de e-mail """
    # pega o endereço actual do site
    current_site = get_current_site(request)
    # assunto do email que será enviado
    mail_subject = 'Activate your blog account.'
    # renderiza um template html para a forma de string
    message = render_to_string(
        'users/email_template.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
    )
    # destinatário do email
    to_email = form.cleaned_data.get('email')
    # objecto responsável pelo envio do email
    email = EmailMessage(mail_subject, message, to=[to_email])
    # envio do email
    email.send(fail_silently=False)
```

ela verifica o Token de ativação e o usuário,
```python
  def activate(request, uidb64, token):
    """
    View de activação de conta
    
    VIEW ACESSADA COM O LINK DE ACTIVAÇAO DE CONTA
    QUE FOI ENVIADA PARA O EMAIL DO NOVO USUÁRIO
    """

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # se o user for diferente de 'None'
        # e as informções do token geradas estiverem de acordo 
        # ele define a propriedade de usuário activado como sendo 'True'
        user.is_active = True
        # e depois salva essa informação do usuário
        user.save()
        # faz o login do novo usuário
        login(request, user)
        messages.success(request, 'Registro feito com sucesso')
        # Redireciona o usuário para a página do formulário de entrega
        return redirect('user-shipping-address')
```

em caso de sucesso a view emite a seguinte mensagem de sucesso **_"Registro feito com sucesso"_** e redireciona o usuário para a página de cadastro dos dados de entrega como vemos no exemplo a cima, e em caso de insucesso o usuário recebe a seguinte mensagem **_"Link de activação inválido!"_**. 
```python
  def activate(request, uidb64, token):
    """
    View de activação de conta
    
    VIEW ACESSADA COM O LINK DE ACTIVAÇAO DE CONTA
    QUE FOI ENVIADA PARA O EMAIL DO NOVO USUÁRIO
    """
    ...
    else:
          # Activation link is invalid
          return HttpResponse('Link de activação inválido!')
```

A view **login_user** tal como diz o nome é responsável pelo login do usuário, no processo de login ela verifica o carrinho salvo do usuário na base de dados e carrega os seus itens, caso o usuário tenha adicionou algum item ao carrinho enquanto não estava logado, ao fazer o login a view adiciona esse(s) item(ns) ao carrinho do usuário logado.

```python
def login_user(request):
  ...
  if user is not None:
    login(request, user)

    current_user = Profile.objects.get(user__id=user.id)
    # Get their saved cart from database
    saved_cart = current_user.user_cart
    # Convert database string to python dictionary
    if saved_cart:
        # Convert to dictionary using JSON
        converted_cart = json.loads(saved_cart)
        # Add the loaded cart dictionary to our session
        # Get the cart
        cart = Cart(request)
        # Loop thru the cart and add the items from the database
        for key, value in converted_cart.items():
            cart.add(book=key, quantity=value)
    messages.success(request, 'You Have Been Logged In!')
    return redirect('home')
```

A view **user_shipping_address** retorna uma página com o formulário de cadastro dos dados de entrega do usuário, ela também é responsável pela validação dos dados, em caso de success ela redireciona o usuário para a página home com a mensagem **_"Registro feito com sucesso"_**.

A view **update_user_shipping_address** é semelhante a view **user_shipping_address** mas para actualização dos dados de entrega.

A view **user_books** retorna uma página com os livros comprados pelo usuário.

A view **user_books_details** retorna uma página com os detalhes de um livro comprado pelo usuário.

A view **profile** tal como diz o nome, retorna a página de perfil do usuário.

A view **staff_profile** retorna uma página de perfil de administração para os membros do staff.

A view **upload_announcement** retorna uma página com o formulário de upload de anúncios e novidades.

### Models de Users
A app users tem apenas um model que é o **Profile**, ele armazena informações do usuário como o nome e os dados de entrega.

### Signals de Users
A app user também só contem um signal que é o **create_profile** que é responsável por criar um perfil para usuário tão logo o usuário se cadastrar no sistema com sucesso.

### TokenGenerator
O **TokenGenerator** é responsavel por gerar um token para o link de ativação de conta.

## Payment app
A app **Payment** é responsável pelo controle tanto do método de pagamento com o de entrega, nela também encontramos a view responsável pelo download dos livros, e o gerador de faturas

### Views de Payment

A view **order_conclusion** retorna a página de conclusão do processo de pedido, ela retorna uma mensagem de secesso ao usuário.

A view **not_shipped_dash** retorna uma página com a lista de pedidos não entregues, está página é só para administradores da página.

A view **not_shipped_to_shipped** é uam view de transição do pedido de não entregue para entregue.

A view **shipped_dash** retorna uma página com a lista de pedidos entregues.

<mark>As views acima citadas só podem ser acessadas por administradores da página, com excepção da view **order_conclusion**.</mark>

Apos de seleção dos itens, preenchimento do formulário de endereço de entrega e da escolha do método de pagamento, a view **process_order** processa o pedido do cliente com base nas informações anteriomente dadas pelo cliente.

ela salva as informações do pedido na base de dados criando um novo objecto **_Order_** e salvando os seus dados na base de dados.

```python
  ...
  # Create Order
  # Cria um pedido
  create_oder = Order(
      user=user,
      full_name=full_name,
      email=shipping_email,
      shipping_address=shipping_address,
      amount_paid=amount_paid
  )
  create_oder.save()
```

Ela também cria uma fatura aberta e envia para o email do cliente

```python
  ...
  # create invoice
  # Cria uma fatura
  invoice_number = f'E_Books_{order_id}'
  invoice = Invoices(order_id=order_id, invoice_number=invoice_number, payment_mode=payment_mode)
  invoice.save()

  """
  EN: Send an email to the customer with the invoice and book
  PT: Enviar um email para o cliente com a fatura e o livro
  """
  # pega o endereço actual do site
  current_site = get_current_site(request)
  # Email subject
  # Assunto do email
  mail_subject = 'Obrigado por comprar na livraria Dissertare'
  # renders an html template to string form
  # renderiza um template html para a forma de string
  message = render_to_string(
      'payment/payment_email_template.html',
      {
          'domain': current_site.domain,
          'order_id': order_id
      }
  )
  to_email = shipping_email
  email = EmailMessage(mail_subject, message, to=[to_email])
  email.attach_file(invoice.invoice_file.path)
  email.send(fail_silently=False)
```

no final a view elimina os itens do carrinho do cliente e redireciona o  cliente para a página de conclusão do pedido **order_conclusion**.

```python
  ...
  # Delete our cart
  # Exclui o nosso carrinho
  for key in list(request.session.keys()):
      if key == 'session_key':
          # Delete the key
          # Elimina a chave
          del request.session[key]

  """
  EN: Delete Cart from Database (user_cart field)
  PT: Elimina o carrinho da base de dados (campo user_cart)
  """
  current_user = Profile.objects.filter(user__id=request.user.id)
  # Delete shopping cart in Database (user_cart field)
  # Remove as informações do carrinho de compras da base de dados (campo user_cart)
  current_user.update(user_cart="")


  messages.success(request, "Pedido concluido com sucesso!")
  return redirect('order-conclusion')
```

A view **billing_info** retorna uma página com o fomulário método de pagamento. Ao submeter o formulário ela manda as informações para view **process_order** para a conclusão do pedido.

A view **checkout** é por onde começamos o processo do pedido, ela é acessada pela link na página do carrinho. está view retorna uma página com o formulário dos dados do local de entrega.

A view **ordered_books** retorna uma página com os livros digitais que o usuário comprou, essa página é acessada pelo link enviado ao cliente após o termino da compra.

A view **download_book** é responsável pelo download do livro

## context_processors
Os **context_processors** são usados para disponibilizar conteudos em todas a páginas do site sem a utilização de alguma view em específico.
O seu conteudo é disponibilizado como contexto de templates em **_OPTIONS.context\_processors_** de **_TEMPLATES_** que se encontra em **_settings.py_**. Ele funciona de forma semelhante ao context das views mas no entanto disponibilizada para todos os templates do site e não apenas para um.

## Forms
No geral os forms têm a mesma caracteristica, eles fazem referência a um **_model_** com os seus respectivos campos. Usamos o dicionário **_widgets_** para adicionar alguns atributos como classes Bootstrap, placeholder, maxlength e muito mais, tudo isto em **_class Meta_**. **PaymentForm** é a única Exceção, ele não faz a referência a algum **_model_** diretamente.