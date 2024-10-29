from .estrategiaDTO import EstrategiaDTO

class SimulacionDTO:
    def __init__(self):
        self._id = None
        self._estrategias = []

    @property
    def estrategias(self):
        return self._estrategias
    
    @estrategias.setter
    def estrategias(self, estrategias_list):
        if not isinstance(estrategias_list, list):
            raise ValueError("estrategias_list debe ser una lista")

        # Verificar que todos los elementos en la lista sean de tipo GananciaTrimestralDTO
        for earning in estrategias_list:
            if not isinstance(earning, EstrategiaDTO):
                raise ValueError("Todos los elementos en estrategias_list deben ser del tipo EstrategiaDTO")

        self._estrategias = estrategias_list