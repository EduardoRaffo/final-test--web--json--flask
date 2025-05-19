import re
def Check_email(email):
    if len(email) <= 320: #320 caracteres es la longitud estandar maxima para un correo electronico
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" #aqui valida que puedes tener puntos. letras mayusculas y minusculas. el arroba obligatorio. luego en el dominio tiene que tener un punto y dos caracteres como minimo al final.
        return re.match(patron, email) is not None
    else:
        return False
    
def Check_name(user_name):
        return (re.match(r'^[A-Za-zÀ-ÿ\s\-]+$', user_name) is not None 
            and len(user_name.strip()) > 1)

def Check_surname(user_surname):
    return user_surname.replace(" ", "").isalpha() and len(user_surname) > 1

def Check_password(password):
    return len(password) >= 6

def Check_phone(phone_num):
    return phone_num.isdigit() and len(phone_num) in [9, 10]

def Check_age(user_age):
    try:
        user_age = int(user_age)
        return 10 <= user_age <= 120
    except ValueError:
        return False

class UserValidator:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def validate(self):
        validators = {
            "email": (Check_email, "Email invalido."),
            "user_name": (Check_name, "Nombre invalido."),
            "user_surname": (Check_surname, "Apeliido invalido."),
            "password": (Check_password, "Contraseña demasiado corta, minimo 6 caracteres"),
            "phone_num": (Check_phone, "Número de telefono invalido"),
            "user_age": (Check_age, "Edad no valida."),
        }
        for field, (func, msg) in validators.items():
            value = self.data.get(field, "").strip()
            if not func(value):
                self.errors.append(f"{field}: {msg}")
        return len(self.errors) == 0