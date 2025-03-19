from datetime import datetime
import requests
import os
import re
import subprocess
from validacion_credenciales import *
from generaJson import *

def extraer_grupo(valor):
    # Usamos una expresión regular para extraer el valor después de "Control1."
    match = re.search(r'Control\w+\.(\d+)_\d+', valor)
    if match:
        return match.group(1)  # Devuelve el valor de 'x' (ej. 'x_25')
    else:
        return None  # Retorna None si no encuentra el patrón esperado


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
        contenido = subprocess.check_output(
            ["git", "show", f"{branch}:{path}"],
            text=True
        )
        return contenido
    except subprocess.CalledProcessError as e:
        print(f"[leer_archivo_sin_checkout] Error: {e}")
        return ""

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
def extraer_uvus_y_hash(texto):
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
   
    resultados = dict()
    # Obtener la hora actual
    hora_actual = datetime.now()

    repo_name = os.getenv('GITHUB_REPOSITORY')

    resultados["repo_name"] = repo_name

    print("Repo name: " + str(repo_name))
    if repo_name:
        grupo = extraer_grupo(repo_name)
        print("Grupo al que pertenece: " + str(grupo))
        resultados["grupo"] = grupo
    #grupo = 1
    
    print("Push efectuado a las: " + str(hora_actual))

    usuario = os.getenv("GITHUB_ACTOR")
    resultados["usuario"] = usuario
    print(f"El usuario que ejecutó esta acción es: {usuario}")

    num_ramas=contar_ramas()
    print(f"Número de ramas: {num_ramas}")
    resultados["num_ramas"] = num_ramas

    ramas = nombre_ramas()
    resultados["ramas"] = ramas

    resultados["commits"] = {clave: {} for clave in ramas}
    resultados["ficheros"] = {clave: {} for clave in ramas}

    
    print("Nombre de las ramas y commits por rama:")
    for rama in ramas:
        print("-"+str(rama))
        print(" Nº commits: " +str(contar_commits(rama)))
        print(" Etiquetas: " + str(obtener_etiquetas_de_rama(rama)))
        
        hashes, mensajes = obtener_mensajes_commits(rama)
        for i in range(len(mensajes)):
            resultados["commits"][rama].update({hashes[i]:mensajes[i]})
            resultados["ficheros"][rama].update({hashes[i]:obtener_ficheros_modificados_por_commit(hashes[i])})
            #print("     [" + str(hashes[i]) + "] " + mensajes[i])
            #print("         * Ficheros modificados: " + str(obtener_ficheros_modificados_por_commit(hashes[i])))
    

    #print(resultados["commits"]["main"])
    #print(resultados["ficheros"]["main"])
    contenidoFichero_enRama = leer_archivo_en_rama(rama, "claseControl.txt")
       

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

        resultados["ficheros_iguales"] = False
        if contenidoFichero_generaClase_Clase == contenidoFichero_enRama_Clase:
            print("El fichero del alumno y el esperado son iguales")
            resultados["ficheros_iguales"] = True
        else:
            print("El fichero del alumno y el esperado  NO son iguales")
        
        uvus_leido, hash_leido = extraer_uvus_y_hash(contenidoFichero_enRama)
        print("hash leido del alumno " +str(hash_leido))

        resultados["hash_leido"] = hash_leido
        
        # timestamp entre 18/03 y 30/03
        rango_fechas = [1742315579, 1743345179]
        
        comprobacion_hash, hash_calculado = verificar_identificador(str(uvus_leido), hash_leido, rango_fechas)

        resultados["hash calculado"] = hash_calculado

        resultados["hash_coinciden"] = False
        if(comprobacion_hash == True):
            print("Los hashs coinciden")
            resultados["hash_coinciden"] = True
        else:
            print("Los hashs NO coinciden")
        
        guardar_json(resultados, str(usuario)+".json")

    except subprocess.CalledProcessError as e:
        print("El fichero generado por generaClase no se ha generado")
    
        # 18/03/25 de 9:00 a 9:30

        
       



