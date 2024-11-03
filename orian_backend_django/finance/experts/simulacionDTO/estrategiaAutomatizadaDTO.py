from .activoDTO import ActivoDTO
from .estrategiaTransaccionDTO import EstrategiaTransaccionDTO

class EstrategiaAutomatizadaDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._activo = None
        self._adminCantidadTransaccionCompra = None
        self._adminCantidadTransaccionVenta = None
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
    def adminCantidadTransaccionVenta(self):
        return self._adminCantidadTransaccionVenta
    
    @adminCantidadTransaccionVenta.setter
    def adminCantidadTransaccionVenta(self, value):
        if not isinstance(value, EstrategiaTransaccionDTO):
            raise ValueError("adminCantidadTransaccionVenta debe ser un EstrategiaTransaccionDTO")
        self._adminCantidadTransaccionVenta = value

    @property
    def adminCantidadTransaccionCompra(self):
        return self._adminCantidadTransaccionCompra
    
    @adminCantidadTransaccionCompra.setter
    def adminCantidadTransaccionCompra(self, value):
        if not isinstance(value, EstrategiaTransaccionDTO):
            raise ValueError("adminCantidadTransaccionCompra debe ser un EstrategiaTransaccionDTO")
        self._adminCantidadTransaccionCompra = value

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
        if not isinstance(value, int):
            raise ValueError("prioridad debe ser una int")
        self._prioridad = value

    def __str__(self):
        return (f"EstrategiaAutomatizadaDTO(id={self._id}, nombre={self._nombre}, "
                f"activo={self._activo}, "
                f"adminCantidadTransaccionCompra={self._adminCantidadTransaccionCompra}, "
                f"adminCantidadTransaccionVenta={self._adminCantidadTransaccionVenta}, "
                f"disparadorTransaccionCompra={self._disparadorTransaccionCompra}, "
                f"disparadorTransaccionVenta={self._disparadorTransaccionVenta}, "
                f"algoritmoTrading={self._algoritmoTrading}, "
                f"prioridad={self._prioridad})")