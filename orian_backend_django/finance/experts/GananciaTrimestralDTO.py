
class GananciaTrimestralDTO:
    def __init__(self):
        self._fechaFinalFiscal = None
        self._fechaReportada = None
        self._gananciaReportada = None
        self._gananciaEstimada = None
        self._sorpresaNeta = None
        self._sorpresaPorcentaje = None

    @property
    def fechaFinalFiscal(self) -> str:
        return self._fechaFinalFiscal
    
    @fechaFinalFiscal.setter
    def fechaFinalFiscal(self, value: str):
        if not isinstance(value, str):
            raise ValueError("fechaFinalFiscal debe ser una cadena")
        self._fechaFinalFiscal = value

    @property
    def fechaReportada(self) -> str:
        return self._fechaReportada
    
    @fechaReportada.setter
    def fechaReportada(self, value: str):
        if not isinstance(value, str):
            raise ValueError("fechaReportada debe ser una cadena")
        self._fechaReportada = value

    @property
    def gananciaReportada(self) -> str:
        return self._gananciaReportada
    
    @gananciaReportada.setter
    def gananciaReportada(self, value: str):
        if not isinstance(value, str):
            raise ValueError("gananciaReportada debe ser una cadena")
        self._gananciaReportada = value

    @property
    def gananciaEstimada(self) -> str:
        return self._gananciaEstimada
    
    @gananciaEstimada.setter
    def gananciaEstimada(self, value: str):
        if not isinstance(value, str):
            raise ValueError("gananciaEstimada debe ser una cadena")
        self._gananciaEstimada = value

    @property
    def sorpresaNeta(self) -> str:
        return self._sorpresaNeta
    
    @sorpresaNeta.setter
    def sorpresaNeta(self, value: str):
        if not isinstance(value, str):
            raise ValueError("sorpresaNeta debe ser una cadena")
        self._sorpresaNeta = value

    @property
    def sorpresaPorcentaje(self) -> str:
        return self._sorpresaPorcentaje
    
    @sorpresaPorcentaje.setter
    def sorpresaPorcentaje(self, value: str):
        if not isinstance(value, str):
            raise ValueError("sorpresaPorcentaje debe ser una cadena")
        self._sorpresaPorcentaje = value

    def to_dict(self):
        return {
            'fechaFinalFiscal': self.fechaFinalFiscal,
            'fechaReportada': self.fechaReportada,
            'gananciaReportada': self.gananciaReportada,
            'gananciaEstimada': self.gananciaEstimada,
            'sorpresaNeta': self.sorpresaNeta,
            'sorpresaPorcentaje': self.sorpresaPorcentaje
        }