from flask import render_template, redirect, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets
import os



@app.route('/')
def home():
    products = Addproduct.query.filter(Addproduct.stock > 0)
    return render_template('products/index.html', products=products)



@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'Your brand has been updated', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/updatebrand.html', title='Update brand', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} cant be deleted from your database', 'warning')
    return redirect(url_for('admin'))



@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcat = request.form.get('category')
        brand = Category(name=getcat)
        db.session.add(brand)
        flash(f'The Categoty {getcat} was added to your database', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')


@app.route('/updatecat/<int:id>', methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Login first please', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('category'))
    category = updatecat.name
    return render_template('products/updatebrand.html', title='Update category page', updatecat=updatecat)



@app.route('/deletecategory/<int:id>', methods=['GET', 'POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'The brand {category.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The brand {category.name} cant be deleted from your database', 'warning')
    return redirect(url_for('admin'))





@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    form = Addproducts(request.form)
    brands = Brand.query.all()
    categories = Category.query.all()
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.description.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addproduct = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc, category_id=category,
                                brand_id=brand, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', brands=brands,categories=categories)

@app.route('/updateproduct/<int:id>', methods=['POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.desc = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Yor product {product.name} has been updated', 'success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.description.data = product.desc
    return render_template('products/updateproduct.html', form=form,  brands=brands, categories=categories, product=product)





#
# @app.route('/updateproduct/<int:id>', methods=['GET','POST'])
# def updateproduct(id):
#     brands = Brand.query.all()
#     categories = Category.query.all()
#     product = Addproduct.query.get_or_404(id)
#     brand = request.form.get('brand')
#     category = request.form.get('category')
#     form = Addproducts(request.form)
#     if request.method == "POST":
#         product.name = form.name.data
#         product.price = form.price.data
#         product.discount = form.discount.data
#         product.brand_id = brand
#         product.category_id = category
#         product.colors = form.colors.data
#         product.desc = form.description.data
#         if request.method == "POST":
#             try:
#                 product.image_1 =os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
#                 product.image_2 = os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
#                 product.image_3 = os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
#             except Exception as e:
#                 print(e)
#         db.session.commit()
#         flash(f'Yor product {product.name} has been updated', 'success')
#         return redirect(url_for('admin'))
#     form.name.data = product.name
#     form.price.data = product.price
#     form.discount.data = product.discount
#     form.stock.data = product.stock
#     form.colors.data = product.colors
#     form.description.data = product.desc
#     return render_template('products/updateproduct.html', form=form,  brands=brands, categories=categories, product=product)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))