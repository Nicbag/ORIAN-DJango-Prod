from .estrategiaAutomatizadaDTO import EstrategiaAutomatizadaDTO
from .carteraDTO import CarteraDTO
from .activoDTO import ActivoDTO
from .granularidadDTO import GranularidadDTO
from .estrategiaTransaccionDTO import EstrategiaTransaccionDTO
from .tipoEstrategiaTransaccion import TipoEstrategiaTransaccionDTO
from .parametroDTO import ParametroDTO
from .activoCarteraDTO import ActivoCarteraDTO

class SimulacionDTO:
    def __init__(self):
        self._id = None
        self._nombre = None
        self._fechaDesde = None
        self._fechaHasta = None
        self._estrategiasAutomatizadas: list[EstrategiaAutomatizadaDTO] = []
        self._granularidad: GranularidadDTO = None
        self._carteraUsuario: CarteraDTO = None
        self._monedaBase: ActivoDTO = None

    @property
    def fechaDesde(self):
        return self._fechaDesde
    
    @fechaDesde.setter
    def fechaDesde(self, value):
        if not isinstance(value, str):
            raise ValueError("fechaDesde debe ser una cadena")
        self._fechaDesde = value

    @property
    def fechaHasta(self):
        return self._fechaHasta
    
    @fechaHasta.setter
    def fechaHasta(self, value):
        if not isinstance(value, str):
            raise ValueError("fechaHasta debe ser una cadena")
        self._fechaHasta = value

    @property
    def estrategias(self):
        return self._estrategiasAutomatizadas
    
    @estrategias.setter
    def estrategias(self, estrategias_list):
        if not isinstance(estrategias_list, list):
            raise ValueError("estrategias_list debe ser una lista")

        # Verificar que todos los elementos en la lista sean de tipo GananciaTrimestralDTO
        for i in estrategias_list:
            if not isinstance(i, EstrategiaAutomatizadaDTO):
                raise ValueError("Todos los elementos en estrategias_list deben ser del tipo EstrategiaDTO")

        self._estrategiasAutomatizadas = estrategias_list

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not isinstance(value, str):
            raise ValueError("nombre debe ser una cadena")
        self._nombre = value


    @property
    def granularidad(self):
        return self.granularidad
    
    @granularidad.setter
    def granularidad(self, value):
        if not isinstance(value, GranularidadDTO):
            raise ValueError("granularidad_id debe ser una GranularidadDTO")
        self._granularidad = value

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if not isinstance(value, str):
            raise ValueError("id debe ser una cadena")
        self._id = value

    @property
    def carteraUsuario(self):
        return self._carteraUsuario

    @carteraUsuario.setter
    def carteraUsuario(self, value):
        if not isinstance(value, CarteraDTO):
            raise ValueError("cartera_dto debe ser una CarteraDTO")
        self._carteraUsuario = value

    @property
    def monedaBase(self):
        return self._monedaBase
    
    @monedaBase.setter
    def monedaBase(self, value):
        if not isinstance(value, ActivoDTO):
            raise ValueError("moneda_base debe ser una ActivoDTO")
        self._monedaBase = value

    def __str__(self):
        return (f"SimulacionDTO(id={self._id}, nombre={self._nombre}, "
                f"estrategiasAutomatizadas={self._estrategiasAutomatizadas}, "
                f"granularidad={self._granularidad}, "
                f"carteraUsuario={self._carteraUsuario}, "
                f"monedaBase={self._monedaBase})")