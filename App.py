# app.py
from flask import Flask, request, session, redirect, url_for, render_template
from flaskext.mysql import MySQL
from tkinter import ttk
from tkinter import*
import pymysql
import re

app = Flask(__name__)


app.secret_key = 'mysecretkey'

mysql = MySQL()

# configuracion para la conexion a msql
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'registro'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




@app.route('/')
def home():
    return render_template('Pagina_principal.html')



# http://localhost:5000/pythonlogin/ - esta es la pagina para iniciar sesion


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():

 # conexion a msql
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # esto es el login
    msg = ''

    if request.method == 'POST' and 'Email' in request.form and 'Contraseña' in request.form:

        Email = request.form['Email']
        Contraseña = request.form['Contraseña']

        cursor.execute(
            'SELECT * FROM datos2 WHERE Email = %s AND Contraseña = %s', (Email, Contraseña))

        datos2 = cursor.fetchone()

    # If si la cuenta exisite, te manda a home, que es la pagina que veria el usuario al ingresar, en la misma estan los datos de su cuenta
        if datos2:

            session['loggedin'] = True
            session['id'] = datos2['id']
            session['Email'] = datos2['Email']

            return redirect(url_for('home'))
        else:
            # esto es un mensaje por si la cagas y escribiste mal
            msg = 'Incorrect username/password!'

    if request.method == 'POST' and 'Email' in request.form and 'Contraseña' in request.form:

        Email = request.form['Email']
        Contraseña = request.form['Contraseña']

        cursor.execute(
            'SELECT * FROM datos WHERE Email = %s AND Contraseña = %s', (Email, Contraseña))

        datos = cursor.fetchone()

    # If si la cuenta exisite, te manda a home, que es la pagina que veria el usuario al ingresar, en la misma estan los datos de su cuenta
        if datos:

            session['loggedin'] = True
            session['id'] = datos['id']
            session['Email'] = datos['Email']

            return redirect(url_for('home'))
        else:
            # esto es un mensaje por si la cagas y escribiste mal
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)

# http://localhost:5000/register - Esto es el registro a la pagina


@app.route('/register', methods=['GET', 'POST'])
def register():
 # Conexion a mysql
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # esto es la conexion a mysql para el registro
    msg = ''

    if request.method == 'POST' and 'Nombre' in request.form and 'Contraseña' in request.form and 'Email' in request.form:

        Nombre = request.form['Nombre']
        Email = request.form['Email']
        Contraseña = request.form['Contraseña']
        ConfirmarContraseña = request.form['ConfirmarContraseña']

        cursor.execute('SELECT * FROM datos WHERE Nombre = %s', (Nombre))
        account = cursor.fetchone()
        # esto es por si la cuenta que queres registrar ya existe
        if account:
            msg = 'La cuenta ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Email incorrecto!'
        elif not re.match(r'[A-Za-z0-9]+', Nombre):
            msg = 'El nombre solo debe contener caracteres y numeros!'
        elif not Nombre or not Contraseña or not Email:
            msg = 'Por favor llene el formulario!'

        else:
            # ahora si la cuenta no existe te deja registrar por este codigo
            cursor.execute('INSERT INTO datos VALUES (NULL, %s, %s, %s, %s)',
                           (Nombre, Email, Contraseña, ConfirmarContraseña))
            conn.commit()

            msg = 'Has sido registrado con exito, ahora solo debes iniciar sesion!'
            return render_template('index.html')
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


################################################################################

@app.route('/register2', methods=['GET', 'POST'])
def register2():
 # Conexion a mysql
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # esto es la conexion a mysql para el registro

    if request.method == 'POST' and 'Nombredellocal' in request.form and 'Direccion' in request.form and 'Correo' in request.form and 'Contraseña' in request.form:

        Nombredellocal = request.form['Nombredellocal']
        Direccion = request.form['Direccion']
        Correo = request.form['Correo']
        Contraseña = request.form['Contraseña']

        cursor.execute(
            'SELECT * FROM datos2 WHERE Nombredellocal = %s', (Nombredellocal))
        account = cursor.fetchone()
        # esto es por si la cuenta que queres registrar ya existe
        if account:
            msg = 'La cuenta ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Correo):
            msg = 'Email incorrecto!'
        elif not re.match(r'[A-Za-z0-9]+', Nombredellocal):
            msg = 'El nombre solo debe contener caracteres y numeros!'
        elif not Nombredellocal or not Contraseña or not Correo:
            msg = 'Por favor llene el formulario!'

        else:
            # ahora si la cuenta no existe te deja registrar por este codigo
            cursor.execute('INSERT INTO datos2 VALUES (NULL, %s, %s, %s, %s)',
                           (Nombredellocal, Direccion, Correo, Contraseña))
            conn.commit()

            msg = 'Has sido registrado con exito, ahora solo debes iniciar sesion!'
            return render_template('index.html')
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


# http://localhost:5000/home - Esta es la pagina a la que accede el usuario al ingresar


@app.route('/')
def home2():

    if 'loggedin' in session:

        return render_template('home.html', Email=session['Email'])

    return redirect(url_for('login'))

# http://localhost:5000/logout - esta es la pagina para salir de la sesion


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('Nombre', None)
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - aca van a estar todas las caracteristicas de la cuenta


@app.route('/profile')
def profile():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM datos2 WHERE id = %s', [session['id']])
        datos2 = cursor.fetchone()

        return render_template('profile.html', datos2=datos2)
    # esto es por is el usuario nopuede ingresar, lo redirecciona
    return redirect(url_for('login'))

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM datos WHERE id = %s', [session['id']])
        datos2 = cursor.fetchone()

        return render_template('profile.html', datos=datos)
    # esto es por is el usuario nopuede ingresar, lo redirecciona
    return redirect(url_for('login'))


@app.route('/inventario')
def inventario():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('SELECT * FROM productos WHERE id = %s', [session['id']])
        productos = cursor.fetchone()

        return render_template('inventario.html', productos=productos)



  


if __name__ == '__main__':
    app.run(debug=True)

