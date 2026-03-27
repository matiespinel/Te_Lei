
# import os
# from dotenv import load_dotenv
from pymongo import MongoClient

# load_dotenv()

# MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
# MongoDB Atlas (comentado - descomentar y configurar .env para usar)
# MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://usuario:password@cluster.mongodb.net/')

# Conexión local
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
libors = db['libors']
from enum import Enum


class estado(Enum):
    LEIDO = "leido"
    NO_LEIDO = "no leido"
    A_MEDIAS = "a medias"

class genero(Enum):
    FICCION = "ficcion"
    CIENCIA_FICCION = "ciencia ficcion"
    FANTASIA = "fantasia"
    HISTORICO = "historico"
    AVENTURA = "aventura"
    ARTES_MARCIALES = "artes marciales"
    MISTERIO = "misterio"
    ROMANCE = "romance"
class libro:
    def __init__(self, title, author, leido, pagina_capitulo, generos):
        self.titulo : str = title
        self.autor_fuente : str = author
        self.leido : bool = leido
        self.pagina_capitulo : int = pagina_capitulo
        self.generos : list = generos

    def save(self):
        if (libors.find_one({'titulo': self.titulo})):
            print("El libro ya existe en la base de datos.")
            return False
        libors.insert_one({
            'titulo': self.titulo,
            'autor_fuente': self.autor_fuente,
            'leido': self.leido,   #enum
            'pagina_capitulo': self.pagina_capitulo,
            'generos': self.generos
        })
        return True

    @staticmethod
    def find_by_title(title):
        return libors.find_one({'titulo': title})
        

