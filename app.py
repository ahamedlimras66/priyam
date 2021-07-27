import os
# from InvoiceGenerator.pdf import SimpleInvoice
from flask import Flask, url_for
from route.home import home

os.environ["INVOICE_LANG"] = "en"
app = Flask(__name__)

def generate_bill(info,invoice_number):
    from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator

    client = Client(info['bill_name'])
    provider = Provider('AB', bank_account='1', bank_code='2010')
    creator = Creator('John Doe')

    invoice = Invoice(client, provider, creator)
    invoice.currency_locale = 'en_US.UTF-8'
    invoice.currency = u'₹'
    invoice.number = invoice_number

    for i in range(len(info['product_id'])):
        invoice.add_item(Item(info['quatity'][i], info['product_price'][i], description=info['product_name'][i]))


    pdf = SimpleInvoice(invoice)
    pdf.gen("bills/"+str(invoice_number)+".pdf", generate_qr_code=True)

app.register_blueprint(home, url_prefix="/")

if __name__ == "__main__":
	app.run(debug=True)