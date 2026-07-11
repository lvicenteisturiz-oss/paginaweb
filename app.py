import requests 
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'winter25'

def obtener_conexion():
    conexion = sqlite3.connect('registro.sqlite')
    return conexion

@app.route('/login', methods=['POST'])
def login():
    usuario_ingresado = request.form.get('usuario')
    clave_ingresada = request.form.get('clave')
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    sql = "SELECT id, usuario FROM usuarios WHERE usuario = ? AND clave = ?"
    cursor.execute(sql, (usuario_ingresado, clave_ingresada))
    usuario_encontrado = cursor.fetchone()
    
    cursor.close()
    conexion.close()
    
    if usuario_encontrado:
        session['usuario'] = usuario_encontrado[1]
    return redirect(url_for('soporte_de_la_pagina'))

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('soporte_de_la_pagina'))

@app.route("/inicio")
def inicio_del_programa():
    return render_template("inicio.html")
@app.route("/")

def soporte_de_la_pagina():

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            clave TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            mascota TEXT NOT NULL,
            edad REAL NOT NULL
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (usuario, clave) VALUES ('admin', '1234')")
        conexion.commit()

    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    
    cursor.close()
    conexion.close()
    
    es_admin = 'usuario' in session
    return render_template('base.html', es_admin=es_admin)
@app.route("/formulario")
def formulario():
    return render_template("formulario.html")
@app.route("/servicios")
def servicio():
    return render_template("servicios.html")
@app.route("/enviar", methods=['GET','POST'])
def envio():
    if 'usuario' not in session:
        return "Acceso denegado.", 403
    if request.method == 'GET':
        return render_template("inicio.html")
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        nombre_mascota = request.form.get('mascota')
        correo = request.form.get('correo')
        edad = request.form.get('edad')
        consulta = base_de_datos()
        cursor = consulta.cursor()
        consultasql = "INSERT INTO animales (nombre, correo, edad, mascota) VALUES (%s, %s, %s, %s)"
        valores = (nombre, correo, edad, nombre_mascota)
        cursor.execute(consultasql, valores)
        consulta.commit()
        cursor.close()
        consulta.close()
        variable = f"nombre: {nombre} nombre_mascota: {nombre_mascota} correo: {correo} edad: {edad}"
        return render_template("solicitud.html", mensaje = variable)
@app.route("/catalogo")
def catalogos():
    gatos = "https://api.thecatapi.com/v1/images/search?limit=10"
    peticion = requests.get(gatos)
    datos_json = peticion.json()
    datos_crudos=[]
    for gato in datos_json:
        item = {
            "nombre": gato["id"],
            "imagen": gato["url"]
        }
        datos_crudos.append(item)
    return render_template("informacion.html", datos = datos_crudos)
def base_de_datos():
    conexion = sqlite3(
        host = "localhost", 
        user = "root",
        password = "",
        database = "paginaweb")
    return conexion 
if __name__ == "__main__": 
    app.run(debug= True, port= 5000)
