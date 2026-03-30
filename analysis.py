from base import libro, libors
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO

cursor = libors.find()
df = pd.DataFrame(list(cursor))
df
generos = df.explode("generos").groupby("generos").size().sort_values(ascending=False)
#generos tiene una serie de pandas con el conteo de libros por genero. 
#piechart 
fig = plt.figure()
plt.pie(generos, labels=generos.index, autopct='%1.1f%%')
plt.title("Distribución de géneros en biblioteca")
fig = plt.savefig("static/generos_piechart.png")
tmpfile = BytesIO()
fig.savefig(tmpfile, format='png')
encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
