# Primero, importa los modelos necesarios
from finance.models import Precio_Activo, Activo, Granularidad_Tiempo

#! ============================================================================0
# Define los IDs del activo y la granularidad que deseas consultar
activo_id = 51151  # Cambia esto por el ID del activo que necesitas
granularidad_id = 51210  # Cambia esto por el ID de la granularidad que necesitas

# Realiza la consulta
precios = Precio_Activo.objects.filter(activo_id=activo_id, granularidad_id=granularidad_id)

# Imprime los resultados
for precio in precios:
    print(f"ID: {precio.id}, Max Price: {precio.precio_max}, Close Price: {precio.precio_cierre}, "
          f"Open Price: {precio.precio_apertura}, Min Price: {precio.precio_min}, "
          f"Fecha y Hora: {precio.fecha_hora}")


#! ============================================================================0
# Obtener todos los activos
activos = Activo.objects.all()

# Filtrar activos por nombre
activos_filtrados = Activo.objects.filter(nombre='Activo Ejemplo')

# Obtener un activo específico por ID
activo_unico = Activo.objects.get(id=1)