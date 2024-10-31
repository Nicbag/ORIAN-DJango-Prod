class ActivoDTO:
    def __init__(self):
        self._id = None
        self._ticker = None
        self._es_entero: str = None

    @property
    def ticker(self):
        return self._ticker
    
    @ticker.setter
    def ticker(self, value):
        if not isinstance(value, str):
            raise ValueError("ticker debe ser una cadena")
        self._ticker = value

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise ValueError("id debe ser una cadena")
        self._id = value

    @property
    def es_entero(self):
        return self._es_entero
    
    @es_entero.setter
    def es_entero(self, value):
        if not isinstance(value, str):
            raise ValueError("es_entero debe ser una cadena")
        self._es_entero = value

    def __str__(self):
        return (f"ActivoDTO(id={self._id}, nombre={self._nombre}, es_entero={self._es_entero})")