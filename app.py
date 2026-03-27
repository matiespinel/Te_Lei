from flask import Flask, request, jsonify
from base import libro, libors
from flask import render_template

app = Flask(__name__)
@app.route("/")
def index():
    libros_lista = []
    for x in libors.find():
        x.pop("_id")
        libros_lista.append(x)
    return render_template("index.html", libros=libros_lista)
def agregar(titulo, autor, leido, pagina):
    nuevo_libro = libro(titulo, autor, leido, pagina)
    if (nuevo_libro.save()): 
        return jsonify({"message": "Libro agregado exitosamente."}), 201
    else:
        return jsonify({"message": "Error al agregar el libro."}), 400


def buscar_y_actualizar(titulo, leido, pagina):
    libro_encontrado = libro.find_by_title(titulo)
    #check casos borde
    if (pagina is None) and leido == "a medias":
        return jsonify({"message": "Error: La página o capítulo no puede ser nulo para un libro en estado 'a medias'."}), 400
    else:
        
        if libro_encontrado:
            libors.update_one({'titulo': titulo}, {'$set': {'pagina_capitulo': pagina, 'leido': leido}})
            return jsonify({"message": "Libro actualizado exitosamente."}), 200
        else:
            return jsonify({"message": "Libro no encontrado."}), 404


@app.route("/accion", methods=["POST"])
def accion(): #en base a lo que llegue del html, se puede realizar una acción específica con el libro encontrado, como marcarlo como leído, actualizar su estado, etc.
    #primero me fije que accione me llego del html, y luego realizo la acción correspondiente con el libro encontrado
    #ya sea  Consultar, Modificar o Agregar
    accion = request.form.get("accion")
    titulo = request.form.get("titulo")
    autor = request.form.get("autor")
    leido = request.form.get("leido")
    pagina = request.form.get("pagina")
    #verificamos accion:
    if accion not in ["consultar", "modificar", "agregar"]:
        return jsonify({"message": "Acción no válida."}), 400
    if accion == "agregar":
        agregar(titulo, autor, leido, pagina)
    elif accion == "consultar":
        libro_encontrado = libro.find_by_title(titulo)
        if libro_encontrado:
            libro_encontrado.pop("_id")
            return jsonify(libro_encontrado), 200
        else:
            return jsonify({"message": "Libro no encontrado."}), 404
    elif accion == "modificar":
        buscar_y_actualizar(titulo, leido, pagina)
    return jsonify({"message": f"Acción '{accion}' realizada exitosamente."}), 200



if __name__ == "__main__":
    app.run(debug=True)

