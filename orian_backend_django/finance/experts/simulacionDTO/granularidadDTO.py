class GranularidadDTO:
    def __init__(self):
        self._id = None
        self._nombre = None

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
        if not isinstance(value, int):
            raise ValueError("id debe ser una int")
        self._id = value


    def __str__(self):
        return (f"GranularidadDTO(id={self._id}, nombre={self._nombre})")