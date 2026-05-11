from tempfile import template
from tkinter import INSERT
from flask import Flask, render_template,redirect, url_for, request,flash, session
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
makeupvelaApp.secret_key = 'clave_secreta_cambia_esto'

makeupvelaApp.config.from_object(config['development'])
makeupvelaApp.config.from_object(config['mail'])


db              =MySQL(makeupvelaApp)
adminUsuario = LoginManager(makeupvelaApp)
mail = Mail(makeupvelaApp)

@adminUsuario.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id)

@makeupvelaApp.route('/', methods=['GET'])
def home():
    # Obtener productos de la base de datos
    selProducto = db.connection.cursor()
    selProducto.execute("SELECT * FROM productos")
    productos = selProducto.fetchall()
    selProducto.close()
    # Carrito desde sesión
    carrito = session.get('carrito', [])
    total_carrito = sum(item['precio'] * item['cantidad'] for item in carrito) if carrito else 0
    return render_template('home.html', productos=productos, carrito=carrito, total_carrito=total_carrito)

# Ruta para agregar producto al carrito
@makeupvelaApp.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    producto_id = int(request.form['producto_id'])
    cantidad = int(request.form.get('cantidad', 1))
    # Buscar producto en la base de datos
    selProducto = db.connection.cursor()
    selProducto.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    producto = selProducto.fetchone()
    selProducto.close()
    if not producto:
        flash('Producto no encontrado')
        return redirect(url_for('home'))
    # Preparar item carrito
    item = {
        'id': producto['id'],
        'nombre': producto['nombre'],
        'precio': producto['precio'],
        'cantidad': cantidad
    }
    carrito = session.get('carrito', [])
    # Si ya está en el carrito, sumar cantidad
    for prod in carrito:
        if prod['id'] == item['id']:
            prod['cantidad'] += cantidad
            break
    else:
        carrito.append(item)
    session['carrito'] = carrito
    flash('Producto agregado al carrito')
    return redirect(url_for('home'))

# Ruta para actualizar cantidad en el carrito
@makeupvelaApp.route('/actualizar_carrito', methods=['POST'])
def actualizar_carrito():
    producto_id = int(request.form['producto_id'])
    cantidad = int(request.form.get('cantidad', 1))
    carrito = session.get('carrito', [])
    for prod in carrito:
        if prod['id'] == producto_id:
            prod['cantidad'] = cantidad
            break
    session['carrito'] = [p for p in carrito if p['cantidad'] > 0]
    flash('Carrito actualizado')
    return redirect(url_for('home'))

# Ruta para eliminar producto del carrito
@makeupvelaApp.route('/eliminar_del_carrito', methods=['POST'])
def eliminar_del_carrito():
    producto_id = int(request.form['producto_id'])
    carrito = session.get('carrito', [])
    carrito = [p for p in carrito if p['id'] != producto_id]
    session['carrito'] = carrito
    flash('Producto eliminado del carrito')
    return redirect(url_for('home'))

# Ruta para checkout
@makeupvelaApp.route('/checkout', methods=['POST'])
def checkout():
    session.pop('carrito', None)
    flash('¡Gracias por tu compra!')
    return redirect(url_for('home'))
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
@makeupvelaApp.route('/iCarrito/<int:id>', methods=['GET', 'POST'])
def iCarrito():
        if request.method == 'POST':
            SelProducto = db.connection.cursor()
            SelProducto.execute("SELECT * FROM productos WHERE id = %s", (id,))
            p= SelProducto.fetchone()
            producto = {
                'id': p[0],
                'nombre': p[1],
                'descripcion': p[2],
                'precio': float(p[3]),
                'nombre_img': p[4],
            }
            if 'carrito' not in session:
                session['carrito']= []
                carrito = session['carrito']
                carrito.append(producto)
                session['carrito']= carrito
                flash('producto agregado')
                return redirect(url_for('home'))
            
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
    makeupvelaApp.run(port=5025)


