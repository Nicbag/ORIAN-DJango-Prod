from django.http import JsonResponse
from django.views import View
import yfinance as yf
import requests

# from binance.client import Client
import json, datetime, os
from finance.experts.information import getStockInformation
from django.views.decorators.csrf import csrf_exempt
from decouple import config

# Cargar la clave de la API desde la variable de entorno
api_key_poligon = config('API_KEY_POLYGON')
api_key_alpha = config('API_KEY_ALPHA')

class StockNews(View):
    def get(self, request, ticker, *args, **kwargs):
        try:
            url = f"https://api.polygon.io/v2/reference/news?ticker={ticker.upper().split('-')[0]}&limit=10&apiKey={api_key_poligon}"

            response = requests.get(url)
            data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Network error: " + str(e)}, status=500)
        except ValueError:
            return JsonResponse(
                {"error": "Error processing the API response"}, status=500
            )
        except Exception as e:
            return JsonResponse(
                {"error": "An unexpected error occurred: " + str(e)}, status=500
            )
        return JsonResponse(data)


class StockInformation(View):
    def get(self, request, ticker, *args, **kwargs):

        try:
            infoDTO = getStockInformation(
                ticker.upper(),
                api_key_alpha,
                api_key_poligon,
            )
            print(infoDTO.to_dict())
            return JsonResponse(infoDTO.to_dict())

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "An unexpected error occurred: " + str(e)}, status=500
            )


class StockHistory(View):
    def get(self, request, ticker, period="", interval="", *args, **kwargs):
        try:
            stock_data = yf.Ticker(ticker)

            if interval == "0":
                history = stock_data.history(period=period)
            else:
                history = stock_data.history(period=period, interval=interval)

            if history.empty:
                raise ValueError("No historical data found for the ticker.")

            # Convertir las fechas del índice a un formato que mantenga la fecha y la hora
            history.index = history.index.strftime("%Y-%m-%d %H:%M:%S")

        except (ValueError, yf.YFNetworkError, yf.YFResponseError) as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "An unexpected error occurred: " + str(e)}, status=500
            )

        # Convertir el DataFrame a un formato JSON adecuado
        return JsonResponse(history.to_dict(orient="index"))


class CryptocurrencyInformation(View):
    def get(self, request, crypto, *args, **kwargs):
        url = f"https://api.coingecko.com/api/v3/coins/{crypto}"
        try:
            response = requests.get(url, headers={"User-Agent": "MyApp/1.0"})
            response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP 4xx/5xx
            data = response.json()
        except requests.exceptions.RequestException as e:
            # Manejo de errores de red
            return JsonResponse({"error": "Network error: " + str(e)}, status=500)
        except ValueError:
            # Manejo de errores al procesar la respuesta JSON
            return JsonResponse(
                {"error": "Error al procesar la respuesta de la API"}, status=500
            )
        except Exception as e:
            # Manejo de cualquier otro tipo de error inesperado
            return JsonResponse(
                {"error": "An unexpected error occurred: " + str(e)}, status=500
            )

        return JsonResponse(data)


api_secret = config('API_SECRET')
api_key = config('API_KEY')
from binance.client import Client

class CryptocurrencyHistory(View):
    def get(self, request, crypto, *args, **kwargs):

        try:
            # Configura tu cliente Binance (necesitas tu API key y secret aquí)
            client = Client(api_key=api_key, api_secret=api_secret)

            # Asegúrate de que el símbolo sea válido (mayúsculas, sin caracteres ilegales)
            crypto = crypto.upper()  # Convierte el símbolo a mayúsculas
            # Define el rango de fechas para los últimos tres meses
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(
                days=90
            )  # Aproximadamente tres meses

            # Consulta a la API de Binance para obtener datos históricos de velas
            klines = client.get_historical_klines(
                crypto,
                Client.KLINE_INTERVAL_1DAY,
                start_date.strftime("%d %b, %Y"),
                end_date.strftime("%d %b, %Y"),
            )

            if not klines:
                raise ValueError("No historical data found for the cryptocurrency.")

            # Procesar datos para obtener precios de apertura, cierre, máximo, mínimo y volumen
            history = {}
            for kline in klines:
                timestamp = int(kline[0]) / 1000
                date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                history[date] = {
                    "open": float(kline[1]),
                    "high": float(kline[2]),
                    "low": float(kline[3]),
                    "close": float(kline[4]),
                    "volume": float(kline[5]),
                }

        except (ValueError, Exception) as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "An unexpected error occurred: " + str(e)}, status=500
            )

        return JsonResponse(history)


from django.utils.decorators import method_decorator


class TranslateInformation(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body.decode("utf-8"))
            text = body.get("text")

            if not text:
                return JsonResponse({"error": "Text field is required."}, status=400)

            url = "https://api.mymemory.translated.net/get"
            params = {"q": text, "langpair": "en|es"}
            response = requests.get(url, params=params)

            data = response.json()
            print(data)
            return JsonResponse(data.get("responseData", {}))

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Network error: " + str(e)}, status=500)


from finance.models import (
    Transaccion,
    Activo,
    Tipo_Transaccion,
    Cartera_Usuario,
    Historico_Cartera_Usuario,
)
from finance.experts.simulacionDTO.simulacionDTO import (
    SimulacionDTO,
    GranularidadDTO,
    CarteraDTO,
    ActivoDTO,
    EstrategiaAutomatizadaDTO,
    EstrategiaTransaccionDTO,
    TipoEstrategiaTransaccionDTO,
    ParametroDTO,
    ActivoCarteraDTO,
)
from finance.orian_simulation.simulation_mappings import mapear_simulacion_dto
from django.views.decorators.csrf import csrf_exempt


class SimulacionAutomatizada(View):
    # @csrf_exempt
    def post(self, request, *args, **kwargs):

        try:
            # Lee el body de la solicitud y lo convierte a un diccionario de Python
            body = json.loads(request.body.decode("utf-8"))

            #! HERE!!!
            simulacion_dto = SimulacionDTO()
            simulacion_dto.id = body.get("id")
            simulacion_dto.nombre = body.get("nombre")
            simulacion_dto.fechaDesde = body.get("fechaDesde")
            simulacion_dto.fechaHasta = body.get("fechaHasta")

            simulacion_dto.granularidad = (
                GranularidadDTO()
            )  # Crear instancia de GranularidadDTO
            simulacion_dto._granularidad.id = body.get("granularidadTiempo", {}).get(
                "id"
            )
            simulacion_dto._granularidad.nombre = body.get(
                "granularidadTiempo", {}
            ).get("nombre")

            simulacion_dto.carteraUsuario = (
                CarteraDTO()
            )  # Crear instancia de CarteraDTO
            simulacion_dto.carteraUsuario.id = body.get("carteraUsuario", {}).get(
                "id"
            )
            simulacion_dto.carteraUsuario.nombre = body.get("carteraUsuario", {}).get(
                "nombre"
            )
            listaActivoCartera = body.get("carteraUsuario", {}).get(
                "listaActivoCartera", {}
            )
            listaActivoCarteraDTO = []
            for activoCartera in listaActivoCartera:
                activoCarteraDTO = ActivoCarteraDTO()
                activoCarteraDTO.id = activoCartera.get("id")
                activoCarteraDTO.es_entero = activoCartera.get("esEntero")
                activoCarteraDTO.ticker = activoCartera.get("ticker")
                activoCarteraDTO.cantidad = activoCartera.get("cantidad")
                listaActivoCarteraDTO.append(activoCarteraDTO)
            simulacion_dto._carteraUsuario.listaActivoCartera = listaActivoCarteraDTO

            simulacion_dto._monedaBase = ActivoDTO()  # Crear instancia de ActivoDTO
            simulacion_dto._monedaBase.id = body.get("monedaBase", {}).get("id")
            simulacion_dto._monedaBase.es_entero = "FALSO"
            simulacion_dto._monedaBase.ticker = body.get("monedaBase", {}).get(
                "ticker"
            )

            estrategiasAutomatizadas = body.get("estrategiasAutomatizadas", {})
            estrategiasAutomatizadasDTO = []
            for estrategiaAutomatizada in estrategiasAutomatizadas:
                estrategiaAutomatizadaDTO = EstrategiaAutomatizadaDTO()
                estrategiaAutomatizadaDTO.id = estrategiaAutomatizada.get("id")
                estrategiaAutomatizadaDTO.nombre = estrategiaAutomatizada.get("nombre")
                estrategiaAutomatizadaDTO.prioridad = estrategiaAutomatizada.get(
                    "prioridad"
                )
                activo = estrategiaAutomatizada.get("activo", {})
                activoDTO = ActivoDTO()
                activoDTO.id = activo.get("id")
                activoDTO.ticker = activo.get("ticker")
                estrategiaAutomatizadaDTO.activo = activoDTO

                disparadorTransaccionCompra = estrategiaAutomatizada.get(
                    "disparadorTransaccionCompra", {}
                )
                disparadorTransaccionCompraDTO = EstrategiaTransaccionDTO()
                disparadorTransaccionCompraDTO.id = disparadorTransaccionCompra.get(
                    "id"
                )
                disparadorTransaccionCompraDTO.nombre = (
                    disparadorTransaccionCompra.get("nombre")
                )
                tipo_estrategia_transaccion = disparadorTransaccionCompra.get(
                    "tipoEstrategiaTransaccion", {}
                )
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO.id = tipo_estrategia_transaccion.get(
                    "id"
                )
                tipo_estrategia_transaccionDTO.nombre = (
                    tipo_estrategia_transaccion.get("nombre")
                )
                disparadorTransaccionCompraDTO.tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO

                parametro = disparadorTransaccionCompra.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO.id = parametro.get("id")
                    parametroDTO.nombre = parametro.get("nombre")
                    parametroDTO.valor = parametro.get("valorParametro")
                    parametrosDTO.append(parametroDTO)
                disparadorTransaccionCompraDTO.parametros = parametrosDTO
                estrategiaAutomatizadaDTO.disparadorTransaccionCompra = disparadorTransaccionCompraDTO

                adminCantidadTransaccionVenta = estrategiaAutomatizada.get(
                    "adminCantidadTransaccionVenta", {}
                )
                adminCantidadTransaccionVentaDTO = EstrategiaTransaccionDTO()
                adminCantidadTransaccionVentaDTO.id = (
                    adminCantidadTransaccionVenta.get("id")
                )
                adminCantidadTransaccionVentaDTO.nombre = (
                    adminCantidadTransaccionVenta.get("nombre")
                )
                tipo_estrategia_transaccion = adminCantidadTransaccionVenta.get(
                    "tipoEstrategiaTransaccion", {}
                )
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO.id = tipo_estrategia_transaccion.get(
                    "id"
                )
                tipo_estrategia_transaccionDTO.nombre = (
                    tipo_estrategia_transaccion.get("nombre")
                )
                adminCantidadTransaccionVentaDTO.tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO


                parametro = adminCantidadTransaccionVenta.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO.id = parametro.get("id")
                    parametroDTO.nombre = parametro.get("nombre")
                    parametroDTO.valor = parametro.get("valorParametro")
                    parametrosDTO.append(parametroDTO)
                adminCantidadTransaccionVentaDTO.parametros = parametrosDTO
                estrategiaAutomatizadaDTO.adminCantidadTransaccionVenta = adminCantidadTransaccionVentaDTO

                adminCantidadTransaccionCompra = estrategiaAutomatizada.get(
                    "adminCantidadTransaccionCompra", {}
                )
                adminCantidadTransaccionCompraDTO = EstrategiaTransaccionDTO()
                adminCantidadTransaccionCompraDTO.id = (
                    adminCantidadTransaccionCompra.get("id")
                )
                adminCantidadTransaccionCompraDTO.nombre = (
                    adminCantidadTransaccionCompra.get("nombre")
                )
                tipo_estrategia_transaccion = adminCantidadTransaccionCompra.get(
                    "tipoEstrategiaTransaccion", {}
                )
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO.id = tipo_estrategia_transaccion.get(
                    "id"
                )
                tipo_estrategia_transaccionDTO.nombre = (
                    tipo_estrategia_transaccion.get("nombre")
                )
                adminCantidadTransaccionCompraDTO.tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO

                parametro = adminCantidadTransaccionCompra.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO.id = parametro.get("id")
                    parametroDTO.nombre = parametro.get("nombre")
                    parametroDTO.valor = parametro.get("valorParametro")
                    parametrosDTO.append(parametroDTO)
                adminCantidadTransaccionCompraDTO.parametros = parametrosDTO
                estrategiaAutomatizadaDTO.adminCantidadTransaccionCompra = adminCantidadTransaccionCompraDTO
                

                disparadorTransaccionVenta = estrategiaAutomatizada.get(
                    "disparadorTransaccionVenta", {}
                )
                disparadorTransaccionVentaDTO = EstrategiaTransaccionDTO()
                disparadorTransaccionVentaDTO.id = disparadorTransaccionVenta.get("id")
                disparadorTransaccionVentaDTO.nombre = disparadorTransaccionVenta.get(
                    "nombre"
                )
                tipo_estrategia_transaccion = disparadorTransaccionVenta.get(
                    "tipoEstrategiaTransaccion", {}
                )
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO.id = tipo_estrategia_transaccion.get(
                    "id"
                )
                tipo_estrategia_transaccionDTO.nombre = (
                    tipo_estrategia_transaccion.get("nombre")
                )
                disparadorTransaccionVentaDTO.tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO

                parametro = disparadorTransaccionVenta.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO.id = parametro.get("id")
                    parametroDTO.nombre = parametro.get("nombre")
                    parametroDTO.valor = parametro.get("valorParametro")
                    parametrosDTO.append(parametroDTO)
                disparadorTransaccionVentaDTO.parametros = parametrosDTO
                estrategiaAutomatizadaDTO.disparadorTransaccionVenta = disparadorTransaccionVentaDTO

                algoritmoTrading = estrategiaAutomatizada.get("algoritmoTrading", {})
                algoritmoTradingDTO = EstrategiaTransaccionDTO()
                algoritmoTradingDTO.id = algoritmoTrading.get("id")
                algoritmoTradingDTO.nombre = algoritmoTrading.get("nombre")
                tipo_estrategia_transaccion = algoritmoTrading.get(
                    "tipoEstrategiaTransaccion", {}
                )
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO.id = tipo_estrategia_transaccion.get(
                    "id"
                )
                tipo_estrategia_transaccionDTO._nombre = (
                    tipo_estrategia_transaccion.get("nombre")
                )
                algoritmoTradingDTO.tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO

                parametro = algoritmoTrading.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO.id = parametro.get("id")
                    parametroDTO.nombre = parametro.get("nombre")
                    parametroDTO.valor = parametro.get("valorParametro")
                    parametrosDTO.append(parametroDTO)
                algoritmoTradingDTO.parametros = parametrosDTO
                estrategiaAutomatizadaDTO.algoritmoTrading = algoritmoTradingDTO

                estrategiasAutomatizadasDTO.append(estrategiaAutomatizadaDTO)

            print("hola",estrategiasAutomatizadasDTO)
            simulacion_dto.estrategias = estrategiasAutomatizadasDTO

            print(simulacion_dto)
            #! Here -> SimulacionDTO

            transacciones_json_list = mapear_simulacion_dto(simulacion_dto)

            # ACA ESTÁ CIRO. Esta variable es un diccionario de python pero se lo puede
            # convertir a json facil con "json.dumps(transacciones_json_list)"

            #! Transacciones
            cartera_usuario_id = body.get("carteraUsuario", {}).get("id")
            #transacciones = list(Transaccion.objects.filter(cartera_usuario=cartera_usuario_id).values())
            transacciones = transacciones_json_list
            transaccionesDTO = []
            for transaccion in transacciones:
                activo_id = transaccion["activo_id"]
                activo = Activo.objects.get(id=activo_id)

                tipo_transaccion_nombre = transaccion["tipo_transaccion_nombre"]
                tipo_transaccion = Tipo_Transaccion.objects.get(
                    nombre=tipo_transaccion_nombre
                )

                cartera_usuario_id = simulacion_dto._carteraUsuario._id
                cartera_usuario = Cartera_Usuario.objects.get(id=cartera_usuario_id)

                activo_dto = {"id": activo.id, "nombre": activo.nombre}
                tipo_transaccion_dto = {
                    "id": tipo_transaccion.id,
                    "nombre": tipo_transaccion.nombre,
                }
                cartera_usuario_dto = {
                    "id": cartera_usuario.id,
                    "nombre": cartera_usuario.nombre,
                }

                transaccionDTO = {
                    "id": None,
                    "cantidad": transaccion["cantidad"],
                    "precio": transaccion["precio"],
                    "fecha": transaccion["fecha"],
                    "tipoTransaccion": tipo_transaccion_dto,
                    "carteraUsuarioId": cartera_usuario_id,
                    "activo": activo_dto,
                }
                transaccionesDTO.append(transaccionDTO)
            print(transaccionesDTO)

            resultado = {
                "transacciones": transaccionesDTO
            }
            
            rpta = JsonResponse(resultado, safe=False)

            print(rpta)
            return rpta

        except Exception as e:
            print("ERROR:", e)
            raise e
            return JsonResponse({"error": str(e)}, status=400)
        

from finance.experts.indicadores import map_indicadores
from finance.models import Precio_Activo
import pandas as pd

class Indicadores(View):
    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode("utf-8"))
        nombre = body["nombre"]
        parametros = body["parametros"]
        activo_id = body["activo_id"]
        granularidad_id = body["granularidad_id"]
        
        # Obtener precios del activo
        precios = Precio_Activo.objects.filter(
            activo_id=activo_id, granularidad_id=granularidad_id
        )
        fechas_list = [pd.Timestamp(precio.fecha_hora) for precio in precios]
        precios_cierre_list = [float(precio.precio_cierre) for precio in precios]
        precios_apertura_list = [float(precio.precio_apertura) for precio in precios]
        precios_max_list = [float(precio.precio_max) for precio in precios]
        precios_min_list = [float(precio.precio_min) for precio in precios]
        volumen_list = [float(precio.volumen) for precio in precios]
    
        df = pd.DataFrame(
                {
                    "Close": precios_cierre_list,
                    "Open": precios_apertura_list,
                    "High": precios_max_list,
                    "Low": precios_min_list,
                    "Volume": volumen_list,
                },
                index=fechas_list,)
        
        return JsonResponse(map_indicadores(df, nombre, parametros))
