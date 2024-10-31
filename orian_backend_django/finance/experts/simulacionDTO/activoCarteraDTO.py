from .activoDTO import ActivoDTO

class ActivoCarteraDTO:
    def __init__(self):
        self._id = None
        self._ticker = None
        self._cantidad = None

    @property
    def ticker(self):
        return self._nombre
    
    @ticker.setter
    def ticker(self, value):
        if not isinstance(value, str):
            raise ValueError("ticker debe ser una cadena")
        self._ticker = value

    @property
    def cantidad(self):
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self, value):
        if not isinstance(value, str):
            raise ValueError("cantidad debe ser una cadena")
        self._cantidad = value


    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise ValueError("id debe ser una cadena")
        self._id = value

    def __str__(self):
        return (f"ActivoCarteraDTO(id={self._id}, nombre={self._nombre}, cantidad={self._cantidad})")