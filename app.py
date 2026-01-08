from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta'

db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

usuarios = []

@app.route("/")
def inicio():
   return render_template("index.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        usuarios.append({
            "nombre": nombre,
            "correo": correo,
            "contraseña": contraseña
        })

        return redirect(url_for("menu"))

    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        for u in usuarios:
            if u["correo"] == correo and u["contraseña"] == contraseña:
                return redirect(url_for("menu"))

      
        return render_template("login.html", error="Datos incorrectos")

    return render_template("login.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/pantalla1")
def pantalla1():
    return render_template("pantalla1.html")

@app.route("/pantalla2")
def pantalla2():
    return render_template("pantalla2.html")

@app.route("/pantalla3")
def pantalla3():
    return render_template("pantalla3.html")

@app.route("/pantalla4")
def pantalla4():
    return render_template("pantalla4.html")

@app.route("/pantalla5")
def pantalla5():
    return render_template("pantalla5.html")

@app.route("/clasificar", methods=["GET", "POST"])
def clasificar():
    instruccion = ""

    if request.method == "POST":
        residuo = request.form["residuo"]

        if residuo == "plastico":
            instruccion = "Lava el envase, aplástalo y colócalo en el contenedor amarillo."
        elif residuo == "papel":
            instruccion = "Asegúrate de que esté limpio y seco y colócalo en el contenedor azul."
        elif residuo == "vidrio":
            instruccion = "Deposítalo sin tapas en el contenedor verde."
        elif residuo == "metal":
            instruccion = "Limpia la lata y colócala en el contenedor amarillo."
        elif residuo == "organico":
            instruccion = "Colócalo en el contenedor café para compostaje."
        else:
            instruccion = "Este residuo no es reciclable. Depósitalo en basura general."

    return render_template("clasificar.html", instruccion=instruccion)
@app.route("/lecciones")
def lecciones():
    mini_lecciones = [
        {
            "titulo": "¿Por qué reciclar?",
            "contenido": "Reciclar reduce la cantidad de basura que llega a rellenos sanitarios, ahorra recursos naturales y disminuye la contaminación del aire, agua y suelo."
        },
        {
            "titulo": "Impacto del plástico",
            "contenido": "El plástico puede tardar cientos de años en degradarse. Si no se recicla, termina en océanos afectando a animales y ecosistemas."
        },
        {
            "titulo": "Separar correctamente",
            "contenido": "Cuando separas bien los residuos, evitas que los materiales reciclables se contaminen y se desperdicien."
        },
        {
            "titulo": "Tus acciones cuentan",
            "contenido": "Pequeñas acciones como reciclar una botella o usar menos plástico ayudan a reducir el impacto ambiental y proteger el planeta."
        }
    ]

    return render_template("lecciones.html", lecciones=mini_lecciones)

puntos_usuario = 0
indice_reto = 0

@app.route("/retos", methods=["GET", "POST"])
def retos():
    global puntos_usuario, indice_reto

    retos_lista = [
        "Separé correctamente mis residuos hoy",
        "Usé una botella reutilizable",
        "Evité usar bolsas de plástico",
        "Apagué luces que no estaba usando",
        "Reutilicé un envase en lugar de tirarlo"
    ]

    mensaje = ""

    if request.method == "POST":
        accion = request.form["accion"]

        if accion == "si":
            puntos_usuario += 15
            mensaje = "🎉 ¡Muy bien! Ganaste 15 puntos."
        elif accion == "no":
            mensaje = "💡 ¡Inténtalo en el siguiente reto!"
        elif accion == "siguiente":
            indice_reto += 1
            if indice_reto >= len(retos_lista):
                indice_reto = 0  

    reto_actual = retos_lista[indice_reto]

    return render_template(
        "retos.html",
        reto=reto_actual,
        mensaje=mensaje,
        puntos=puntos_usuario
    )
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    puntaje = 0
    resultado = False

    if request.method == "POST":
        resultado = True

        if request.form.get("p1") == "plastico":
            puntaje += 1
        if request.form.get("p2") == "azul":
            puntaje += 1
        if request.form.get("p3") == "no":
            puntaje += 1

    return render_template("quiz.html", puntaje=puntaje, resultado=resultado)


@app.route("/nivel_reciclaje")
def nivel_reciclaje():
    return render_template("nivel_reciclaje.html")






if __name__ == "__main__":
    app.run(debug=True)

