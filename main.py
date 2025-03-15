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
	    print("		Nº commits: " + str(contar_commits(rama)))




