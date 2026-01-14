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

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puntaje = db.Column(db.Integer)

class Puntos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puntos = db.Column(db.Integer)

with app.app_context():
    db.create_all()


@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            contraseña=contraseña
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("menu"))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contraseña = request.form["contraseña"]

        usuario = Usuario.query.filter_by(
            correo=correo,
            contraseña=contraseña
        ).first()

        if usuario:
            return redirect(url_for("menu"))
        else:
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
            instruccion = "Este residuo no es reciclable."

    return render_template("clasificar.html", instruccion=instruccion)
                           
@app.route("/lecciones")
def lecciones():
    mini_lecciones = [
        {
            "titulo": "¿Por qué reciclar?",
            "contenido": "Reciclar reduce la basura y la contaminación."
        },
        {
            "titulo": "Impacto del plástico",
            "contenido": "El plástico tarda cientos de años en degradarse."
        },
        {
            "titulo": "Separar correctamente",
            "contenido": "Separar evita que los reciclables se desperdicien."
        },
        {
            "titulo": "Tus acciones cuentan",
            "contenido": "Pequeñas acciones generan grandes cambios."
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
        "Reutilicé un envase"
    ]

    mensaje = ""

    if request.method == "POST":
        accion = request.form["accion"]

        if accion == "si":
            puntos_usuario += 15
            mensaje = "🎉 ¡Muy bien! Ganaste 15 puntos."
            db.session.add(Puntos(puntos=puntos_usuario))
            db.session.commit()

        elif accion == "no":
            mensaje = "💡 ¡Inténtalo en el siguiente reto!"
        elif accion == "siguiente":
            indice_reto = (indice_reto + 1) % len(retos_lista)

    return render_template(
        "retos.html",
        reto=retos_lista[indice_reto],
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

        db.session.add(Quiz(puntaje=puntaje))
        db.session.commit()

    return render_template("quiz.html", puntaje=puntaje, resultado=resultado)

@app.route("/nivel_reciclaje")
def nivel_reciclaje():
    return render_template("nivel_reciclaje.html")


if __name__ == "__main__":
    app.run(debug=True)

