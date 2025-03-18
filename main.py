from datetime import datetime
import requests
import os
import re
import subprocess


def contar_ramas():
    try:
        # Listar todas las ramas remotas
        resultado = subprocess.run(
            ["git", "branch", "-r"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        ramas = resultado.stdout.strip().split('\n')
        ramas = [r.strip() for r in ramas if r.strip()]
        return len(ramas)
    except subprocess.CalledProcessError as e:
        print("Error ejecutando git:", e.stderr)
        return 0

def nombre_ramas():
    resultado = subprocess.run(
        ["git", "branch", "-r"],
        capture_output=True,
        text=True
    )
    ramas = resultado.stdout.strip().split('\n')
    ramas_limpias = [
        r.strip().replace("origin/", "") for r in ramas 
        if r.strip() and '->' not in r
    ]
    return ramas_limpias

def contar_commits(rama):
    rama_remota = f"origin/{rama}"
    resultado = subprocess.run(
        ["git", "rev-list", "--count", rama_remota],
        capture_output=True,
        text=True
    )
    return int(resultado.stdout.strip())

def obtener_mensajes_commits(rama):
    # Obtener todos los hashes y los mensajes de commit para una rama remota
    rama_remota = f"origin/{rama}"
    resultado = subprocess.run(
        ["git", "log", "--pretty=format:%h %s", rama_remota],
        capture_output=True,
        text=True
    )

    # Procesar la salida y separar los hashes de los mensajes
    commits = resultado.stdout.strip().split('\n')
    hashes = []
    mensajes = []
    
    for commit in commits:
        hash_commit, mensaje_commit = commit.split(" ", 1)  # Separar hash y mensaje
        hashes.append(hash_commit)
        mensajes.append(mensaje_commit)
    
    # Devolver dos listas: una con los hashes y otra con los mensajes
    return hashes, mensajes

def obtener_ficheros_modificados_por_commit(commit_hash):
    # Ejecutar el comando git show para obtener los ficheros modificados en un commit
    resultado = subprocess.run(
        ["git", "show", "--name-only", "--pretty=format:", commit_hash],
        capture_output=True,
        text=True
    )

    # Comprobamos si hubo algún error en la ejecución
    if resultado.returncode != 0:
        print(f"Error al ejecutar el comando git show: {resultado.stderr}")
        return []

    # Procesar la salida y obtener los ficheros modificados
    ficheros_modificados = resultado.stdout.strip().split('\n')

    # Filtrar las líneas vacías (y el commit hash si es necesario)
    ficheros_modificados = [line for line in ficheros_modificados if line.strip()]

    return ficheros_modificados

def obtener_etiquetas_de_rama(rama):
    # Ejecutamos el comando git log con --decorate para ver las etiquetas de todos los commits en la rama
    resultado = subprocess.run(
        ["git", "log", "--oneline", "--decorate", rama],
        capture_output=True,
        text=True
    )
    
    if resultado.returncode != 0:
        print("Error al obtener las etiquetas.")
        return []

    # Lista para almacenar las etiquetas encontradas
    etiquetas = []
    #print(resultado)
    # Expresión regular para encontrar las etiquetas en la salida
    regex_etiqueta = r"tag: ([^\)]+)"

    # Iteramos sobre cada línea de la salida de git log
    for linea in resultado.stdout.splitlines():
        # Buscamos todas las etiquetas en la línea
        encontrado = re.findall(regex_etiqueta, linea)
        
        if encontrado:
            etiquetas.extend(encontrado)  # Añadimos todas las etiquetas encontradas

    # Eliminar etiquetas duplicadas (si es necesario)
    etiquetas = list(set(etiquetas))

    return etiquetas


def leer_archivo_en_rama(branch: str, path: str) -> str:
   
    try:
        # Guarda la rama actual
        rama_actual = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,  stderr=subprocess.DEVNULL
        ).strip()

        # Cambia a la rama deseada
        subprocess.run(["git", "checkout", branch], stdout=subprocess.DEVNULL,  stderr=subprocess.DEVNULL, check=True)

        # Lee el contenido del archivo
        if not os.path.exists(path):
            raise FileNotFoundError(f"Archivo no encontrado en la rama '{branch}': {path}")

        with open(path, 'r', encoding='utf-8') as f:
            contenido = f.read()

        return contenido
    except:
        print("[leer_archivo_en_rama] La rama " + str(rama) + " NO existe")
        pass

    finally:
        # Vuelve a la rama original
        subprocess.run(["git", "checkout", rama_actual], stdout=subprocess.DEVNULL,  stderr=subprocess.DEVNULL,check=True)

# linea_a_buscar: línea desde la que empieza a revisar el fichero ("package us.dit;")
def eliminar_parte_contenido(contenido: str, linea_a_buscar: str) -> str:
    
    # Buscar la línea que contiene 'linea_a_buscar'
    index_busqueda = contenido.find(linea_a_buscar)
    
    if index_busqueda != -1:
        # Eliminar todo lo que está antes de la línea que contiene 'linea_a_buscar'
        contenido = contenido[index_busqueda:]
    
    # Eliminar las líneas en blanco
    lineas = contenido.splitlines()
    nuevas_lineas = [linea for linea in lineas if linea.strip()]  # Solo las que no estén vacías
    
    return "\n".join(nuevas_lineas)

# Extrae el uvus y el timestamp del fichero de texto
def extraer_uvus_y_timestamp(texto):
    uvus = None
    timestamp = None

    # Buscar líneas tipo //clave:valor
    for linea in texto.splitlines():
        if match := re.match(r'//uvus:(.+)', linea):
            uvus = match.group(1).strip()
        elif match := re.match(r'//pass:(.+)', linea):
            timestamp = match.group(1).strip()

    return uvus, timestamp


if __name__ == "__main__":
   
    # Obtener la hora actual
    hora_actual = datetime.now()
    
    print("Push efectuado a las: " + str(hora_actual))

    usuario = os.getenv("GITHUB_ACTOR")
    print(f"El usuario que ejecutó esta acción es: {usuario}")

    total=contar_ramas()
    print(f"Número de ramas: {total}")

    ramas = nombre_ramas()	
    print("Nombre de las ramas y commits por rama:")
    for rama in ramas:
        print("-"+str(rama))
        print(" Nº commits: " +str(contar_commits(rama)))
        print(" Etiquetas: " + str(obtener_etiquetas_de_rama(rama)))
        print(" Mensajes de cada commit:")
        hashes, mensajes = obtener_mensajes_commits(rama)
        for i in range(len(mensajes)):
            print("     [" + str(hashes[i]) + "] " + mensajes[i])
            print("         * Ficheros modificados: " + str(obtener_ficheros_modificados_por_commit(hashes[i])))

    #rama = "uvus"
    
    contenidoFichero_enRama = leer_archivo_en_rama(rama, "claseControl.txt")
    
    repo_name = os.getenv('GITHUB_REPOSITORY')
    grupo = 1

    try:
         # Ejecucion de generaClase
        subprocess.run(["./generaClase", str(usuario), str(grupo)], stdout=subprocess.DEVNULL)

        # Fichero generado como resultado de generaClase
        contenidoFichero_generaClase = subprocess.check_output(["cat", "claseControl.txt"], text=True)
        #print(contenidoFichero_generaClase)

        # Solo la clase generada por generaClase
        contenidoFichero_generaClase_Clase = eliminar_parte_contenido(contenidoFichero_generaClase, "package us.dit;")
        # Clase subida por el alumno a su repo
        contenidoFichero_enRama_Clase = eliminar_parte_contenido(contenidoFichero_enRama, "package us.dit;")

        if contenidoFichero_generaClase_Clase == contenidoFichero_enRama_Clase:
            print("Los ficheros incluidos y esperados son iguales")
        
        uvus_leido, timestamp_leido = extraer_uvus_y_timestamp(contenidoFichero_enRama)
    except subprocess.CalledProcessError as e:
        print("El fichero generado por generaClase no se ha generado")
    

    
       



