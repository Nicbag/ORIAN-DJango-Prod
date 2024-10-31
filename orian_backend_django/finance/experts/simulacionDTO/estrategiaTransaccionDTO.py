from .tipoEstrategiaTransaccion import TipoEstrategiaTransaccionDTO
from .parametroDTO import ParametroDTO

class EstrategiaTransaccionDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._tipoEstrategiaTransaccion = None
        self._parametros = []

    @property
    def parametros(self):
        return self._parametros
    
    @parametros.setter
    def parametros(self, parametros_list):
        if not isinstance(parametros_list, list):
            raise ValueError("parametros_list debe ser una lista")

        # Verificar que todos los elementos en la lista sean de tipo ParametroDTO
        for i in parametros_list:
            if not isinstance(i, ParametroDTO):
                raise ValueError("Todos los elementos en parametros_list deben ser del tipo ParametroDTO")

        self._parametros = parametros_list

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not isinstance(value, str):
            raise ValueError("nombre debe ser una cadena")
        self._nombre = value

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise ValueError("id debe ser una cadena")
        self._id = value

    @property
    def tipoEstrategiaTransaccion(self):
        return self._tipoEstrategiaTransaccion
    
    @tipoEstrategiaTransaccion.setter
    def tipoEstrategiaTransaccion(self, value):
        if not isinstance(value, TipoEstrategiaTransaccionDTO):
            raise ValueError("tipoEstrategiaTransaccion debe ser una TipoEstrategiaTransaccionDTO")
        self._tipoEstrategiaTransaccion = value

    def __str__(self):
        return f"{self.nombre} - {self.tipoEstrategiaTransaccion}"