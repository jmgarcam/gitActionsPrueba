from datetime import datetime
import requests
import os
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
        print(" Mensajes de cada commit:")
        hashes, mensajes = obtener_mensajes_commits(rama)
        for i in range(len(mensajes)):
            print("     [" + str(hashes[i]) + "] " + mensajes[i])
            print("         * Ficheros modificados: " + str(obtener_ficheros_modificados_por_commit(hashes[i])))
        
            
       



