from flask import Flask, request, redirect, url_for, flash
from base import libro, libors
from flask import render_template
from analysis import encoded


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'clave-secreta-para-flash-messages'

@app.route("/")
def index():
    libros_lista = []
    for x in libors.find():
        x.pop("_id")
        libros_lista.append(x)
    return render_template("index.html", libros=libros_lista)

def agregar(titulo, autor, leido, pagina, generos):
    nuevo_libro = libro(titulo, autor, leido, pagina, generos)
    if (nuevo_libro.save()):
        return True, "Libro agregado exitosamente."
    else:
        return False, "El libro ya existe."

def buscar_y_actualizar(titulo, leido, pagina):
    libro_encontrado = libro.find_by_title(titulo)
    if (pagina is None) and leido == "a medias":
        return False, "La página no puede ser nula para un libro 'a medias'."
    else:
        if libro_encontrado:
            libors.update_one({'titulo': titulo}, {'$set': {'pagina_capitulo': pagina, 'leido': leido}})
            return True, "Libro actualizado exitosamente."
        else:
            return False, "Libro no encontrado."

@app.route("/accion", methods=["POST"])
def accion():
    accion = request.form.get("accion")
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    leido = request.form.get("leido")
    pagina = request.form.get("pagina")
    generos = request.form.getlist("generos")

    mensaje = ""
    tipo = "success"
    libro_consultado = None

    if accion not in ["consultar", "modificar", "agregar", "stats"]:
        mensaje = "Acción no válida."
        tipo = "error"
    elif accion == "agregar":
        exito, msg = agregar(titulo, autor, leido, pagina, generos)
        mensaje = msg
        tipo = "success" if exito else "error"
    elif accion == "consultar":
        libro_encontrado = libro.find_by_title(titulo)
        if libro_encontrado:
            libro_encontrado.pop("_id")
            libro_consultado = libro_encontrado
            mensaje = f"Libro encontrado: {titulo}"
            tipo = "success"
        else:
            mensaje = "Libro no encontrado."
            tipo = "error"
    elif accion == "modificar":
        exito, msg = buscar_y_actualizar(titulo, leido, pagina)
        mensaje = msg
        tipo = "success" if exito else "error"
    elif accion == "stats":
        # Lógica para mostrar estadísticas
        pass

    flash(mensaje, tipo)

    # Si se consultó un libro y se encontró, lo pasamos como libro destacado
    if libro_consultado:
        return render_template("index.html", libros=[libro_consultado], mensaje=mensaje, tipo=tipo)

    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)

