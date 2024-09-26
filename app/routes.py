from flask import render_template, redirect, url_for, flash, request
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Hasheamos la contraseña aquí
        db.session.add(user)
        db.session.commit()
        flash('¡Tu cuenta ha sido creada!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Registro', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # Agrega esta línea para autenticar al usuario
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Inicio de sesión fallido. Revisa tus credenciales', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/crear_cursos")
@login_required
def crear_cursos():
    return render_template("cursos.html")