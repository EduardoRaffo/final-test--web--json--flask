from dotenv import load_dotenv
from json_users_data import Load_users,Save_users,Delete_user,User_by_ID,FILENAME
from types import SimpleNamespace
import validations as v
import json
import os
from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request, redirect, url_for
from pyngrok import ngrok, conf
"""Estuve leyendo, que es una buena practica no poner directamente le TOKEN en el fichero principal. Lo guarde en .env para acceder a él de manera segura."""
load_dotenv()  # carga las variables del archivo .env en el entorno
TOKEN = os.getenv("NGROK_TOKEN")
if not TOKEN:
    raise Exception("No se ha cargado NGROK_TOKEN")
ngrok.set_auth_token(TOKEN) 

# Iniciar app Flask
app = Flask(__name__)
public_url = ngrok.connect(5000)
run_with_ngrok(app)

@app.route("/", methods=["GET", "POST"]) #Se inicializa la pagina principal, con el metodo GET para obtener los datos que se ingrresan al formulario, y POST para enviarlos y procesarlos en el BACK
def formulario():
    mensaje = ""     #Prepara el posible mensaje de error o exito
    data = None     #variable para guardar temporalmente los datos ingresados
    if request.method == "POST": #cuando se completa el formulario y se presiona el boton de guardar
        data = {
            "user_name": request.form.get("nombre", "").strip(),
            "user_surname": request.form.get("apellido", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("contraseña", "").strip(),
            "phone_num": request.form.get("phone_num", "").strip(),
            "user_age": request.form.get("edad", "").strip()
        } #Los datos se guardan en un diccionario
        validator = v.UserValidator(data) # Se intentan validar con la clase que creamos en validations
        if validator.validate(): #si los datos pasan las validaciones correctamente
            users = Load_users()
            users.append(SimpleNamespace(**data))
            Save_users(users)
            mensaje = "Usuario registrado correctamente!"
            data = None  # limpiar formulario tras éxito
        else:
            mensaje = "Errores:" + ",".join(validator.errors) #si algo no pasa las validaciones, se muestra por pantalla

    return render_template("form.html", mensaje=mensaje, valores=data) #usa el fichero form para mostrar el html y sus estilos

@app.route('/usuarios') #Define que la url /usuarios se va a mostrar lo siguiente
def Show_users():
    with open(FILENAME, 'r', encoding='utf-8') as archivo:
        usuarios = json.load(archivo, object_hook=lambda d: SimpleNamespace(**d))
    return render_template('users.html', usuarios=usuarios) #muestra los usuarios guardados en JSON. en forma de tabla

@app.route("/delete_user/<int:user_id>", methods=["GET"]) #se utiliza para borrar a travez del boton en la tabla de usuarios registrados.               
def delete_user(user_id):
    Delete_user(user_id)
    return redirect(url_for("Show_users")) #vuelve a la tabla con los usuarios restantes.

@app.route('/edit/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    index, usuario = User_by_ID(user_id) # Buscar el usuario por su ID
    if usuario is None:
        return "Usuario no encontrado", 404
    return render_template('update_users.html', usuario=usuario, user_id=user_id) #Muestra el formulario con los datos del usuario seleccionado, para modificar 

@app.route('/update/<int:user_id>', methods=['POST']) 
def update_user(user_id):
    index, _ = User_by_ID(user_id) #busca el usuario por su indice
    if index is None:
        return "Usuario no encontrado", 404

    data = { #Actualiza los datos, segun el formulario de actualizacion
        "user_name": request.form.get("nombre", "").strip(),
        "user_surname": request.form.get("apellido", "").strip(),
        "email": request.form.get("email", "").strip(),
        "password": request.form.get("contraseña", "").strip(),
        "phone_num": request.form.get("phone_num", "").strip(),
        "user_age": request.form.get("edad", "").strip(),
        "id": user_id  # conservar el ID original
    }

    validator = v.UserValidator(data) #procesa si los datos son validos
    if validator.validate():
        usuarios = Load_users()
        usuarios[index] = SimpleNamespace(**data)
        Save_users(usuarios)
        return redirect(url_for("Show_users")) #Al terminar de actualizar, vuelve a la tabla con los usuarios actualizados
    else:
        mensaje = "Errores: " + ", ".join(validator.errors) 
        return render_template("update_users.html", usuario=SimpleNamespace(**data), user_id=user_id, mensaje=mensaje)

if __name__ == "__main__":# Ejecuta la app solo si este archivo es el principal.
    print(f" * Running on {public_url.public_url}") # Muestra la URL pública generada por ngrok para facilitar el acceso externo.
    print(f" * Click here: {public_url.public_url}") # Luego arranca el servidor Flask en modo desarrollo.
    app.run()