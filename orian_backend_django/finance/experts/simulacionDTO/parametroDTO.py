class ParametroDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._valor = None

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("id debe ser una entero")
        self._id = value

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
        print(type(value))
        print(value)
        
        try:
            self._valor = float(value)
        except Exception:
            raise ValueError("valor debe ser un numero")

    def __str__(self):
        return (f"ParametroDTO(id={self._id}, nombre={self._nombre}, valor={self._valor})")