import pandas as pd

from .finance.experts.simulacionDTO import (
    ActivoDTO,
    EstrategiaAutomatizadaDTO,
    EstrategiaTransaccionDTO,
    ParametroDTO,
    SimulacionDTO,
    TipoEstrategiaTransaccionDTO,
)

from .orian_simulation.trading.algorithm import (
    SteadyTrendAlgorithm,
    MajorityTrendAlgorithm,
    RandomAlgorithm,
)
from .orian_simulation.transaction import (
    TransactionQuantityManagerByWalletPercentage,
    TransactionQuantityManagerByFixedAmount,
    TransactionTriggerByRepeatedPredictions,
    Wallet
)

from .orian_simulation.market import Asset, StockMarketHandler, Currency
from .orian_simulation.strategy import AutomatedStrategy
from .orian_simulation.simulation import OnlineSimulation

from finance.models import Precio_Activo, Activo, Granularidad_Tiempo

disparador_map = {
    "Disparador de transacciones por predicciones repetitivas": {
        "class": TransactionTriggerByRepeatedPredictions,
        "params": {
            "repeticiones": int,
        },
    }
}

admin_cantidad_map = {
    "Administrador de cantidades por porcentaje": {
        "class": TransactionQuantityManagerByWalletPercentage,
        "params": {
            "porcentaje": float,
        },
    },
    "Administrador de cantidades por cantidad fija": {
        "class": TransactionQuantityManagerByFixedAmount,
        "params": {
            "cantidad": int,
        },
    },
}

trading_algorithm_map = {
    "Algoritmo de tendencia constante": {
        "class": SteadyTrendAlgorithm,
        "params": {
            "tamaño_ventana": int,
        },
    },
    "Algoritmo de tendencia mayoritaria": {
        "class": MajorityTrendAlgorithm,
        "params": {
            "tamaño_ventana": int,
        },
    },
    "Algoritmo aleatorio": {
        "class": RandomAlgorithm,
        "params": {},
    },
}




def encontrar_parametro_por_nombre(parametros_dto: list[ParametroDTO], nombre: str):
    for parametro in parametros_dto:
        if parametro.nombre == nombre:
            return parametro
    raise ValueError(f"El parámetro {nombre} no se encontró en la lista de parámetros {parametros_dto}")

def obtener_mapping_por_nombre(estrategia_transaccion_nombre: str):
    if estrategia_transaccion_nombre in disparador_map.keys():
        return disparador_map[estrategia_transaccion_nombre]
    
    elif estrategia_transaccion_nombre in admin_cantidad_map.keys():
        return admin_cantidad_map[estrategia_transaccion_nombre]

    elif estrategia_transaccion_nombre in trading_algorithm_map.keys():
        return trading_algorithm_map[estrategia_transaccion_nombre]
    
    else:
        raise ValueError(f"El nombre de la estrategia de transacción {estrategia_transaccion_nombre} no se encontró en el mapa de estrategias de transacción")

def instanciar_estrategia_transaccion(
        estrategia_transaccion: EstrategiaTransaccionDTO
        ):
    mapping = obtener_mapping_por_nombre(estrategia_transaccion.nombre)
    parametros = []
    for param_name, dtype in mapping["params"].items():
        param = encontrar_parametro_por_nombre(estrategia_transaccion.parametros, param_name)
        parametros.append(dtype(param.valor))

    return mapping["class"](*parametros)

def mapear_estrategia_dto(estrategiaDTO: EstrategiaAutomatizadaDTO):
    estrategia_activo = Asset(estrategiaDTO.activo.nombre, bool(estrategiaDTO.activo.es_entero)))    
    algoritmoDTO = estrategiaDTO.algoritmoTrading
    disparadorDTO = estrategiaDTO.disparadorTransaccionCompra
    admin_cantidad_compraDTO = estrategiaDTO.admninCantidadTransaccionCompra
    admin_cantidad_ventaDTO = estrategiaDTO.admninCantidadTransaccionVenta

    return AutomatedStrategy(
        trading_asset=estrategia_activo,
        trading_algorithm=instanciar_estrategia_transaccion(algoritmoDTO),
        priority=int(estrategiaDTO.prioridad), #                               
        transaction_trigger=instanciar_estrategia_transaccion(disparadorDTO),
        buy_transaction_quantity_manager=instanciar_estrategia_transaccion(admin_cantidad_compraDTO),
        sell_transaction_quantity_manager=instanciar_estrategia_transaccion(admin_cantidad_ventaDTO),
        name=estrategiaDTO.nombre
    )


def mapear_simulacion_dto(simulacionDTO: SimulacionDTO):
    # Mapear estrategias a AutomatedStrategy    
    estrategias: list[AutomatedStrategy] = []
    for estrategiaDTO in simulacionDTO.estrategias:
        estrategias.append(mapear_estrategia_dto(estrategiaDTO))

    # Obtener StockMarketHandler
    activos = []
    for estrategiaDTO in simulacionDTO.estrategias:
        estrategiaDTO: EstrategiaAutomatizadaDTO
        estrategiaDTO.activo.nombre
        estrategiaDTO.activo.id
        activos.append({
            "id": estrategiaDTO.activo._id,
            "nombre": estrategiaDTO.activo.nombre,
            "clase": Asset(estrategiaDTO.activo.nombre, bool(estrategiaDTO.activo.es_entero))
        })

    granularidad_id = simulacionDTO.granularidad_id
    conjunto_de_precios = [
        Precio_Activo.objects.filter(activo_id=activo["id"], granularidad_id=granularidad_id)
        for activo in activos
    ]
    markets = {}
    for activo, precios in zip(conjunto_de_precios, activos):
        fechas_list = [pd.Timestamp(precio.fecha_hora) for precio in precios]
        precios_lista = [float(precio.precio_cierre) for precio in precios]
        df = pd.DataFrame(precios_lista, index=fechas_list, columns=['Close'])
        markets[activo["clase"]] = df

    stock_market_handler = StockMarketHandler(markets)

    # Obtener cartera
    cantidades = {}
    cartera = simulacionDTO.cartera_dto
    for activo_cartera in cartera.lista_activo_cartera:
        activo_cartera: ActivoDTO
        activo = Asset(activo_cartera.nombre, bool(activo_cartera.es_entero))
        cantidades[activo] = int(activo_cartera.cantidad)
    wallet = Wallet(cantidades, Currency(simulacionDTO.moneda_base.nombre))

    return OnlineSimulation(stock_market_handler=stock_market_handler, strategies=estrategias, wallet=wallet)

