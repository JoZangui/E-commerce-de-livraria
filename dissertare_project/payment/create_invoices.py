import os

from dissertare_project.settings import MEDIA_ROOT

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator


class CreateInvoce():
    def __init__(self, cliente_name:str, cliente_email:str, cliente_phone:str, cliente_address:str, invoice_number:str) -> None:
        os.environ["INVOICE_LANG"] = 'en'

        # Header
        # client info
        self.client = Client(cliente_name)
        self.client.email = cliente_email
        self.client.phone = cliente_phone
        self.client.address = cliente_address

        # Our info
        self.provider = Provider('Dissertare', bank_account='2600420569', bank_code='2010')
        self.provider.email = 'dissertare@comapany.com'
        self.provider.phone = '933333333'
        self.provider.address = 'Luanda'
        self.creator = Creator('John Doe')

        self.invoice = Invoice(self.client, self.provider, self.creator)
        self.invoice.currency = 'Kz'
        self.invoice.number = invoice_number

    def add_item(self, quantities:int, price:float, description:str) -> None:
        self.invoice.add_item(Item(quantities, price, description))

    def create_invoice_file(self) -> str:

        from InvoiceGenerator.pdf import SimpleInvoice

        # create invoice pdf
        self.invoice_pdf = SimpleInvoice(self.invoice)
        self.files_dir = os.path.join(MEDIA_ROOT,f'invoices\invoice_{self.invoice.number}.pdf')
        self.invoice_pdf.gen(self.files_dir, generate_qr_code=True)

        return self.files_dir
