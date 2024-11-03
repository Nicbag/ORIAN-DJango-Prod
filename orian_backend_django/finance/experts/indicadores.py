from typing import Callable

import pandas as pd
from ta.volume import (
    MFIIndicator,
    AccDistIndexIndicator,
    OnBalanceVolumeIndicator,
    ChaikinMoneyFlowIndicator,
    EaseOfMovementIndicator,
)
from ta.volatility import (
    BollingerBands,
    AverageTrueRange,
    KeltnerChannel,
    DonchianChannel,
    UlcerIndex,
)
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator, IchimokuIndicator
from ta.momentum import (
    RSIIndicator,
    StochRSIIndicator,
    TSIIndicator,
    UltimateOscillator,
    AwesomeOscillatorIndicator,
)


def convert_series_to_list_of_dicts(series) -> list[dict]:
    series = series.dropna()
    times = list(map(str, series.index.tolist()))
    values = series.values.tolist()
    values_list = []
    for time, val in zip(times, values):
        values_list.append({"tiempo": time, "valor": val}) 
    return values_list


def map_indicadores(df: pd.DataFrame, nombre_indicador: str, param_indicador: dict) -> Callable:
    #
    # INDICADORES DE VOLATILIDAD
    #

    ##
    ##  BANDAS DE BOLLINGER
    ##
    if nombre_indicador == "Bandas Bollinger":
        ventana = int(param_indicador["ventana"])
        bb = BollingerBands(close=df["Close"], window=ventana, window_dev=2)
        return {
            "tipo": "lineas",
            "datos": [
                {
                    "nombre": "Banda superior",
                    "valores": convert_series_to_list_of_dicts(bb.bollinger_hband())
                 },
                {
                    "nombre": "Banda inferior",
                    "valores": convert_series_to_list_of_dicts(bb.bollinger_lband())
                 },
                 {
                    "nombre": "Media Móvil",
                    "valores": convert_series_to_list_of_dicts(bb.bollinger_mavg())
                 }
            ]
        }
    
    ##
    ##  RANGO VERDADERO PROMEDIO
    ##
    elif nombre_indicador == "Rango verdadero promedio":
        ventana = int(param_indicador["ventana"])
        atr = AverageTrueRange(high=df["High"], low=df["Low"], close=df["Close"], window=ventana)
        return {
            "tipo": "lineas",
            "datos": [
                {
                    "nombre": "ATR",
                    "valores": convert_series_to_list_of_dicts(atr.average_true_range())
                 }
            ]
        }

    #
    # INDICADORES DE TENDENCIA
    #

    ##
    ##  SMA
    ##
    elif nombre_indicador == "SMA":
        ventana = int(param_indicador["ventana"])
        sma = SMAIndicator(close=df["Close"], window=ventana)
        return {
            "tipo": "lineas",
            "datos": [
                {
                    "nombre": "SMA",
                    "valores": convert_series_to_list_of_dicts(sma.sma_indicator())
                 }
            ]
        }
    
    ##
    ## EMA
    ##
    elif nombre_indicador == "EMA":
        ventana = int(param_indicador["ventana"])
        ema = EMAIndicator(close=df["Close"], window=ventana)
        return {
            "tipo": "lineas",
            "datos": [
                {
                    "nombre": "EMA",
                    "valores": convert_series_to_list_of_dicts(ema.ema_indicator())
                 }
            ]
        }
    
    else:
        raise ValueError(f"Indicador {nombre_indicador} no encontrado. Por favor, verifique el nombre del indicador.")    