from tempfile import template
from tkinter import INSERT
from flask import Flask, render_template,redirect, url_for, request,flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from config import config
from models.entities.User import User
from models.ModelUser import ModelUser
from flask_login import LoginManager, login_user, logout_user
from flask_mail import Mail, Message
import os

makeupvelaApp=Flask (__name__)

makeupvelaApp.config.from_object(config['development'])
makeupvelaApp.config.from_object(config['mail'])


db              =MySQL(makeupvelaApp)
adminUsuario = LoginManager(makeupvelaApp)
mail = Mail(makeupvelaApp)

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
        msg = Message(subject='Bienvenido a Makeup Vela', recipients=[correo])
        msg.html = render_template('mail.html', usuario=nombre)
        mail.send(msg)
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

@makeupvelaApp.route('/sProducto',methods = ['GET','POST']) 
def sProducto():
    selProducto = db.connection.cursor()
    selProducto.execute("SELECT * FROM productos")
    p = selProducto.fetchall()
    selProducto.close()
    return render_template('productos.html', productos=p)

@makeupvelaApp.route('/uProductos/<int:id>' ,methods=['GET','POST'])
def uProductos(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']
        nombre_img = request.form['nombre_img_actual']
        imagen = request.files['imagen']
        if imagen and imagen.filename:
            nombre_img = secure_filename(imagen.filename)
            imagen.save(os.path.join('static/img', nombre_img))

        actProducto = db.connection.cursor()
        actProducto.execute(
            "UPDATE productos SET nombre=%s, descripcion=%s, categoria=%s, precio=%s, stock=%s, nombre_img=%s WHERE id=%s",
            (nombre, descripcion, categoria, precio, stock, nombre_img, id)
        )
        db.connection.commit()
        actProducto.close()
        flash("Producto actualizado exitosamente")
        return redirect(url_for('productos'))
    else:
        flash("Error al actualizar el producto")
        return redirect(url_for('productos'))
@makeupvelaApp.route('/iProducto', methods=['GET', 'POST'])
def iProducto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']
        imagen = request.files['imagen']
    nombre_img = None
    if imagen and imagen.filename:
        nombre_img = secure_filename(imagen.filename)
        imagen.save(os.path.join('static/img', nombre_img))
    NuevoProducto = db.connection.cursor()
    NuevoProducto.execute("INSERT INTO productos (nombre, descripcion, categoria, precio, stock, nombre_img) VALUES (%s, %s, %s, %s, %s, %s)", (nombre.upper(), descripcion, categoria, precio, stock, nombre_img))
    db.connection.commit()
    flash('Producto Agregado')
    NuevoProducto.close()
     return redirect(url_for('sProducto'))
    else:
    return render_template('productos.html')

if __name__ == '__main__':
    makeupvelaApp.run(port=5025,debug=True)


