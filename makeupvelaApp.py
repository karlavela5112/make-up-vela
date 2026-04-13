from tempfile import template
from flask import Flask, render_template,redirect, url_for, request,flash
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
        flash('Usuario registrado') 
        db.conection.commit()
        regUsuario.close()
        return redirect(url_for('signin'))
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
                    selProducto = db.connection.cursor()
                    selProducto.execute("SELECT * FROM productos")
                    p = selProducto.fetchall()
                    selProducto.close()
                    return render_template('usuario.html', productos=p)
            else:
                flash ('Contraseña incorrecta')
                return render_template('signin.html')
        else:
            flash ('Usuario inexistente')
            return render_template('signin.html')
    else:
        return render_template('signin.html')  
@makeupvelaApp.route('/signout')
def signout():
    logout_user()
    return render_template('home.html')

@makeupvelaApp.route('/sUsuario',methods = ['GET','POST'])
def sUsuario():
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuarios")
    u = selUsuario.fetchall()
    selUsuario.close()
    return render_template('users.html', usuarios=u)

@makeupvelaApp.route('/signin', methods=["GET", "POST"])
def signout():
    logout_user()
    return render_template('home.html')
@makeupvelaApp.route('/iUsuario', methods=["GET", "POST"])
def iUsuario():
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['correo'] 
            clave = request.form['clave']
            claveCifrada = generate_password_hash(clave)
            perfil = request.form['perfil']
            regUsuario = db.connection.cursor()
            regUsuario.execute("INSERT INTO usuarios (nombre, correo, clave, perfil) VALUES (%s, %s, %s, %s)", (nombre.upper(), correo, claveCifrada, perfil))
            flash('Usuario registrado') 
            db.connection.commit()
            regUsuario.close()
            return redirect(url_for('sUsuario'))
        else:
            return render_template('users.html')
@makeupvelaApp.route('/uUsuario/<int:id>', methods=['GET', 'POST'])
def uUsuario(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo'] 
        clave = request.form['clave']
        perfil = request.form['perfil']
        actUsuario = db.connection.cursor()
        actUsuario.execute("UPDATE usuarios SET nombre=%s, correo=%s, clave=%s, perfil=%s WHERE id=%s", (nombre.upper(), correo, clave, perfil, id))
        db.connection.commit()
        actUsuario.close()
        return redirect(url_for('sUsuario'))
    else:
       return redirect(url_for('sUsuario'))
@makeupvelaApp.route('/dUsuario/<int:id>', methods=['GET', 'POST'])
def dUsuario(id):
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        delUsuario.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        db.connection.commit()
        delUsuario.close()
        flash('Usuario eliminado')
        return redirect(url_for('sUsuario'))
    else:
        return render_template('users.html')
     
if __name__ == '__main__':
    makeupvelaApp.config.from_object(config['development'])
makeupvelaApp.run(port=5025,debug=True)


