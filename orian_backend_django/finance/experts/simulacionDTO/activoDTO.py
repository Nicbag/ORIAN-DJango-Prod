

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
        if not isinstance(value, int):
            raise ValueError("id debe ser una int")
        self._id = value

    @property
    def es_entero(self):
        return self._es_entero

    @es_entero.setter
    def es_entero(self, value):
        if (value.upper() != "VERDADERO") and (value.upper() != "FALSO"):
            raise ValueError(f"es_entero ({value}) debe ser una cadena que represente un booleano verdadero o falso")

        if value.upper() == "VERDADERO":
            self._es_entero = True
            return
        if value.upper() == "FALSO":
            self._es_entero = False
            return

    def __str__(self):
        return f"ActivoDTO(id={self._id}, nombre={self._ticker}, es_entero={self._es_entero})"
