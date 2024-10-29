class EmpleadoDTO:
    def __init__(self, nombre, puesto, edad=None):
        self.nombre = nombre  # Llama al setter
        self.puesto = puesto  # Llama al setter
        self.edad = edad if edad is not None else 0  # Valor predeterminado para la edad

    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, value: str):
        if not isinstance(value, str):
            raise ValueError("nombre debe ser una cadena")
        self._nombre = value

    @property
    def puesto(self) -> str:
        return self._puesto
    
    @puesto.setter
    def puesto(self, value: str):
        if not isinstance(value, str):
            raise ValueError("puesto debe ser una cadena")
        self._puesto = value

    @property
    def edad(self) -> int:
        return self._edad
    
    @edad.setter
    def edad(self, value: int):
        if not isinstance(value, int):
            raise ValueError("edad debe ser un entero")
        self._edad = value

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'puesto': self.puesto,
            'edad': self.edad
        }
