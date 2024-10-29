from .EmpleadoDTO import EmpleadoDTO
from .GananciaTrimestralDTO import GananciaTrimestralDTO

class InfoDTO:
    def __init__(self):
        self._ticker = None
        self._pais = None
        self._sitioWeb = None
        self._industria = None
        self._sector = None
        self._descripcion = None
        self._totalEmpleados = None
        self._capitalizacion = None
        self._divisa = None
        self._exchange = None
        self._fechaDividendos = None
        self._exFechaDividendos = None
        self._ultimoCuarto = None
        self._empleados = []
        self._gananciaTrimestrales = []

    @property
    def gananciaTrimestrales(self):
        return self._gananciaTrimestrales
    
    @gananciaTrimestrales.setter
    def gananciaTrimestrales(self, quarterly_earnings):
        if not isinstance(quarterly_earnings, list):
            raise ValueError("gananciaTrimestrales debe ser una lista")
         
        self._gananciaTrimestrales = quarterly_earnings

    @property
    def empleados(self):
        return self._empleados

    @empleados.setter
    def empleados(self, company_officers):
        if not isinstance(company_officers, list):
            raise ValueError("empleados debe ser una lista")
         
        self._empleados = company_officers

    @property
    def ticker(self) -> str:
        return self._ticker

    @ticker.setter
    def ticker(self, value: str):
        if not isinstance(value, str):
            raise ValueError("ticker debe ser una cadena")
        self._ticker = value

    @property
    def pais(self) -> str:
        return self._pais

    @pais.setter
    def pais(self, value: str):
        if not isinstance(value, str):
            raise ValueError("pais debe ser una cadena")
        self._pais = value

    @property
    def sitioWeb(self) -> str:
        return self._sitioWeb

    @sitioWeb.setter
    def sitioWeb(self, value: str):
        if not isinstance(value, str):
            raise ValueError("sitio_web debe ser una cadena")
        self._sitioWeb = value

    @property
    def industria(self) -> str:
        return self._industria

    @industria.setter
    def industria(self, value: str):
        if not isinstance(value, str):
            raise ValueError("industria debe ser una cadena")
        self._industria = value

    @property
    def sector(self) -> str:
        return self._sector

    @sector.setter
    def sector(self, value: str):
        if not isinstance(value, str):
            raise ValueError("sector debe ser una cadena")
        self._sector = value

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value: str):
        if not isinstance(value, str):
            raise ValueError("descripcion debe ser una cadena")
        self._descripcion = value

    @property
    def totalEmpleados(self) -> str:
        return self._totalEmpleados

    @totalEmpleados.setter
    def totalEmpleados(self, value: str):
        if value is not None and not isinstance(value, (str, int)):
            raise ValueError("total_empleados debe ser una cadena o un número entero")
        self._totalEmpleados = str(value) if value is not None else None

    @property
    def capitalizacion(self) -> str:
        return self._capitalizacion
    
    @capitalizacion.setter
    def capitalizacion(self, value: str):
        if not isinstance(value, str):
            raise ValueError("capitalizacion debe ser una cadena")
        self._capitalizacion = value

    @property
    def divisa(self) -> str:
        return self._divisa
    
    @divisa.setter
    def divisa(self, value: str):
        if not isinstance(value, str):
            raise ValueError("divisa debe ser una cadena")
        self._divisa = value

    @property
    def exchange(self) -> str:
        return self._exchange
    
    @exchange.setter
    def exchange(self, value: str):
        if not isinstance(value, str):
            raise ValueError("exchange debe ser una cadena")
        self._exchange = value

    @property
    def fechaDividendos(self) -> str:
        return self._fechaDividendos
    
    @fechaDividendos.setter
    def fechaDividendos(self, value: str):
        if not isinstance(value, str):
            raise ValueError("fechaDividendos debe ser una cadena")
        self._fechaDividendos = value

    @property
    def exFechaDividendos(self) -> str:
        return self._exFechaDividendos
    
    @exFechaDividendos.setter
    def exFechaDividendos(self, value: str):
        if not isinstance(value, str):
            raise ValueError("exFechaDividendos debe ser una cadena")
        self._exFechaDividendos = value

    @property
    def ultimoCuarto(self) -> str:
        return self._ultimoCuarto
    
    @ultimoCuarto.setter
    def ultimoCuarto(self, value: str):
        if not isinstance(value, str):
            raise ValueError("ultimoCuarto debe ser una cadena")
        self._ultimoCuarto = value

    def to_dict(self):
        return {
            'ticker': self._ticker,
            'pais': self._pais,
            'sitioWeb': self._sitioWeb,
            'industria': self._industria,
            'sector': self._sector,
            'descripcion': self._descripcion,
            'totalEmpleados': self._totalEmpleados,
            'capitalizacion': self._capitalizacion,
            'divisa': self._divisa,
            'exchange': self._exchange,
            'fechaDividendos': self._fechaDividendos,
            'exFechaDividendos': self._exFechaDividendos,
            'ultimoCuarto': self._ultimoCuarto,
            'empleados': self._empleados,
            'gananciaTrimestrales': self._gananciaTrimestrales
        }

