import hashlib
from datetime import datetime, timedelta

# Crear el hash
def crear_identificador(uvus, timestamp):
    if uvus:
        uvus = uvus.lower()
    base = f"{uvus}:{timestamp}"
    return hashlib.sha256(base.encode('utf-8')).hexdigest()

# Verificar hash contra posibles timestamps
def verificar_identificador(uvus, hash_recibido, timestamp_base):

    for offset in range(timestamp_base[0], timestamp_base[1] + 1):
        hash_intento = crear_identificador(uvus, offset)

        if hash_intento == hash_recibido:
            return True  # Coincide con este timestamp

    return False, None

