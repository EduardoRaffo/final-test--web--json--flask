#!pip install pyngrok flask-ngrok
from dotenv import load_dotenv
from json_users_data import Load_users,Save_users,FILENAME
from types import SimpleNamespace
import validations as v
import sqlite3
import json
import os
from flask_ngrok import run_with_ngrok
from flask import Flask, request, render_template
from pyngrok import ngrok, conf

load_dotenv()  # carga las variables del archivo .env en el entorno
TOKEN = os.getenv("NGROK_TOKEN")
if not TOKEN:
    raise Exception("No se ha cargado NGROK_TOKEN")
ngrok.set_auth_token(TOKEN)

# Iniciar app
app = Flask(__name__)
public_url = ngrok.connect(5000)
run_with_ngrok(app)

@app.route("/", methods=["GET", "POST"])
def formulario():
    mensaje =""
    if request.method == "POST":
        data = {
            "user_name": request.form.get("nombre", "").strip(),
            "user_surname": request.form.get("apellido", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("contraseña", "").strip(),
            "phone_num": request.form.get("phone_num", "").strip(),
            "user_age": request.form.get("edad", "").strip()
        }
        validator = v.UserValidator(data)
        if validator.validate():
            users = Load_users()
            users.append(SimpleNamespace(**data))    
            Save_users(users)      
            mensaje = "Usuario registrado correctamente!"
        else:
            mensaje = "Errores: " + ", ".join(validator.errors)
    
    return render_template("formulario.html", mensaje=mensaje)

if __name__ == "__main__":
    print(f" * Running on {public_url.public_url}")
    print(f" * Click here: {public_url.public_url}")
    app.run()