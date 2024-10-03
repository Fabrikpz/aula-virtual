from flask import render_template, redirect, url_for, flash, request
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask import Blueprint
from .models import Curso


main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        cursos = Curso.query.filter((Curso.user_id == current_user.id) | (Curso.usuarios.any(User.id == current_user.id))).all()
    else:
        cursos = []

    return render_template("home.html", cursos=cursos)


@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data) 
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
            login_user(user)
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

@main.route('/crear_cursos', methods=['GET', 'POST']) 
@login_required
def crear_cursos():
    if request.method == 'POST':
        curso_nombre = request.form.get('curso_nombre')
        curso_descripcion = request.form.get('curso_descripcion')

        if not curso_nombre or not curso_descripcion:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('main.crear_cursos'))

        nuevo_curso = Curso(nombre=curso_nombre, descripcion=curso_descripcion, user_id=current_user.id)  # user_id asignado correctamente
        db.session.add(nuevo_curso)
        db.session.commit()

        flash('Curso creado exitosamente', 'success')
        return redirect(url_for('main.home'))

    return render_template('cursos.html')

@main.route('/eliminar_curso/<int:curso_id>', methods=['POST'])
@login_required
def eliminar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    if curso.user_id != current_user.id:
        flash('No tienes permiso para eliminar este curso', 'danger')
        return redirect(url_for('main.home'))
    
    db.session.delete(curso)
    db.session.commit()
    flash('Curso eliminado exitosamente', 'success')
    return redirect(url_for('main.home'))

@main.route('/actualizar_curso/<int:curso_id>', methods=['GET', 'POST'])
@login_required  
def actualizar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id) 

    if request.method == 'POST':
        curso.nombre = request.form.get('curso_nombre')
        curso.descripcion = request.form.get('curso_descripcion')

        if not curso.nombre or not curso.descripcion:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('main.actualizar_curso', curso_id=curso_id))

        db.session.commit() 
        flash('Curso actualizado exitosamente', 'success')
        return redirect(url_for('main.home'))

    return render_template('actualizar_curso.html', curso=curso)

@main.route('/asignar_estudiante/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def asignar_estudiante(curso_id):
    curso = Curso.query.get_or_404(curso_id)

    if request.method == 'POST':
        email_estudiante = request.form.get('email_estudiante')
        usuario = User.query.filter_by(email=email_estudiante).first()

        if usuario:
            if usuario not in curso.usuarios:  # Verifica si ya está asignado
                curso.usuarios.append(usuario)
                db.session.commit()
                flash(f'Usuario {usuario.username} asignado al curso.', 'success')
            else:
                flash('El usuario ya está asignado a este curso.', 'warning')
            return redirect(url_for('main.home'))
        else:
            flash('Usuario no encontrado', 'danger')

    return render_template('asignar_estudiante.html', curso=curso)

@main.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)
