from app import db
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Tabla intermedia para la relación muchos a muchos entre usuarios y cursos
usuario_curso = db.Table('usuario_curso',
    db.Column('usuario_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('curso.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Nombre de la tabla
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    # Relación muchos a muchos con cursos
    cursos = db.relationship('Curso', secondary=usuario_curso, backref=db.backref('usuarios', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Curso(db.Model):
    __tablename__ = 'curso'  # Nombre correcto de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creador = db.relationship('User', backref=db.backref('cursos_creados', lazy='dynamic'))

    def agregar_contenido(self, titulo, texto, user_id):
        if user_id == self.user_id:
            nuevo_contenido = Contenido(titulo=titulo, texto=texto, curso_id=self.id)
            db.session.add(nuevo_contenido)
            db.session.commit()
            return True
        return False  # No se permite agregar contenido si el usuario no es el creador

    def agregar_examen(self, titulo, nota, user_id):
        if user_id == self.user_id:
            nuevo_examen = Examen(titulo=titulo, nota=nota, curso_id=self.id)
            db.session.add(nuevo_examen)
            db.session.commit()
            return True
        return False  # No se permite agregar examen si el usuario no es el creador

class Contenido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    curso = db.relationship('Curso', backref='contenidos')

class Examen(db.Model):
    __tablename__ = 'examen'  # Cambia el nombre de la tabla a 'examen'
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(255), nullable=False)  # Asegúrate de que esto sea necesario
    titulo = db.Column(db.String(255), nullable=False)
    nota = db.Column(db.Float)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'))  # Cambia a 'curso.id'
    estudiante_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Cambia a 'user.id'

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    examen_id = db.Column(db.Integer, db.ForeignKey('examen.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)

    estudiante = db.relationship('User', backref='notas')
    examen = db.relationship('Examen', backref='notas')  # Relación inversa con Examen
