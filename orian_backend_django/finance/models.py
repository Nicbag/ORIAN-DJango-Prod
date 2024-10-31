from django.db import models

# Create your models here.
class Tipo_Activo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'tipo_activo'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Granularidad_Tiempo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'granuaridad_tiempo'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Activo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    ticker = models.CharField(max_length=255)

    tipo_activo = models.ForeignKey(Tipo_Activo, on_delete=models.DO_NOTHING, db_column='tipo_activo_id')

    class Meta:
        db_table = 'activo'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Precio_Activo(models.Model):
    id = models.AutoField(primary_key=True)
    precio_max = models.FloatField()
    precio_min = models.FloatField()
    precio_apertura = models.FloatField()
    precio_cierre = models.FloatField()
    volumen = models.FloatField()
    fecha_hora = models.DateTimeField()  # Para fechas con hora

    activo = models.ForeignKey('Activo', on_delete=models.DO_NOTHING, db_column='activo_id')  
    granularidad = models.ForeignKey('Granularidad_Tiempo', on_delete=models.DO_NOTHING, db_column='granularidad_tiempo_id')


    class Meta:
        db_table = 'precio_activo'  # Nombre exacto de la tabla
        managed = False   
        app_label = 'finance'       

class Tipo_Transaccion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'tipo_transaccion'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Cartera_Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'cartera_usuario'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Historico_Cartera_Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField()
    valor_total = models.FloatField()

    cartera_usuario = models.ForeignKey('Cartera_Usuario', on_delete=models.DO_NOTHING, db_column='cartera_usuario_id')
    simulacion = models.ForeignKey('Simulacion', on_delete=models.DO_NOTHING, db_column='simulacion_id')

    class Meta:
        db_table = 'historico_cartera_usuario'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Activo_Cartera(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.FloatField()
    precio_compra = models.FloatField()
    fecha_compra = models.DateTimeField()
    cantidad_inicial = models.FloatField()

    activo = models.ForeignKey('Activo', on_delete=models.DO_NOTHING, db_column='activo_id')
    cartera = models.ForeignKey('Cartera_Usuario', on_delete=models.DO_NOTHING, db_column='cartera_usuario_id')

    class Meta:
        db_table = 'activo_cartera'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Transaccion(models.Model):
    id = models.AutoField(primary_key=True)
    cantidad = models.FloatField()
    precio = models.FloatField()
    fecha = models.DateTimeField()

    tipo_transaccion = models.ForeignKey('Tipo_Transaccion', on_delete=models.DO_NOTHING, db_column='tipo_transaccion_id')
    cartera_usuario = models.ForeignKey('Cartera_Usuario', on_delete=models.DO_NOTHING, db_column='cartera_usuario_id')
    activo = models.ForeignKey('Activo', on_delete=models.DO_NOTHING, db_column='activo_id')

    class Meta:
        db_table = 'transaccion'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

#! Simulaciones

class Tipo_Simulacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'tipo_simulacion'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Estado_Simulacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'estado_simulacion'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Simulacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    
    granularidad_tiempo = models.ForeignKey('Granularidad_Tiempo', on_delete=models.DO_NOTHING, db_column='granularidad_tiempo_id')
    cartera_usuario = models.ForeignKey('Cartera_Usuario', on_delete=models.DO_NOTHING, db_column='cartera_usuario_id')
    tipo_simulacion = models.ForeignKey('Tipo_Simulacion', on_delete=models.DO_NOTHING, db_column='tipo_simulacion_id')
    estado_simulacion = models.ForeignKey('Estado_Simulacion', on_delete=models.DO_NOTHING, db_column='estado_simulacion_id')

    class Meta:
        db_table = 'simulacion'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Historico_Estado_Simulacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()

    simulacion = models.ForeignKey('Simulacion', on_delete=models.DO_NOTHING, db_column='simulacion_id')
    estado_simulacion = models.ForeignKey('Estado_Simulacion', on_delete=models.DO_NOTHING, db_column='estado_simulacion_id')

    class Meta:
        db_table = 'historico_estado_simulacion'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

class Reporte_Simulacion(models.Model):
    id = models.AutoField(primary_key=True)
    roi = models.FloatField()
    ganancia_maxima = models.FloatField()
    perdida_maxima = models.FloatField()
    rendimiento = models.FloatField()
    fecha_hora = models.DateTimeField()

    simulacion = models.ForeignKey('Simulacion', on_delete=models.DO_NOTHING, db_column='simulacion_id')

    class Meta:
        db_table = 'reporte_simulacion'  # Nombre exacto de la tabla
        managed = False        # Desactiva las migraciones para esta tabla
        app_label = 'finance'

#! Estrategia Automatizada

class Tipo_Estrategia_Transaccion (models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'tipo_estrategia_transaccion'
        managed = False
        app_label = 'finance'

class Estrategia_Transaccion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    tipo_estrategia_transaccion = models.ForeignKey('Tipo_Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='tipo_estrategia_transaccion_id')
    activo = models.ForeignKey('Activo', on_delete=models.DO_NOTHING, db_column='activo_id')

    class Meta:
        db_table = 'estrategia_transaccion'
        managed = False
        app_label = 'finance'

class Parametro_Estrategia_Transaccion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    tipo_dato = models.CharField(max_length=255)
    valor_max = models.CharField(max_length=255)
    valor_min = models.CharField(max_length=255)
    valor_por_defecto = models.CharField(max_length=255)

    estrategia_transaccion = models.ForeignKey('Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='estrategia_transaccion_id')

    class Meta:
        db_table = 'parametro_estrategia_transaccion'
        managed = False
        app_label = 'finance'

class Estrategia_Automatizada (models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    
    admin_cantidad_transaccion_compra = models.ForeignKey('Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='admin_cantidad_transaccion_compra_id', related_name='admin_cantidad_transaccion_compra')
    admin_cantidad_transaccion_venta = models.ForeignKey('Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='admin_cantidad_transaccion_venta_id', related_name='admin_cantidad_transaccion_venta')
    disparador_transaccion_compra = models.ForeignKey('Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='disparador_transaccion_compra_id', related_name='disparador_transaccion_compra')
    disparador_transaccion_venta = models.ForeignKey('Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='disparador_transaccion_venta_id', related_name='disparador_transaccion_venta')
    algoritmo_trading = models.ForeignKey('Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='algoritmo_trading_id', related_name='algoritmo_trading')
    activo = models.ForeignKey('Activo', on_delete=models.DO_NOTHING, db_column='activo_id')

class Valor_Parametro_Estrategia_Transaccion (models.Model):
    id = models.AutoField(primary_key=True)
    valor = models.CharField(max_length=255)
    valor_cadena = models.CharField(max_length=255)

    parametro_estrategia_transaccion = models.ForeignKey('Parametro_Estrategia_Transaccion', on_delete=models.DO_NOTHING, db_column='parametro_estrategia_transaccion_id')
    estrategia_automatizada = models.ForeignKey('Estrategia_Automatizada', on_delete=models.DO_NOTHING, db_column='estrategia_automatizada_id')

    class Meta:
        db_table = 'valor_parametro_estrategia_transaccion'
        managed = False
        app_label = 'finance'

class Simulacion_Estrategia_Trading_Automatizada (models.Model):
    id = models.AutoField(primary_key=True)
    prioridad = models.IntegerField()

    estrategia_automatizada = models.ForeignKey('Estrategia_Automatizada', on_delete=models.DO_NOTHING, db_column='estrategia_automatizada_id')
    simulacion = models.ForeignKey('Simulacion', on_delete=models.DO_NOTHING, db_column='simulacion_id')

    class Meta:
        db_table = 'simulacion_estrategia_trading_automatizada'
        managed = False
        app_label = 'finance'

#! Estrategia Tradicional

class Estrategia_Trading_Tradicional(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    class Meta:
        db_table = 'estrategia_trading_tradicional'
        managed = False
        app_label = 'finance'

class Simulacion_Estrategia_Trading_Tradicional(models.Model):
    id = models.AutoField(primary_key=True)

    estrategia_trading_tradicional = models.ForeignKey('Estrategia_Trading_Tradicional', on_delete=models.DO_NOTHING, db_column='estrategia_trading_tradicional_id')
    simulacion = models.ForeignKey('Simulacion', on_delete=models.DO_NOTHING, db_column='simulacion_id')

    class Meta:
        db_table = 'simulacion_estrategia_trading_tradicional'
        managed = False
        app_label = 'finance'

class Tipo_Indicador (models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'tipo_indicador'
        managed = False
        app_label = 'finance'

class Indicador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

    tipo_indicador = models.ForeignKey('Tipo_Indicador', on_delete=models.DO_NOTHING, db_column='tipo_indicador_id')

    class Meta:
        db_table = 'indicador'
        managed = False
        app_label = 'finance'

class Parametro_Indicador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    tipo_dato = models.CharField(max_length=255)
    valor_max = models.CharField(max_length=255)
    valor_min = models.CharField(max_length=255)
    valor_por_defecto = models.CharField(max_length=255)

    indicador = models.ForeignKey('Indicador', on_delete=models.DO_NOTHING, db_column='indicador_id')

    class Meta:
        db_table = 'parametro_indicador'
        managed = False
        app_label = 'finance'

class Valor_Parametro(models.Model):
    id = models.AutoField(primary_key=True)
    valor = models.CharField(max_length=255)
    valor_cadena = models.CharField(max_length=255)

    parametro_indicador = models.ForeignKey('Parametro_Indicador', on_delete=models.DO_NOTHING, db_column='parametro_indicador_id')
    estrategia_trading_tradicional = models.ForeignKey('Estrategia_Trading_Tradicional', on_delete=models.DO_NOTHING, db_column='estrategia_trading_tradicional_id')

    class Meta:
        db_table = 'valor_parametro'
        managed = False
        app_label = 'finance'

