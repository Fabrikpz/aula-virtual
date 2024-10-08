from flask import render_template, redirect, url_for, flash, request
from app import db
from app.forms import RegistrationForm, LoginForm, ContenidoForm, ExamenForm
from app.models import User, Curso, Contenido, Examen, Nota
from flask_login import login_user, current_user, logout_user, login_required
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        cursos = Curso.query.filter(
            (Curso.creador.has(id=current_user.id)) | 
            (Curso.usuarios.any(User.id == current_user.id))
        ).all()
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

        nuevo_curso = Curso(nombre=curso_nombre, descripcion=curso_descripcion, user_id=current_user.id)
        
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
            if usuario not in curso.usuarios:
                curso.usuarios.append(usuario)
                db.session.commit()
                flash('Estudiante asignado exitosamente', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('El usuario ya está asignado a este curso.', 'warning')
        else:
            flash('Usuario no encontrado', 'danger')

        return redirect(url_for('main.asignar_estudiante', curso_id=curso_id))

    return render_template('asignar_estudiante.html', curso=curso)

@main.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

@main.route('/curso/<int:curso_id>', methods=['GET'])
@login_required
def curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)

    if current_user not in curso.usuarios and current_user.id != curso.user_id:
        flash('No tienes acceso a este curso', 'danger')
        return redirect(url_for('main.home'))

    examenes = Examen.query.filter_by(curso_id=curso.id).all()

    return render_template('curso.html', curso=curso, examenes=examenes)

@main.route('/agregar_contenido/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def agregar_contenido(curso_id):
    form = ContenidoForm()
    curso = Curso.query.get_or_404(curso_id)

    if form.validate_on_submit():
        nuevo_contenido = Contenido(titulo=form.titulo.data, texto=form.texto.data, curso_id=curso.id)
        db.session.add(nuevo_contenido)
        db.session.commit()
        flash('Contenido agregado exitosamente', 'success')
        return redirect(url_for('main.home'))

    return render_template('agregar_contenido.html', form=form, curso=curso)

@main.route('/agregar_examen/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def agregar_examen(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    form = ExamenForm()

    if form.validate_on_submit():
        nuevo_examen = Examen(titulo=form.titulo.data, contenido=form.contenido.data, curso_id=curso.id)
        db.session.add(nuevo_examen)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('agregar_examen.html', form=form, curso=curso)

@main.route('/asignar_notas/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def asignar_notas(curso_id):
    curso = Curso.query.get_or_404(curso_id)

    if current_user.id != curso.user_id:
        flash('No tienes permiso para asignar notas en este curso.', 'error')
        return redirect(url_for('main.curso', curso_id=curso.id))

    estudiantes = curso.usuarios
    for estudiante in estudiantes:
        estudiante.notas = Nota.query.filter_by(estudiante_id=estudiante.id, curso_id=curso.id).all()

    if request.method == 'POST':
        for key in request.form:
            if key.startswith("nota_"):
                est_id = key.split("_")[1]
                nota_valor = request.form[key]
                nota_registro = Nota.query.filter_by(estudiante_id=est_id, curso_id=curso.id).first()
                if nota_registro:
                    nota_registro.valor = nota_valor
                else:
                    nueva_nota = Nota(estudiante_id=est_id, curso_id=curso.id, valor=nota_valor)
                    db.session.add(nueva_nota)

        db.session.commit()
        flash('Notas asignadas exitosamente', 'success')
        return redirect(url_for('main.curso', curso_id=curso.id))

    return render_template('asignar_notas.html', curso=curso, estudiantes=estudiantes)

@main.route('/eliminar_examen/<int:curso_id>/<int:examen_id>', methods=['POST'])
@login_required
def eliminar_examen(curso_id, examen_id):
    curso = Curso.query.get_or_404(curso_id)
    examen = Examen.query.get_or_404(examen_id)

    if current_user.id != curso.user_id:
        flash('No tienes permiso para eliminar este examen.', 'danger')
        return redirect(url_for('main.curso', curso_id=curso.id))

    db.session.delete(examen)
    db.session.commit()
    flash('Examen eliminado exitosamente', 'success')
    return redirect(url_for('main.curso', curso_id=curso.id))
