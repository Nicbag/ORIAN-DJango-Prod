from .parametroDTO import ParametroDTO

class EstrategiaDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._parametros = []

    @property
    def parametros(self):
        return self._parametros
    
    @parametros.setter
    def parametros(self, parametros_list):
        if not isinstance(parametros_list, list):
            raise ValueError("parametros debe ser una lista")

        # Verificar que todos los elementos en la lista sean de tipo ParametroDTO
        for parametro in parametros_list:
            if not isinstance(parametro, ParametroDTO):
                raise ValueError("Todos los elementos en parametros deben ser del tipo ParametroDTO")

        self._parametros = parametros_list

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not isinstance(value, str):
            raise ValueError("nombre debe ser una cadena")
        self._nombre = value
