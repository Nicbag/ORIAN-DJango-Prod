class ParametroDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._valor = None

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not isinstance(value, str):
            raise ValueError("nombre debe ser una cadena")
        self._nombre = value

    @property
    def valor(self):
        return self._valor
    
    @valor.setter
    def valor(self, value):
        if not isinstance(value, str):
            raise ValueError("valor debe ser una cadena")
        self._valor = value

    def __str__(self):
        return (f"ParametroDTO(id={self._id}, nombre={self._nombre}, valor={self._valor})")