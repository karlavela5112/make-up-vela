from tempfile import template
from tkinter import INSERT
from flask import Flask, render_template,redirect, url_for, request,flash, session
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from config import config
from models.entities.User import User
from models.ModelUser import ModelUser
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message
import os


makeupvelApp=Flask (__name__)
makeupvelApp.secret_key = 'clave_secreta_cambia_esto'

makeupvelApp.config.from_object(config['development'])
makeupvelApp.config.from_object(config['mail'])
print("HOST:", makeupvelApp.config['MYSQL_HOST'])
print("USER:", makeupvelApp.config['MYSQL_USER'])
print("DB:", makeupvelApp.config['MYSQL_DB'])
print("PORT:", makeupvelApp.config['MYSQL_PORT'])



db              =MySQL(makeupvelApp)
adminUsuario = LoginManager(makeupvelApp)
mail = Mail(makeupvelApp)

@adminUsuario.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id)

@makeupvelApp.route('/', methods=['GET'])
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
@makeupvelApp.route('/agregar_al_carrito', methods=['POST'])
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
@makeupvelApp.route('/actualizar_carrito', methods=['POST'])
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
@makeupvelApp.route('/eliminar_del_carrito', methods=['POST'])
def eliminar_del_carrito():
    producto_id = int(request.form['producto_id'])
    carrito = session.get('carrito', [])
    carrito = [p for p in carrito if p['id'] != producto_id]
    session['carrito'] = carrito
    flash('Producto eliminado del carrito')
    return redirect(url_for('home'))

# Ruta para checkout
@makeupvelApp.route('/checkout', methods=['POST'])
def checkout():
    session.pop('carrito', None)
    flash('¡Gracias por tu compra!')
    return redirect(url_for('home'))
@makeupvelApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo'] 
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        #msg = Message(subject='Bienvenido a Makeup Vela', recipients=[correo])
        #msg.html = render_template('mail.html', usuario=nombre)
        #mail.send(msg)
        regUsuario = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave) VALUES (%s, %s, %s)", (nombre.upper(), correo, claveCifrada))
        flash('Usuario registrado') 
        db.connection.commit()
        regUsuario.close()
        return redirect(url_for('home'))
    else: 
        return render_template('signup.html')

@makeupvelApp.route('/signin', methods=['GET', 'POST'])
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
                    selCarrito = db.connection.cursor()
                    selCarrito.execute(" SELECT cantidad  FROM carrito WHERE usuario_id = %s", (usuarioAutenticado.id,))
                    carrito = selCarrito.fetchall()
                    selCarrito.close()
                    session['num_articulos']= sum(c[0] for c in carrito)
                    return redirect(url_for('home_user')) 
            else:
                flash ('Contraseña incorrecta')
                return render_template('signin.html')
        else:
            flash ('Usuario inexistente')
            return render_template('signin.html')
    else:
        return render_template('signin.html')  
@makeupvelApp.route('/signout')
def signout():
    logout_user()
    return render_template('home.html')

@makeupvelApp.route('/sUsuario',methods = ['GET','POST'])
def sUsuario():
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuario")
    u = selUsuario.fetchall()
    selUsuario.close()
    return render_template('users.html', usuarios=u)

@makeupvelApp.route('/iUsuario', methods=["GET", "POST"])
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
@makeupvelApp.route('/uUsuario/<int:id>', methods=['GET', 'POST'])
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
@makeupvelApp.route('/dUsuario/<int:id>', methods=['GET', 'POST'])
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

@makeupvelApp.route('/sProducto',methods = ['GET','POST']) 
def sProducto():
    selProducto = db.connection.cursor()
    selProducto.execute("SELECT * FROM productos")
    p = selProducto.fetchall()
    selProducto.close()
    return render_template('productos.html', productos=p)

@makeupvelApp.route('/uProductos/<int:id>' ,methods=['GET','POST'])
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
    
@makeupvelApp.route('/home_user', methods=['GET','POST'])
def home_user():
      selProducto = db.connection.cursor()
      selProducto.execute("SELECT * FROM productos")
      p = selProducto.fetchall()
      selProducto.close()
      return render_template('usuario.html', productos=p)

@makeupvelApp.route('/home_admin', methods=['GET','POST'])
def home_admin():
    return render_template('admin.html')

@makeupvelApp.route('/sCarrito', methods=['GET', 'POST'])
@login_required
def sCarrito():
    selCarrito = db.connection.cursor()
    selCarrito.execute("SELECT * FROM detalle_carrito INNER JOIN productos ON detalle_carrito.producto_id = productos.id WHERE detalle_carrito.usuario_id = %s", (current_user.id,))
    detalles_carrito = selCarrito.fetchall()
    selCarrito.close()
    session['num_articulos'] = sum(c[3] for c in detalles_carrito)
    session['total_carrito'] = sum(c[4]for c in detalles_carrito)
    return render_template('carrito.html', carrito=detalles_carrito)

@makeupvelApp.route('/iCarrito/<int:id>', methods=['GET', 'POST'])
def iCarrito():
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        SelProducto = db.connection.cursor()
        SelProducto.execute("SELECT * FROM detalle_carrito WHERE usuario_id = %s AND producto_id = %s", (current_user.id, id))
        p= SelProducto.fetchone()
        SelProducto.close()
        if p:
            nueva_cantidad = p[3] + int(cantidad)
            actCarrito= db.connection.cursor()
            actCarrito.execute("UPDATE detalle_carrito SET cantidad=%s, importe=%s WHERE usuario_id= %s AND producto_id= %s", (nueva_cantidad, nueva_cantidad,* float(precio), current_user.id, id))
            db.connection.commit()
            actCarrito.close()
            flash('Producto actualizado en el carrito')
        else:
            NuevoCarrito = db.connection.cursor()
            NuevoCarrito.execute("INSERT INTO detalle_carrito (usuario_id, producto_id, cantidad, importe) VALUES (%s, %s, %s, %s)", (current_user.id, id, cantidad, float(precio) * int(cantidad)))
            db.connection.commit()
            NuevoCarrito.close()

            flash('producto agregado al carrito')
            return redirect(url_for('sCarrito'))
            
@makeupvelApp.route('/iProducto', methods=['GET', 'POST'])
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
    makeupvelApp.run(port=5025)


