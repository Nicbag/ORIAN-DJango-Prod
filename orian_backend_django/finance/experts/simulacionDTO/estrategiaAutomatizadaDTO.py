from .activoDTO import ActivoDTO
from .estrategiaTransaccionDTO import EstrategiaTransaccionDTO

class EstrategiaAutomatizadaDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._activo = None
        self._admninCantidadTransaccionCompra = None
        self._admninCantidadTransaccionVenta = None
        self._disparadorTransaccionCompra = None
        self._disparadorTransaccionVenta = None
        self._algoritmoTrading = None
        self._prioridad = None

    @property
    def algoritmoTrading(self):
        return self._algoritmoTrading
    
    @algoritmoTrading.setter
    def algoritmoTrading(self, value):
        if not isinstance(value, EstrategiaTransaccionDTO):
            raise ValueError("algoritmoTrading debe ser un EstrategiaTransaccionDTO")
        self._algoritmoTrading = value

    @property
    def disparadorTransaccionVenta(self):
        return self._disparadorTransaccionVenta
    
    @disparadorTransaccionVenta.setter
    def disparadorTransaccionVenta(self, value):
        if not isinstance(value, EstrategiaTransaccionDTO):
            raise ValueError("disparadorTransaccionVenta debe ser un EstrategiaTransaccionDTO")
        self._disparadorTransaccionVenta = value

    @property
    def disparadorTransaccionCompra(self):
        return self._disparadorTransaccionCompra
    
    @disparadorTransaccionCompra.setter
    def disparadorTransaccionCompra(self, value):
        if not isinstance(value, EstrategiaTransaccionDTO):
            raise ValueError("disparadorTransaccionCompra debe ser un EstrategiaTransaccionDTO")
        self._disparadorTransaccionCompra = value

    @property
    def admninCantidadTransaccionVenta(self):
        return self._admninCantidadTransaccionVenta
    
    @admninCantidadTransaccionVenta.setter
    def admninCantidadTransaccionVenta(self, value):
        if not isinstance(value, EstrategiaTransaccionDTO):
            raise ValueError("admninCantidadTransaccionVenta debe ser un EstrategiaTransaccionDTO")
        self._admninCantidadTransaccionVenta = value

    @property
    def admninCantidadTransaccionCompra(self):
        return self._admninCantidadTransaccionCompra
    
    @admninCantidadTransaccionCompra.setter
    def admninCantidadTransaccionCompra(self, value):
        if not isinstance(value, EstrategiaTransaccionDTO):
            raise ValueError("admninCantidadTransaccionCompra debe ser un EstrategiaTransaccionDTO")
        self._admninCantidadTransaccionCompra = value

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
    def activo(self):
        return self._activo
    
    @activo.setter
    def activo(self, value):
        if not isinstance(value, ActivoDTO):
            raise ValueError("activo debe ser una cadena")
        self._activo = value



    @property
    def prioridad(self):
        return self._prioridad
    
    @prioridad.setter
    def prioridad(self, value):
        if not isinstance(value, str):
            raise ValueError("prioridad debe ser una cadena")
        self._prioridad = value

    def __str__(self):
        return (f"EstrategiaAutomatizadaDTO(id={self._id}, nombre={self._nombre}, "
                f"activo={self._activo}, "
                f"admninCantidadTransaccionCompra={self._admninCantidadTransaccionCompra}, "
                f"admninCantidadTransaccionVenta={self._admninCantidadTransaccionVenta}, "
                f"disparadorTransaccionCompra={self._disparadorTransaccionCompra}, "
                f"disparadorTransaccionVenta={self._disparadorTransaccionVenta}, "
                f"algoritmoTrading={self._algoritmoTrading}, "
                f"prioridad={self._prioridad})")