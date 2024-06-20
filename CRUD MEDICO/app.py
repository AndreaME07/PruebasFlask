from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bd_clinicmayo'
app.secret_key = 'mysecretkey'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route('/consultarMedico')
def consultarMedico():
    try:
        cursor= mysql.connection.cursor();
        cursor.execute('select * from tb_medico')
        consultaM= cursor.fetchall()
        return render_template('consultarMedico.html', medicos=consultaM)
        #redireccion y resultado de la consulta
    except Exception as e:
        print('e')
    

@app.route('/guardarMedico', methods=['POST'])
def guardarMedico():
    if request.method == 'POST':
        Fnombre = request.form['txtNombre']
        Fapellido_p = request.form['txtApellido_p']
        Fapellido_m = request.form['txtApellido_m']
        Frfc = request.form['txtRFC']
        Fcedula = request.form['txtCedula']
        Fcorreo = request.form['txtCorreo']
        Fcontrasena = request.form['txtContrasena']
        
        # Enviamos a la BD
        cursor = mysql.connection.cursor()
        # Mandamos un insert del formulario hacia nuestra base de datos
        cursor.execute('INSERT INTO tb_medico (nombre, apellido_p, apellido_m, rfc, cedula, correo, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                    (Fnombre, Fapellido_p, Fapellido_m, Frfc, Fcedula, Fcorreo, Fcontrasena))
        # Mandamos el commit
        mysql.connection.commit()
        
        flash('Médico registrado correctamente')
        # Hacemos que una vez guardado el dato que redireccione al index
        return redirect(url_for('consultarMedico'))

# Manejo de excepciones para rutas 
@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis: No encontré nada', 404

# Ejecutar el proyecto
if __name__ == '__main__':
    app.run(port=3000, debug=True) 
    # Debug nos ayuda principalmente a refrescar en caso de que haya algún cambio
