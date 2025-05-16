#!pip install pyngrok flask-ngrok
from dotenv import load_dotenv
import validations as v
import sqlite3
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
        user_name = request.form.get("nombre")
        user_adress = request.form.get("apellido")
        email = request.form.get("email")
        password = request.form.get("contraseña")
        phone_num = request.form.get("phone_num")
        user_age = request.form.get("edad")
        if not v.Check_email(email):
            mensaje = "Por favor, ingresa un email, válido."
        else:
            mensaje = "Email correctamente guardado."
    return render_template("formulario.html", mensaje=mensaje)


if __name__ == "__main__":
    print(f" * Running on {public_url.public_url}")
    print(f" * Click here: {public_url.public_url}")
    app.run()