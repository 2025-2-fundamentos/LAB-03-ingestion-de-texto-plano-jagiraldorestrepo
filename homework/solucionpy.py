# %% [markdown]
# 
# ## Paso 1: Leer el archivo
# Lines contiene una lista de strings con cada linea del archivo
# 
# ej:
# 
# ['linea1', 'linea 2']

# %%
import pandas as pd

with open('./files/input/clusters_report.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(lines)

# %% [markdown]
# ## Paso 2: quitamos lineas vacias y el renglon de 
# - Creamos lista vacia donde guardaremos las lineas utiles
# - Quitamos el salto de linea del final, pero dejamos espacios en blanco (utiles para reconocer el patron)
# - s.strip() devuelve la linea sin espacios, si está vacia '' es false, por tanto es decir si no true, continue, como si esta vacia continue
# - quitamos los espacio en blanco y metemos esa linea en un set. por si es la linea que tiene todos los guiones.
# 

# %%
clean = [] #1

for ln in lines: 
    s = ln.rstrip('\n') #2
    if not s.strip():#3
        continue
    if set(s.strip()) == {'-'}:#4
        continue
    clean.append(s)

clean

# %% [markdown]
# ## Paso 3: detectar cabeceras con una expresion regular
# 
# identificar cuales lineas de la lista son las cabeceras de cada cluster, tienen esta forma
# 
#    1     105             15,9 %          maximum power point tracking, fuzzy...
# 
# solo debemos reconocer tres numeros, y luego un texto con un patron de regex
# 
# 
# 

# %%
import re

# Patrón para detectar cabeceras de clúster
pat_header = re.compile(r'^\s*(\d+)\s+(\d+)\s+([\d.,]+)\s*%?\s+(.*)$')

header_idx = []   # índices de líneas en 'clean' donde empieza cada clúster
groups_seen = []  # para inspeccionar los grupos capturados

for idx, ln in enumerate(clean):
    m = pat_header.match(ln)
    if m:
        header_idx.append(idx)
        groups_seen.append(m.groups())

print("Índices detectados:", header_idx)
for g in groups_seen:
    print("Grupos:", g)




# %%
bloques = []  # aquí guardamos un dict por cabecera con los pedazos crudos
for k, start in enumerate(header_idx):
    end = header_idx[k+1] if k + 1 < len(header_idx) else len(clean)

    m = pat_header.match(clean[start])
    cluster_num, cantidad, porcentaje_txt, primer_tramo = m.groups()

    # Continuaciones: todas las líneas entre start+1 y end
    tails = [ln.strip() for ln in clean[start+1:end]]  # strip para quitar la mega indentación

    # Unimos: primer tramo + continuaciones en un solo texto
    palabras_raw = " ".join([primer_tramo] + tails)

    # Normalizamos espacios múltiples (por los saltos de línea y alineaciones)
    palabras_norm = re.sub(r"\s+", " ", palabras_raw).strip()

    bloques.append({
        "cluster": cluster_num,
        "cantidad de palabras clave": cantidad,
        "porcentaje de palabras clave": porcentaje_txt,  # todavía como texto (con coma)
        "principales palabras clave": palabras_norm     # texto ya unido y con espacios normalizados
    })

# 3) Inspecciona rápido los dos primeros bloques
for b in bloques[:2]:
    print(f"Cluster {b['cluster']}: cant={b['cantidad de palabras clave']}, %={b['porcentaje de palabras clave']}")
    print(b["principales palabras clave"][:220] + "...\n")


for i in bloques: print(i)

# %% [markdown]
# # Ultimo paso: convertir a dataframe

# %%
import pandas as pd


df = pd.DataFrame(bloques)

# Conversión de tipos
df["cluster"] = df["cluster"].astype(int)
df["cantidad_de_palabras_clave"] = df["cantidad de palabras clave"].astype(int)
df["porcentaje_de_palabras_clave"] = (
    df["porcentaje de palabras clave"].str.replace(",", ".", regex=False).astype(float)
)
df["principales_palabras_clave"] =  df["principales palabras clave"]

df.head()



