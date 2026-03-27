from flask import Flask, request, jsonify
from base import libro, libors
from flask import render_template

app = Flask(__name__)
@app.route("/")
def index():
    aux= []
    for x in libors.find():
        x.pop("_id")
        aux.append(x)
    return jsonify(aux)
@app.route("/agregar", methods=["POST"])
def agregar():
    data = request.get_json()
    nuevo_libro = libro(data['titulo'], data['autor_fuente'], data['leido'], data['pagina_capitulo'])
    if (nuevo_libro.save()): 
        return jsonify({"message": "Libro agregado exitosamente."}), 201
    else:
        return jsonify({"message": "Error al agregar el libro."}), 400

@app.route("/buscar_y_actualizar", methods=["PUT"])
def buscar_y_actualizar():
    data = request.get_json()
    libro_encontrado = libro.find_by_title(data['titulo'])
    #check casos borde
    if (data.get("pagina_capitulo") is None) and data["leido"] == "a medias":
        return jsonify({"message": "Error: La página o capítulo no puede ser nulo para un libro en estado 'a medias'."}), 400
    else:
        
        if libro_encontrado:
            libors.update_one({'titulo': data['titulo']}, {'$set': {'pagina_capitulo': data['pagina_capitulo'], 'leido': data['leido']}})
            return jsonify({"message": "Libro actualizado exitosamente."}), 200
        else:
            return jsonify({"message": "Libro no encontrado."}), 404

@app.route("/accion", methods=["POST"])
def accion(): #en base a lo que llegue del html, se puede realizar una acción específica con el libro encontrado, como marcarlo como leído, actualizar su estado, etc.
    #primero me fije que accione me llego del html, y luego realizo la acción correspondiente con el libro encontrado
    #ya sea  Consultar, Modificar o Agregar
    data = request.get_json()
    #verificamos accion:
    accion = data.get("accion")
    if accion not in ["consultar", "modificar", "agregar"]:
        return jsonify({"message": "Acción no válida."}), 400
    if accion == "agregar":
        agregar()
    elif accion == "consultar":
        #buscar_y_actualizar()
        pass
    elif accion == "modificar":
        buscar_y_actualizar()
    return jsonify({"message": f"Acción '{accion}' realizada exitosamente."}),

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

