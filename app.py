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
    nuevo_libro = libro(data['titulo'], data['autor_fuente'], data['leido'])
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
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

