from datetime import datetime
import os

# Obtener la hora actual
hora_actual = datetime.now()

print("Push efectuado a las: " + str(hora_actual))

usuario = os.getenv("GITHUB_ACTOR")
print(f"El usuario que ejecutó esta acción es: {usuario}")
