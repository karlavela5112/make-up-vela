from tempfile import template
from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from config import config

makeupvelaApp=Flask (__name__)

db              =MySQL(makeupvelaApp)

@makeupvelaApp.route('/')
def home():
    ""
    return render_template('home.html')
@makeupvelaApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.form == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo'] 
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        regUsuario = db.conection.cursor()
        regUsuario = db.execute("INSERT INTO usuarios (nombre, correo, clave) VALUES (%s, %s, %s)", (nombre.upper(), correo, claveCifrada))
        db.conection.commit()
        regUsuario.close()
        return render_template('home.html')
    else:
        """Renderiza el formulario de registrO"""
        return render_template('registro.html')
    
if __name__ == '__main__':
    makeupvelaApp.config.from_object(config['development'])
    makeupvelaApp.run(port=5025,debug=True)
