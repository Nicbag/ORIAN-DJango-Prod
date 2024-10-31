from .activoCarteraDTO import ActivoCarteraDTO

class CarteraDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._listaActivoCartera: list[ActivoCarteraDTO] = []

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not isinstance(value, str):
            raise ValueError("nombre debe ser una cadena")
        self._nombre = value

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

    @property
    def listaActivoCartera(self):
        return self._listaActivoCartera
    
    @listaActivoCartera.setter
    def listaActivoCartera(self, lista_activo_cartera):
        if not isinstance(lista_activo_cartera, list):
            raise ValueError("lista_activo_cartera debe ser una lista")

        # Verificar que todos los elementos en la lista sean de tipo ActivoCarteraDTO
        for i in lista_activo_cartera:
            if not isinstance(i, ActivoCarteraDTO):
                raise ValueError("Todos los elementos en lista_activo_cartera deben ser del tipo ActivoCarteraDTO")

        self._listaActivoCartera = lista_activo_cartera

    def __str__(self):
        return (f"CarteraDTO(id={self._id}, nombre={self._nombre}, listaActivoCartera={self._listaActivoCartera})")