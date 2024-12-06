import os

from dissertare_project.settings import MEDIA_ROOT

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator


class CreateInvoce():
    def __init__(self, cliente_email:str, cliente_address:str, cliente_city:str, invoice_number:str, payment_mode:str, creation_date) -> None:
        os.environ["INVOICE_LANG"] = 'en'

        # Header
        # client info
        self.client = Client(f'Método de pagamento: {payment_mode}')
        self.client.email = f'Email: {cliente_email}'
        self.client.address = cliente_address
        self.client.city = f'Cidade: {cliente_city}'

        # Our info
        self.provider = Provider('Dissertare', bank_account='2600420569', bank_code='2010')
        self.provider.email = 'dissertare@comapany.com'
        self.provider.phone = '933333333'
        self.provider.address = 'Luanda'
        self.creator = Creator('John Doe')

        self.invoice = Invoice(self.client, self.provider, self.creator)
        self.invoice.currency = 'Kz'
        self.invoice.number = invoice_number
        self.invoice.date = creation_date
        self.invoice.title = 'Fatura aberta'

    def add_item(self, quantities:int, price:float, description:str) -> None:
        self.invoice.add_item(Item(quantities, price, description))

    def create_invoice_file(self) -> str:

        from InvoiceGenerator.pdf import SimpleInvoice

        # create invoice pdf
        self.invoice_pdf = SimpleInvoice(self.invoice)
        # cria um caminho de directório de forma automática evitando problemas entre caminhos do tipo windows(\) e linux(/)
        self.files_dir = os.path.join(MEDIA_ROOT, 'invoices', f'invoice_{self.invoice.number}.pdf')
        self.invoice_pdf.gen(self.files_dir, generate_qr_code=True)

        return self.files_dir
