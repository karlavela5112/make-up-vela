from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from config import config
from models.entities.User import User
from models.ModelUser import ModelUser
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()
makeupvelaApp=Flask(__name__)

makeupvelaApp.config.from_object(config['development'])
makeupvelaApp.config.from_object(config['mail'])

db = MySQL(makeupvelaApp)
adminUsuario = LoginManager(makeupvelaApp)
mail = Mail(makeupvelaApp)

@adminUsuario.user_loader
def cargarUsuario(id):
    return ModelUser.get_by_id(db, id)

@makeupvelaApp.route('/', methods=['GET'])
def home():
    busqueda = request.args.get('busqueda', '')
    categoria_id = request.args.get('categoria', '')

    query = "SELECT * FROM productos WHERE 1=1"
    parametros = []

    if busqueda:
        query += " AND nombre LIKE %s"
        parametros.append(f"%{busqueda}%")

    if categoria_id:
        query += " AND categoria_id = %s"
        parametros.append(categoria_id)

    selProducto = db.connection.cursor()
    selProducto.execute(query, tuple(parametros))
    productos = selProducto.fetchall()
    selProducto.close()

    selCategorias = db.connection.cursor()
    selCategorias.execute("SELECT * FROM categorias")
    categorias = selCategorias.fetchall()
    selCategorias.close()

    carrito = session.get('carrito', {})
    total_carrito = sum(item['precio'] * item['cantidad'] for item in carrito.values()) if carrito else 0

    return render_template('home.html', 
                           productos=productos, 
                           categorias=categorias, 
                           carrito=carrito, 
                           total_carrito=total_carrito,
                           busqueda_actual=busqueda,
                           categoria_actual=categoria_id)

@makeupvelaApp.route('/producto/<int:id>')
def detalle_producto(id):
    cur = db.connection.cursor()
    cur.execute("""
        SELECT p.id, p.nombre, p.descripción, p.precio, p.nombre_img, c.nombre 
        FROM productos p 
        INNER JOIN categorias c ON p.categoria_id = c.id 
        WHERE p.id = %s
    """, (id,))
    producto_seleccionado = cur.fetchone()
    cur.close()

    if not producto_seleccionado:
        flash('Lo sentimos, no pudimos encontrar ese producto.')
        return redirect(url_for('home'))

    cur = db.connection.cursor()
    cur.execute("SELECT * FROM categorias")
    lista_categorias = cur.fetchall()
    cur.close()

    return render_template('producto.html', 
                           producto=producto_seleccionado, 
                           categorias=lista_categorias)

@makeupvelaApp.context_processor
def inject_cart_count():
    carrito = session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())
    return dict(cart_count=total_items)

@makeupvelaApp.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    items = list(carrito.values())
    total = sum(item['precio'] * item['cantidad'] for item in items)
    return render_template('carrito.html', items=items, total=total)

@makeupvelaApp.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito():
    producto_id = str(request.form['producto_id']) 
    
    cur = db.connection.cursor()
    cur.execute("SELECT id, nombre, precio, nombre_img FROM productos WHERE id = %s", (producto_id,))
    producto = cur.fetchone()
    cur.close()

    if producto:
        if 'carrito' not in session:
            session['carrito'] = {}
            
        carrito = session['carrito']
        
        if producto_id in carrito:
            carrito[producto_id]['cantidad'] += 1
        else:
            carrito[producto_id] = {
                'id': producto[0],
                'nombre': producto[1],
                'precio': float(producto[2]),
                'imagen': producto[3],
                'cantidad': 1
            }
            
        session['carrito'] = carrito
        session.modified = True 
        flash(f'¡{producto[1]} agregado a tu canasta!')
        
    return redirect(request.referrer or url_for('home'))

@makeupvelaApp.route('/modificar_carrito', methods=['POST'])
def modificar_carrito():
    producto_id = str(request.form['producto_id'])
    accion = request.form['accion']
    
    if 'carrito' in session:
        carrito = session['carrito']
        if producto_id in carrito:
            if accion == 'sumar':
                carrito[producto_id]['cantidad'] += 1
            elif accion == 'restar':
                carrito[producto_id]['cantidad'] -= 1
                if carrito[producto_id]['cantidad'] <= 0:
                    del carrito[producto_id]
            elif accion == 'eliminar':
                del carrito[producto_id]
                
            session['carrito'] = carrito
            session.modified = True
            
    return redirect(url_for('ver_carrito'))

@makeupvelaApp.route('/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    session.pop('carrito', None)
    session.modified = True
    flash('Tu canasta ha sido vaciada.')
    return redirect(url_for('home'))

@makeupvelaApp.route('/checkout', methods=['POST'])
def checkout():
    session.pop('carrito', None) 
    flash('¡Gracias por tu compra! Tu pedido está siendo procesado.')
    return redirect(url_for('home'))

@makeupvelaApp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo'] 
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave, method='pbkdf2:sha256')
        msg = Message(subject='Bienvenido a Makeup Vela', recipients=[correo])
        msg.html = render_template('mail.html', usuario=nombre)
        mail.send(msg)
        regUsuario = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave) VALUES (%s, %s, %s)", (nombre.upper(), correo, claveCifrada))
        flash('Usuario registrado') 
        db.connection.commit()
        regUsuario.close()
        return redirect(url_for('home'))
    else: 
        return render_template('signup.html')

@makeupvelaApp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0,None,request.form['correo'],request.form['clave'],None)
        usuarioAutenticado = ModelUser.signin(db, usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado)
                if usuarioAutenticado.perfil == 'A':
                    return redirect(url_for('home_admin'))
                else:
                    return redirect(url_for('home')) 
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
    return redirect(url_for('home'))

@makeupvelaApp.route('/sUsuario',methods = ['GET','POST'])
@login_required
def sUsuario():
    if current_user.perfil != 'A': 
        flash('Acceso denegado.')
        return redirect(url_for('home'))
    selUsuario = db.connection.cursor()
    selUsuario.execute("SELECT * FROM usuario")
    u = selUsuario.fetchall()
    selUsuario.close()
    return render_template('users.html', usuarios=u)

@makeupvelaApp.route('/iUsuario', methods=["GET", "POST"])
@login_required
def iUsuario():
    if current_user.perfil != 'A':
        flash('Acceso denegado.')
        return redirect(url_for('home'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo'] 
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave, method='pbkdf2:sha256')
        perfil = request.form['perfil']
        
        regUsuario = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave, perfil) VALUES (%s, %s, %s, %s)", (nombre.upper(), correo, claveCifrada, perfil))
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
        actUsuario.execute("UPDATE usuario SET nombre=%s, correo=%s, clave=%s, perfil=%s WHERE id=%s", (nombre.upper(), correo, clave, perfil, id))
        db.connection.commit()
        actUsuario.close()
        return redirect(url_for('sUsuario'))
    else:
       return redirect(url_for('sUsuario'))

@makeupvelaApp.route('/dUsuario/<int:id>', methods=['GET', 'POST'])
@login_required
def dUsuario(id):
    if current_user.perfil != 'A': 
        flash('Acceso denegado.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        delUsuario = db.connection.cursor()
        delUsuario.execute("DELETE FROM usuario WHERE id=%s", (id,))
        db.connection.commit()
        delUsuario.close()
        flash('Usuario eliminado')
        return redirect(url_for('sUsuario'))
    else:
        return render_template('users.html')

@makeupvelaApp.route('/sProducto', methods=['GET', 'POST'])
@login_required
def sProducto():
    if current_user.perfil != 'A': 
        flash('Acceso denegado.')
        return redirect(url_for('home'))
    selProducto = db.connection.cursor()
    try:
        selProducto.execute("SELECT * FROM productos")
        p = selProducto.fetchall()
    finally:
        selProducto.close() 
    return render_template('productos.html', productos=p)

@makeupvelaApp.route('/uProductos/<int:id>' ,methods=['GET','POST'])
@login_required
def uProductos(id):
    if current_user.perfil != 'A': 
        flash('Acceso denegado.')
        return redirect(url_for('home'))
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
            "UPDATE productos SET nombre=%s, descripción=%s, categoria_id=%s, precio=%s, stock=%s, nombre_img=%s WHERE id=%s",
            (nombre, descripcion, categoria, precio, stock, nombre_img, id)
        )
        db.connection.commit()
        actProducto.close()
        flash("Producto actualizado exitosamente")
        return redirect(url_for('sProducto')) 
    else:
        flash("Error al actualizar el producto")
        return redirect(url_for('sProducto'))
    
@makeupvelaApp.route('/dProducto/<int:id>', methods=['POST'])
@login_required
def dProducto(id):
    if current_user.perfil != 'A': 
        flash('Acceso denegado.')
        return redirect(url_for('home'))
    try:
        delProducto = db.connection.cursor()
        delProducto.execute("DELETE FROM productos WHERE id=%s", (id,))
        db.connection.commit()
        delProducto.close()
        flash('Producto eliminado exitosamente del catálogo.')
    except Exception as e:
        flash('Error al eliminar: El producto está vinculado a un carrito o pedido activo.')
        
    return redirect(url_for('sProducto'))

@makeupvelaApp.route('/home_admin', methods=['GET','POST'])
@login_required
def home_admin():
    if current_user.perfil != 'A':
        flash('No tienes permisos para ver esta página.')
        return redirect(url_for('home'))
        
    return render_template('admin.html')
            
@makeupvelaApp.route('/iProducto', methods=['GET', 'POST'])
@login_required
def iProducto():
    if current_user.perfil != 'A':
        flash('Acceso denegado.')
        return redirect(url_for('home'))
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
        NuevoProducto.execute("INSERT INTO productos (nombre, descripción, categoria_id, precio, stock, nombre_img) VALUES (%s, %s, %s, %s, %s, %s)", (nombre.upper(), descripcion, categoria, precio, stock, nombre_img))
        db.connection.commit()
        flash('Producto Agregado')
        NuevoProducto.close()
        return redirect(url_for('sProducto'))
    else:
        return render_template('productos.html')

if __name__ == '__main__':
    makeupvelaApp.run(port=5025)