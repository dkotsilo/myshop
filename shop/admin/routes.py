from flask import render_template, session, redirect, request, url_for, flash
from shop import app, db, bcrypt
from .models import User
from .forms import RegistrationForm
import os


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('admin/index.html', title='Admin Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Register page")

##and form.validate()