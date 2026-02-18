from tempfile import template
from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from config import config
from models.entities.User import User
from models.ModelUser import ModelUser
from flask_login import LoginManager, login_user, logout_user

makeupvelaApp=Flask (__name__)

db              =MySQL(makeupvelaApp)
adminUsuario = LoginManager(makeupvelaApp)

@adminUsuario.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id)
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
        
        return render_template('registro.html')

@makeupvelaApp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0,None,request.form['correo'],request.form['clave'],None)
        usuarioAutenticado = ModelUser.signin(db, usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado)
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template('usuario.html')
            else:
                return 'Contraseña incorrecta'
        else:
            return 'Usuario inexistente'
    else:
        return render_template('signin.html')            


if __name__ == '__main__':
    makeupvelaApp.config.from_object(config['development'])
    makeupvelaApp.run(port=5025,debug=True)
