from tempfile import template
from flask import Flask, render_template, url_for requst
from werkzeug.security import generate_password_hash

makeupvelaApp=Flask (__name__)

@makeupvelaApp.route('/')
def home():
    ""
    return render_template('home.html')
@oldwearApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.form == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo'] \
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        regUsuario = db.conection.cursor()
        regUsuario = db.execute("INSERT INTO usuarios (nombre, correo, clave) VALUES (%s, %s, %s)", (nombre.upper(), correo, claveCifrada))
        db.conection.commit()
        regUsuario.close()
        return redirect(url_for'home.html')
    else:
        """Renderiza el formulario de registrO"""
        return render_template('registro.html')
    
if __name__ == '__main__':
    makeupvelaApp.run(debug=True)