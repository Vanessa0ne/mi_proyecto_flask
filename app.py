from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_super_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopciones.db'
db = SQLAlchemy(app)

class Adopcion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(15), nullable=False)

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre del adoptante', validators=[DataRequired()])
    contacto = StringField('Número de contacto', validators=[DataRequired()])
    submit = SubmitField('Registrar')

@app.route('/', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        nueva_adopcion = Adopcion(nombre=form.nombre.data, contacto=form.contacto.data)
        db.session.add(nueva_adopcion)
        db.session.commit()
        return redirect(url_for('lista_adopciones'))
    return render_template('registro.html', form=form)

@app.route('/adopciones')
def lista_adopciones():
    adopciones = Adopcion.query.all()
    return render_template('lista_adopciones.html', adopciones=adopciones)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
