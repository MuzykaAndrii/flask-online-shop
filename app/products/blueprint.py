from flask import Blueprint, render_template, request, url_for, flash, abort, redirect
from app.forms import CreateProductForm
from app.models import Product, User
from flask_login import login_required, current_user
from datetime import datetime as dt

products = Blueprint('products', __name__, template_folder='templates')

@products.route("/")
def index():
    return redirect(url_for('products.get_products'))

@products.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    creator = User.query.get(product.seller_id).username
    return render_template('products/product.html', title=product.title, product=product, creator=creator)

####### CREATE POST
@products.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = CreateProductForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        creator_id = current_user.id

        product = Product(title, content, creator_id)
        product.save()

        flash('Product created successfully', 'success')
        return redirect(url_for('products.product', product_id=product.id))

    return render_template('products/create_product.html', title='Create new product', form=form)


######## GET POSTS
@products.route('/products', methods=['GET'])
def get_products():
    # Set the pagination configuration
    POSTS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search_query')

    if search_query:
        # paginate according to search query
        products = Product.query.filter(Product.title.contains(search_query) | Product.content.contains(search_query)).paginate(page=page, per_page=POSTS_PER_PAGE)
    else:
        #paginate simply
        products = Product.query.paginate(page=page, per_page=POSTS_PER_PAGE)

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
        product.content = form.content.data
        product.date_producted = dt.now()
        product.save()

        flash('Product successfully updated', 'success')
        return redirect(url_for('products.product', product_id=product.id))
    
    elif request.method == 'GET':
        form.title.data = product.title
        form.content.data = product.content
    
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