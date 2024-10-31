# Primero, importa los modelos necesarios
from finance.models import Precio_Activo, Activo, Granularidad_Tiempo, Transaccion

#! ============================================================================0
# Define los IDs del activo y la granularidad que deseas consultar
activo_id = 51151  # Cambia esto por el ID del activo que necesitas
granularidad_id = 51210  # Cambia esto por el ID de la granularidad que necesitas

# Realiza la consulta
precios = Precio_Activo.objects.filter(activo_id=activo_id, granularidad_id=granularidad_id)

# Imprime los resultados
'''for precio in precios:
    print(f"ID: {precio.id}, Max Price: {precio.precio_max}, Close Price: {precio.precio_cierre}, "
          f"Open Price: {precio.precio_apertura}, Min Price: {precio.precio_min}, "
          f"Fecha y Hora: {precio.fecha_hora}")
'''

print(list(Transaccion.objects.all().values()))
#! ============================================================================0
# Obtener todos los activos
activos = Activo.objects.all()

# Filtrar activos por nombre
activos_filtrados = Activo.objects.filter(nombre='Activo Ejemplo')

# Obtener un activo específico por ID
activo_unico = Activo.objects.get(id=1)



from finance.models import Transaccion, Activo, Tipo_Transaccion, Cartera_Usuario, Historico_Cartera_Usuario

#! Historico Cartera Usuario
cartera_usuario_id = 51301
historicoCarteraUsuarios = list(Historico_Cartera_Usuario.objects.filter(cartera_usuario_id=cartera_usuario_id).values())
print(historicoCarteraUsuarios, "Historico Cartera Usuario")

transacciones = list(Transaccion.objects.filter(cartera_usuario=cartera_usuario_id).values())
print(transacciones)


#! Transacciones
transacciones = list(Transaccion.objects.all().values())
transaccionesDTO = []

for transaccion in transacciones:
    activo_id = transaccion['activo_id']
    activo = Activo.objects.get(id=activo_id)

    tipo_transaccion_id = transaccion['tipo_transaccion_id']
    tipo_transaccion = Tipo_Transaccion.objects.get(id=tipo_transaccion_id)

    cartera_usuario_id = transaccion['cartera_usuario_id']
    cartera_usuario = Cartera_Usuario.objects.get(id=cartera_usuario_id)
    
    # Serializa el objeto activo
    activo_dto = {
        "id": activo.id,
        "nombre": activo.nombre,
        # Agrega aquí otros campos que necesites del objeto Activo
    }

    # Serializa el objeto tipo_transaccion
    tipo_transaccion_dto = {
        "id": tipo_transaccion.id,
        "nombre": tipo_transaccion.nombre,
        # Agrega aquí otros campos que necesites del objeto Tipo_Transaccion
    }

    # Serializa el objeto cartera_usuario
    cartera_usuario_dto = {
        "id": cartera_usuario.id,
        "nombre": cartera_usuario.nombre,
        # Agrega aquí otros campos que necesites del objeto Cartera_Usuario
    }
    
    transaccionDTO = {
        "id": transaccion['id'],
        "cantidad": transaccion['cantidad'],
        "precio": transaccion['precio'],
        "fecha": transaccion['fecha'],
        "tipo_transaccion": tipo_transaccion_dto,
        "cartera_usuario": cartera_usuario_dto,
        "activo": activo_dto
    }
    transaccionesDTO.append(transaccionDTO)

print(transaccionesDTO)