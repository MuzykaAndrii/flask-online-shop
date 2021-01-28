from flask import Blueprint, render_template, request, url_for, flash, abort, redirect
from app.forms import CreateProductForm
from app.models import Product, User
from flask_login import login_required, current_user
from datetime import datetime as dt
from app.utils import *
from app import app

products = Blueprint('products', __name__, template_folder='templates')

@products.route("/")
def index():
    return redirect(url_for('products.get_products'))

@products.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    creator = User.query.get(product.seller_id).username
    product.views = int(product.views) + 1
    product.save()
    return render_template('products/product.html', title=product.title, product=product, creator=creator)

####### CREATE POST
@products.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = CreateProductForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        creator_id = current_user.id
        price = form.price.data
        quantity = form.quantity.data
        pictures = list()
        for f in form.pictures.data:
            pictures.append(save_picture(f, app.root_path + app.config['PRODUCTS_PICS_DIR']))
        
        product = Product(title, description, creator_id, price, quantity, pictures)
        product.save()

        flash('Product created successfully', 'success')
        return redirect(url_for('products.product', product_id=product.id))

    return render_template('products/create_product.html', title='Create new product', form=form)

################ GET FROM SELLER
@products.route('/products/<string:seller_name>', methods=['GET'])
def get_seller_products(seller_name):
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    
    creator = User.query.filter_by(username=seller_name).first_or_404()
    products = creator.products.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    desc = 'All products from {}'.format(seller_name)
    return render_template('products/products.html', title='Products', products=products, desc=desc)

######## GET POSTS
@products.route('/products', methods=['GET'])
def get_products():
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search_query')

    if search_query:
        # paginate according to search query
        products = Product.query.filter(Product.title.contains(search_query) | Product.description.contains(search_query)).paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    else:
        #paginate simply
        products = Product.query.order_by(Product.date_posted.desc()).paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    return render_template('products/products.html', title='Products', products=products)

###### UPDATE POST
@products.route('/product/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id:
        abort(403)

    form = CreateProductForm()

    if form.validate_on_submit():
        product.title = form.title.data
        product.description = form.description.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.date_posted = dt.now()
        product.save()

        flash('Product successfully updated', 'success')
        return redirect(url_for('products.product', product_id=product.id))
    
    elif request.method == 'GET':
        form.title.data = product.title
        form.description.data = product.description
        form.price.data = product.price
        form.quantity.data = product.quantity
    
    return render_template('products/update_product.html', title='Edit product', form=form, product_id=product.id)

####### DELETE POST
@products.route('/product/<int:product_id>/delete')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.seller_id != current_user.id:
        abort(403)
    product.delete()
    flash('Your product hes been deleted!', 'success')
    return redirect(url_for('products.get_products'))