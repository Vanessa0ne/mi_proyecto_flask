from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Inicializa la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_super_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopciones.db'

# Inicializa la base de datos
db = SQLAlchemy(app)

# Modelo para la base de datos
class Adopcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(15), nullable=False)

# Formulario para el registro de adopciones
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre del adoptante', validators=[DataRequired()])
    contacto = StringField('Número de contacto', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# Ruta para la página de registro de adopciones
@app.route('/', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        nueva_adopcion = Adopcion(nombre=form.nombre.data, contacto=form.contacto.data)
        db.session.add(nueva_adopcion)
        db.session.commit()
        return redirect(url_for('lista_adopciones'))
    return render_template('registro.html', form=form)

# Ruta para mostrar la lista de adopciones
@app.route('/adopciones')
def lista_adopciones():
    adopciones = Adopcion.query.all()
    return render_template('lista_adopciones.html', adopciones=adopciones)

# Inicializa la base de datos y ejecuta la aplicación
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos si no existen
    app.run(debug=True)
