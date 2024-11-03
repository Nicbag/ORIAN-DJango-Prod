import pandas as pd

from finance.experts.simulacionDTO import (
    ActivoDTO,
    EstrategiaAutomatizadaDTO,
    EstrategiaTransaccionDTO,
    ParametroDTO,
    SimulacionDTO,
    TipoEstrategiaTransaccionDTO,
    ActivoCarteraDTO,
)

from .trading.algorithm import (
    SteadyTrendAlgorithm,
    MajorityTrendAlgorithm,
    RandomAlgorithm,
)
from .transaction import (
    TransactionEnum,
    TransactionQuantityManagerByWalletPercentage,
    TransactionQuantityManagerByFixedAmount,
    TransactionTriggerByRepeatedPredictions,
    Wallet,
)

from .market import Asset, StockMarketHandler, Currency
from .strategy import AutomatedStrategy
from .simulation import OnlineSimulation

from finance.models import Precio_Activo, Activo, Granularidad_Tiempo, Activo_Cartera

disparador_map = {
    "Disparador de transacciones por predicciones consecutivas": {
        "class": TransactionTriggerByRepeatedPredictions,
        "params": {
            "Cantidad de predicciones consecutivas": int,
        },
    }
}

admin_cantidad_map = {
    "Administrador cantidad por porcentaje": {
        "class": TransactionQuantityManagerByWalletPercentage,
        "params": {
            "Porcentaje": lambda x: float(x) / 100,
        },
    },
    "Administrador cantidad por valor fijo": {
        "class": TransactionQuantityManagerByFixedAmount,
        "params": {
            "Cantidad": int,
        },
    },
}

trading_algorithm_map = {
    "Algoritmo de tendencia constante": {
        "class": SteadyTrendAlgorithm,
        "params": {
            "Longitud de ventana": int,
        },
    },
    "Algoritmo de tendencia mayoritaria": {
        "class": MajorityTrendAlgorithm,
        "params": {
            "Longitud de ventana": int,
        },
    },
    "Algoritmo aleatorio": {
        "class": RandomAlgorithm,
        "params": {},
    },
}

transaction_type_str_map = {
    TransactionEnum.SELL: "VENTA",
    TransactionEnum.BUY: "COMPRA",
}


def encontrar_parametro_por_nombre(parametros_dto: list[ParametroDTO], nombre: str):
    for parametro in parametros_dto:
        if parametro.nombre == nombre:
            return parametro
    raise ValueError(
        f"El parámetro '{nombre}' no se encontró en la lista de parámetros {[p.nombre for p in parametros_dto]}"
    )


def obtener_mapping_por_nombre(estrategia_transaccion_nombre: str):
    if estrategia_transaccion_nombre in disparador_map.keys():
        return disparador_map[estrategia_transaccion_nombre]

    elif estrategia_transaccion_nombre in admin_cantidad_map.keys():
        return admin_cantidad_map[estrategia_transaccion_nombre]

    elif estrategia_transaccion_nombre in trading_algorithm_map.keys():
        return trading_algorithm_map[estrategia_transaccion_nombre]

    else:
        raise ValueError(
            f"El nombre de la estrategia de transacción {estrategia_transaccion_nombre} no se encontró en el mapa de estrategias de transacción"
        )


def instanciar_estrategia_transaccion(
    estrategia_transaccion: EstrategiaTransaccionDTO, wallet: Wallet
):
    mapping = obtener_mapping_por_nombre(estrategia_transaccion.nombre)
    parametros = []

    if estrategia_transaccion.nombre in admin_cantidad_map.keys():
        parametros.append(wallet)

    for param_name, dtype in mapping["params"].items():
        param = encontrar_parametro_por_nombre(
            estrategia_transaccion.parametros, param_name
        )
        parametros.append(dtype(param.valor))

    return mapping["class"](*parametros)


def mapear_estrategia_dto(estrategiaDTO: EstrategiaAutomatizadaDTO, wallet: Wallet):
    estrategia_activo = Asset(
        estrategiaDTO.activo.ticker, bool(estrategiaDTO.activo.es_entero)
    )
    algoritmoDTO = estrategiaDTO.algoritmoTrading
    disparadorDTO = estrategiaDTO.disparadorTransaccionCompra
    admin_cantidad_compraDTO = estrategiaDTO.adminCantidadTransaccionCompra
    admin_cantidad_ventaDTO = estrategiaDTO.adminCantidadTransaccionVenta

    return AutomatedStrategy(
        trading_asset=estrategia_activo,
        trading_algorithm=instanciar_estrategia_transaccion(algoritmoDTO, wallet),
        priority=int(estrategiaDTO.prioridad),  #
        transaction_trigger=instanciar_estrategia_transaccion(disparadorDTO, wallet),
        buy_transaction_quantity_manager=instanciar_estrategia_transaccion(
            admin_cantidad_compraDTO, wallet
        ),
        sell_transaction_quantity_manager=instanciar_estrategia_transaccion(
            admin_cantidad_ventaDTO, wallet
        ),
        name=estrategiaDTO.nombre,
    )


def encontrar_activo_dado_su_ticker(ticker: str, activos: dict) -> dict:
    for activo in activos:
        if activo["nombre"] == ticker:
            return activo
    raise ValueError(
        f"El activo con ticker {ticker} no se encontró en la lista de activos {activos}"
    )


def mapear_simulacion_dto(simulacionDTO: SimulacionDTO):
    # Obtener StockMarketHandler
    activos = []
    for estrategiaDTO in simulacionDTO.estrategias:
        estrategiaDTO: EstrategiaAutomatizadaDTO
        activos.append(
            {
                "id": estrategiaDTO.activo._id,
                "nombre": estrategiaDTO.activo.ticker,
                "clase": Asset(
                    estrategiaDTO.activo.ticker, bool(estrategiaDTO.activo.es_entero)
                ),
            }
        )

    # Obtener cartera
    cantidades = {}
    cartera = simulacionDTO.carteraUsuario
    monedaBase = Currency(simulacionDTO.monedaBase.ticker)
    activos_classes = [a["clase"] for a in activos]
    for activo_cartera in cartera.listaActivoCartera:
        activo_cartera: ActivoCarteraDTO
        if activo_cartera.ticker == monedaBase.name:
            cantidades[monedaBase] = int(activo_cartera.cantidad)
            continue

        asset = Asset(activo_cartera.ticker, bool(activo_cartera.es_entero))
        if asset not in activos_classes:
            activoCartera = Activo_Cartera.objects.filter(id=activo_cartera.id)[0] # Solo tiene un activo
            activos.append(
                {
                    "id": activoCartera.activo_id,
                    "nombre": activo_cartera.ticker,
                    "clase": asset,
                }
            )
        cantidades[asset] = int(activo_cartera.cantidad)

    # Mapear moneda base
    wallet = Wallet(cantidades, monedaBase)

    # Mapear estrategias a AutomatedStrategy
    estrategias: list[AutomatedStrategy] = []
    for estrategiaDTO in simulacionDTO.estrategias:
        estrategias.append(mapear_estrategia_dto(estrategiaDTO, wallet))

    print(estrategias)
    granularidad_id = simulacionDTO.granularidad.id
    conjunto_de_precios = [
        Precio_Activo.objects.filter(
            activo_id=activo["id"], granularidad_id=granularidad_id
        )
        for activo in activos
        if activo["nombre"] != monedaBase.name
    ]

    conjunto_de_precios_definitivo = []
    for activo, precios in zip(
        [a for a in activos if a["nombre"] != monedaBase.name], conjunto_de_precios
    ):
        if len(precios) == 0:
            print("\n\n\n")
            print(f"[WARNING] No se encontraron precios para el activo {activo['nombre']}")
            print("\n\n\n")
            continue
        conjunto_de_precios_definitivo.append(precios)
    conjunto_de_precios = conjunto_de_precios_definitivo

    markets = {}
    for precios, activo in zip(conjunto_de_precios, activos):
        fechas_list = [pd.Timestamp(precio.fecha_hora) for precio in precios]
        precios_lista = [float(precio.precio_cierre) for precio in precios]
        df = pd.DataFrame(precios_lista, index=fechas_list, columns=["Close"])
        markets[activo["clase"]] = df

    stock_market_handler = StockMarketHandler(markets)
    simulation = OnlineSimulation(
        stock_market_handler=stock_market_handler, strategies=estrategias, wallet=wallet
    )
    simulation.run_simulation()

    transacciones_json_list: list[dict] = []
    for wallet_update in simulation.history:
        # {
        #     "transaccion": transacciones_json_list[
        #         wallet_update.transaction_dto.transaction_type
        #     ],
        #     "activo": wallet_update.transaction_dto.asset.name,
        #     "cantidad": wallet_update.transaction_dto.asset_amount,
        #     "fecha": str(wallet_update.transaction_dto.transaction_date),
        #     "saldo cartera": wallet_update.balance.tolist(),
        # }
        activo_dict = encontrar_activo_dado_su_ticker(
            wallet_update.transaction_dto.asset.name, activos
        )
        transacciones_json_list.append(
            {
                "activo_id": activo_dict["id"],
                "fecha": str(wallet_update.transaction_dto.transaction_date),
                "precio": wallet_update.transaction_dto.asset_price.tolist(),
                "cantidad": wallet_update.transaction_dto.asset_amount,
                "tipo_transaccion_nombre": transaction_type_str_map[
                    wallet_update.transaction_dto.transaction_type
                ],
            }
        )

    return transacciones_json_list
