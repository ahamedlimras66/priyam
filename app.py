import os
import json
import datetime
from models.form import *
from models.schema import *
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from InvoiceGenerator.pdf import SimpleInvoice
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, send_file, request, url_for, redirect, send_from_directory, jsonify, Response

os.environ["INVOICE_LANG"] = "en"
app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'my-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'


@app.before_first_request
def create_tables():
    db.create_all()

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

@app.route('/product/<id>')
def find_product(id):
    product = Product.query.filter_by(id=id).first()

    iteam = {}
    iteam['id'] = product.id
    iteam['name'] = product.name
    iteam['price'] = product.price

    return jsonify(iteam)

@app.route('/customer/<id>')
def find_customer(id):
    customer = Customer.query.filter_by(id=id).first()

    iteam = {}
    iteam['id'] = customer.id
    iteam['name'] = customer.name
    iteam['town_city'] = customer.town_city
    iteam['address'] = customer.address
    iteam['phoneno'] = customer.phone

    return jsonify(iteam)

@app.route('/getdata/<jsdata>')
def get_data(jsdata):
    data = json.loads(jsdata)
    print(data)
    print(data['customer_id'])
    new_invoice = Invoice(customer_id=data['customer_id'],
                          invoice_date=datetime.datetime.now())
    db.session.add(new_invoice)
    db.session.commit()

    for i in range(len(data['product_id'])):
        new_iteam = Iteam(invoiceid=new_invoice.id,
                          productid=data['product_id'][i],
                          quantity=data['quatity'][i])
        db.session.add(new_iteam)
        db.session.commit()

    generate_bill(data,new_invoice.id)

    return Response(status=200)

@app.route("/")
def home():
    form = BillForm()
    customers = db.session.query(Customer).all()
    product = db.session.query(Product).all()

    form.productname.choices = [(iteam.id,iteam.name) for iteam in product]
    form.customername.choices = [(customer.id,customer.name) for customer in customers]


    return render_template("home.html",form=form)

@app.route("/newProduct", methods=['POST','GET'])
def newProduct():
    form = NewProductForm()
    if form.validate_on_submit():

        newProduct = Product(name=form.productname.data,
                            price=form.price.data)
        db.session.add(newProduct)
        db.session.commit()

    return render_template("newproduct.html",form=form)

@app.route("/editProduct", methods=['POST','GET'])
def editProduct():
    form = EditProductForm()
    product = db.session.query(Product).all()
    form.productname.choices = [(iteam.id,iteam.name) for iteam in product]

    if form.validate_on_submit():
        product = Product.query.filter_by(id=form.productname.data).first()
        product.price = form.price.data
        db.session.commit()

    return render_template("editproduct.html", form=form)

@app.route("/newCustomer", methods=['POST','GET'])
def newCustomer():
    form = NewCustomerForm()
    if form.validate_on_submit():
        newCustomer = Customer(name=form.customername.data,
                                town_city=form.town_city.data,
                                address=form.address.data,
                                phone=form.phoneno.data)
        db.session.add(newCustomer)
        db.session.commit()

    return render_template("newcustomer.html",
                            form=form)

@app.route('/report')
def report():
    return render_template("report.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
	from db import db
	db.init_app(app)
	app.run(debug=True)