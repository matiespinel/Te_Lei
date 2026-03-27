from base import libro, libors
import pandas as pd

cursor = libors.find()
df = pd.DataFrame(list(cursor))

df
print(df.groupby("leido").count())

def libros_por_estado(df):
    leidos = df.groupby("leido").count()
    no_leidos = df['leido'][df['leido'] == 'no leido'].count()
    a_medias = df['leido'][df['leido'] == 'a medias'].count()
    #pie chart data
    labels = ['Leídos', 'No Leídos', 'A Medias']
    values = [leidos, no_leidos, a_medias]