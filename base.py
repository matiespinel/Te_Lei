from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
libors = db['libors']

class libro:
    def __init__(self, title, author, leido):
        self.titulo : str = title
        self.autor_fuente : str = author
        self.leido : bool = leido

    def save(self):
        libors.insert_one({
            'titulo': self.titulo,
            'autor_fuente': self.autor_fuente,
            'leido': self.leido
        })

    @staticmethod
    def find_by_title(title):
        return libors.find_one({'title': title})