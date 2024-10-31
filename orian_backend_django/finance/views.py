from django.http import JsonResponse
from django.views import View
import yfinance as yf
import requests
from binance.client import Client
import json, datetime, os
from finance.experts.information import getStockInformation
from django.views.decorators.csrf import csrf_exempt

class StockNews(View):
    def get(self, request, ticker, *args, **kwargs):

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        secret_file_path = os.path.join(base_dir, 'finance', 'secret.json')

        try:
            with open(secret_file_path, 'r') as file:
                secrets = json.load(file)

            api_key_poligon = secrets.get('api_key_poligon')

            url = f"https://api.polygon.io/v2/reference/news?ticker={ticker.upper().split('-')[0]}&limit=10&apiKey={api_key_poligon}"

            response = requests.get(url)
            data = response.json()

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Network error: ' + str(e)}, status=500)
        except ValueError:
            return JsonResponse({'error': 'Error processing the API response'}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
        return JsonResponse(data)

class StockInformation(View):
    def get(self, request, ticker, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        secret_file_path = os.path.join(base_dir, 'finance', 'secret.json')

        with open(secret_file_path, 'r') as file:
            secrets = json.load(file)

        try:
            infoDTO = getStockInformation(ticker.upper(), secrets.get('api_key_alpha'), secrets.get('api_key_poligon'))
            print(infoDTO.to_dict())
            return JsonResponse(infoDTO.to_dict())

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


class StockHistory(View):
    def get(self, request, ticker, period='', interval="",*args, **kwargs):        
        try:
            stock_data = yf.Ticker(ticker)

            if (interval == "0"):
                history = stock_data.history(period=period)
            else:
                history = stock_data.history(period=period, interval=interval)

            if history.empty:
                raise ValueError("No historical data found for the ticker.")
            
            # Convertir las fechas del índice a un formato que mantenga la fecha y la hora
            history.index = history.index.strftime('%Y-%m-%d %H:%M:%S')

        except (ValueError, yf.YFNetworkError, yf.YFResponseError) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

        # Convertir el DataFrame a un formato JSON adecuado
        return JsonResponse(history.to_dict(orient="index"))


class CryptocurrencyInformation(View):
    def get(self, request, crypto, *args, **kwargs):
        url = f'https://api.coingecko.com/api/v3/coins/{crypto}'
        try:
            response = requests.get(url, headers={'User-Agent': 'MyApp/1.0'})
            response.raise_for_status()  # Lanza una excepción para códigos de estado HTTP 4xx/5xx
            data = response.json()
        except requests.exceptions.RequestException as e:
            # Manejo de errores de red
            return JsonResponse({'error': 'Network error: ' + str(e)}, status=500)
        except ValueError:
            # Manejo de errores al procesar la respuesta JSON
            return JsonResponse({'error': 'Error al procesar la respuesta de la API'}, status=500)
        except Exception as e:
            # Manejo de cualquier otro tipo de error inesperado
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
        
        return JsonResponse(data)
    
   
class CryptocurrencyHistory(View):    
    def get(self, request, crypto, *args, **kwargs):
        with open('/home/ciro/Documentos/Back/orian-backend-django/secret.json', 'r') as file:
            secrets = json.load(file)
        api_key= secrets.get('api_key')
        api_secret = secrets.get('api_secret')

        try:
            # Configura tu cliente Binance (necesitas tu API key y secret aquí)
            client = Client(api_key=api_key, api_secret=api_secret)

            # Asegúrate de que el símbolo sea válido (mayúsculas, sin caracteres ilegales)
            crypto = crypto.upper()  # Convierte el símbolo a mayúsculas
            # Define el rango de fechas para los últimos tres meses
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days=90)  # Aproximadamente tres meses

            # Consulta a la API de Binance para obtener datos históricos de velas
            klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1DAY, start_date.strftime('%d %b, %Y'), end_date.strftime('%d %b, %Y'))

            if not klines:
                raise ValueError("No historical data found for the cryptocurrency.")

            # Procesar datos para obtener precios de apertura, cierre, máximo, mínimo y volumen
            history = {}
            for kline in klines:
                timestamp = int(kline[0]) / 1000
                date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                history[date] = {
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5])
                }

        except (ValueError, Exception) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

        return JsonResponse(history)
    
from django.utils.decorators import method_decorator
class TranslateInformation(View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body.decode('utf-8'))
            text = body.get('text')

            if not text:
                return JsonResponse({'error': 'Text field is required.'}, status=400)

            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": "en|es"
            }
            response = requests.get(url, params=params)

            data = response.json()
            print(data)
            return JsonResponse(data.get('responseData', {}))

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Network error: ' + str(e)}, status=500)


from finance.models import Transaccion, Activo, Tipo_Transaccion, Cartera_Usuario, Historico_Cartera_Usuario
from finance.experts.simulacionDTO.simulacionDTO import SimulacionDTO, GranularidadDTO, CarteraDTO, ActivoDTO, EstrategiaAutomatizadaDTO, EstrategiaTransaccionDTO, TipoEstrategiaTransaccionDTO, ParametroDTO, ActivoCarteraDTO

class SimulacionAutomatizada(View):
    def post(self, request, *args, **kwargs):
        try:
            # Lee el body de la solicitud y lo convierte a un diccionario de Python
            body = json.loads(request.body.decode('utf-8'))

            #! HERE!!!
            simulacion_dto = SimulacionDTO()
            simulacion_dto._id = body.get("id") 
            simulacion_dto._nombre = body.get("nombre")
            simulacion_dto._fechaDesde = body.get("fechaDesde")
            simulacion_dto._fechaHasta = body.get("fechaHasta")

            simulacion_dto._granularidad = GranularidadDTO()  # Crear instancia de GranularidadDTO
            simulacion_dto._granularidad._id = body.get("granularidadTiempo", {}).get("id")
            simulacion_dto._granularidad._nombre = body.get("granularidadTiempo", {}).get("nombre")

            simulacion_dto._carteraUsuario = CarteraDTO()  # Crear instancia de CarteraDTO
            simulacion_dto._carteraUsuario._id = body.get("carteraUsuario", {}).get("id")
            simulacion_dto._carteraUsuario._nombre = body.get("carteraUsuario", {}).get("nombre")

            listaActivoCartera = body.get("carteraUsuario", {}).get("listaActivoCartera", {})
            listaActivoCarteraDTO = []
            for activoCartera in listaActivoCartera:
                activoCarteraDTO = ActivoCarteraDTO()
                activoCarteraDTO._id = activoCartera.get("id")
                activoCarteraDTO._ticker = activoCartera.get("ticker")
                listaActivoCarteraDTO.append(activoCarteraDTO)
            simulacion_dto._carteraUsuario._listaActivoCartera = listaActivoCarteraDTO
            
            simulacion_dto._monedaBase = ActivoDTO()  # Crear instancia de ActivoDTO
            simulacion_dto._monedaBase._id = body.get("monedaBase", {}).get("id")
            simulacion_dto._monedaBase._nombre = body.get("monedaBase", {}).get("nombre")

            estrategiasAutomatizadas = body.get("estrategiasAutomatizadas", {})
            estrategiasAutomatizadasDTO = []
            for estrategiaAutomatizada in estrategiasAutomatizadas:
                estrategiaAutomatizadaDTO = EstrategiaAutomatizadaDTO()
                estrategiaAutomatizadaDTO._id = estrategiaAutomatizada.get("id")
                estrategiaAutomatizadaDTO._nombre = estrategiaAutomatizada.get("nombre")
                estrategiaAutomatizadaDTO._prioridad = estrategiaAutomatizada.get("prioridad")
                activo = estrategiaAutomatizada.get("activo", {})
                activoDTO = ActivoDTO()
                activoDTO._id = activo.get("id")
                activoDTO._ticker = activo.get("ticker")
                estrategiaAutomatizadaDTO._activo = activoDTO

                disparadorTransaccionCompra = estrategiaAutomatizada.get("disparadorTransaccionCompra", {})
                disparadorTransaccionCompraDTO = EstrategiaTransaccionDTO()
                disparadorTransaccionCompraDTO._id = disparadorTransaccionCompra.get("id")
                disparadorTransaccionCompraDTO._nombre = disparadorTransaccionCompra.get("nombre")
                tipo_estrategia_transaccion = disparadorTransaccionCompra.get("tipoEstrategiaTransaccion", {})
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO._id = tipo_estrategia_transaccion.get("id")
                tipo_estrategia_transaccionDTO._nombre = tipo_estrategia_transaccion.get("nombre")
                disparadorTransaccionCompraDTO._tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO
                parametro = disparadorTransaccionCompra.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO._id = parametro.get("id")
                    parametroDTO._nombre = parametro.get("nombre")
                    parametroDTO._valor = parametro.get("valor")
                    parametrosDTO.append(parametroDTO)
                disparadorTransaccionCompraDTO._parametros = parametrosDTO
                estrategiaAutomatizadaDTO._disparadorTransaccionCompra = disparadorTransaccionCompraDTO

                adminCantidadTransaccionVenta = estrategiaAutomatizada.get("adminCantidadTransaccionVenta", {})
                adminCantidadTransaccionVentaDTO = EstrategiaTransaccionDTO()
                adminCantidadTransaccionVentaDTO._id = adminCantidadTransaccionVenta.get("id")
                adminCantidadTransaccionVentaDTO._nombre = adminCantidadTransaccionVenta.get("nombre")
                tipo_estrategia_transaccion = adminCantidadTransaccionVenta.get("tipoEstrategiaTransaccion", {})
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO._id = tipo_estrategia_transaccion.get("id")
                tipo_estrategia_transaccionDTO._nombre = tipo_estrategia_transaccion.get("nombre")
                disparadorTransaccionCompraDTO._tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO
                parametro = adminCantidadTransaccionVenta.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO._id = parametro.get("id")
                    parametroDTO._nombre = parametro.get("nombre")
                    parametroDTO._valor = parametro.get("valor")
                    parametrosDTO.append(parametroDTO)
                adminCantidadTransaccionVentaDTO._parametros = parametrosDTO
                estrategiaAutomatizadaDTO.adminCantidadTransaccionVenta = adminCantidadTransaccionVentaDTO

                adminCantidadTransaccionCompra = estrategiaAutomatizada.get("adminCantidadTransaccionCompra", {})
                adminCantidadTransaccionCompraDTO = EstrategiaTransaccionDTO()
                adminCantidadTransaccionCompraDTO._id = adminCantidadTransaccionCompra.get("id")
                adminCantidadTransaccionCompraDTO._nombre = adminCantidadTransaccionCompra.get("nombre")
                tipo_estrategia_transaccion = adminCantidadTransaccionCompra.get("tipoEstrategiaTransaccion", {})
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO._id = tipo_estrategia_transaccion.get("id")
                tipo_estrategia_transaccionDTO._nombre = tipo_estrategia_transaccion.get("nombre")
                disparadorTransaccionCompraDTO._tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO
                parametro = adminCantidadTransaccionCompra.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO._id = parametro.get("id")
                    parametroDTO._nombre = parametro.get("nombre")
                    parametroDTO._valor = parametro.get("valor")
                    parametrosDTO.append(parametroDTO)
                adminCantidadTransaccionCompraDTO._parametros = parametrosDTO
                estrategiaAutomatizadaDTO._adminCantidadTransaccionCompra = adminCantidadTransaccionCompraDTO

                disparadorTransaccionVenta = estrategiaAutomatizada.get("disparadorTransaccionVenta", {})
                disparadorTransaccionVentaDTO = EstrategiaTransaccionDTO()
                disparadorTransaccionVentaDTO._id = disparadorTransaccionVenta.get("id")
                disparadorTransaccionVentaDTO._nombre = disparadorTransaccionVenta.get("nombre")
                tipo_estrategia_transaccion = disparadorTransaccionVenta.get("tipoEstrategiaTransaccion", {})
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO._id = tipo_estrategia_transaccion.get("id")
                tipo_estrategia_transaccionDTO._nombre = tipo_estrategia_transaccion.get("nombre")
                disparadorTransaccionCompraDTO._tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO
                parametro = disparadorTransaccionVenta.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO._id = parametro.get("id")
                    parametroDTO._nombre = parametro.get("nombre")
                    parametroDTO._valor = parametro.get("valor")
                    parametrosDTO.append(parametroDTO)
                disparadorTransaccionVentaDTO._parametros = parametrosDTO
                estrategiaAutomatizadaDTO._disparadorTransaccionVenta = disparadorTransaccionVentaDTO

                algoritmoTrading = estrategiaAutomatizada.get("algoritmoTrading", {})
                algoritmoTradingDTO = EstrategiaTransaccionDTO()
                algoritmoTradingDTO._id = algoritmoTrading.get("id")
                algoritmoTradingDTO._nombre = algoritmoTrading.get("nombre")
                tipo_estrategia_transaccion = algoritmoTrading.get("tipoEstrategiaTransaccion", {})
                tipo_estrategia_transaccionDTO = TipoEstrategiaTransaccionDTO()
                tipo_estrategia_transaccionDTO._id = tipo_estrategia_transaccion.get("id")
                tipo_estrategia_transaccionDTO._nombre = tipo_estrategia_transaccion.get("nombre")
                disparadorTransaccionCompraDTO._tipoEstrategiaTransaccion = tipo_estrategia_transaccionDTO
                parametro = algoritmoTrading.get("parametros", {})
                parametrosDTO = []
                for parametro in parametro:
                    parametroDTO = ParametroDTO()
                    parametroDTO._id = parametro.get("id")
                    parametroDTO._nombre = parametro.get("nombre")
                    parametroDTO._valor = parametro.get("valor")
                    parametrosDTO.append(parametroDTO)
                algoritmoTradingDTO._parametros = parametrosDTO
                estrategiaAutomatizadaDTO._algoritmoTrading = algoritmoTradingDTO

                estrategiasAutomatizadasDTO.append(estrategiaAutomatizadaDTO)

            simulacion_dto._estrategiasAutomatizadas = estrategiasAutomatizadasDTO

            #! Here -> SimulacionDTO

            #! Transacciones
            cartera_usuario_id = body.get("carteraUsuario", {}).get("id")
            transacciones = list(Transaccion.objects.filter(cartera_usuario=cartera_usuario_id).values())
            transaccionesDTO = []
            for transaccion in transacciones:
                activo_id = transaccion['activo_id']
                activo = Activo.objects.get(id=activo_id)

                tipo_transaccion_id = transaccion['tipo_transaccion_id']
                tipo_transaccion = Tipo_Transaccion.objects.get(id=tipo_transaccion_id)

                cartera_usuario_id = transaccion['cartera_usuario_id']
                cartera_usuario = Cartera_Usuario.objects.get(id=cartera_usuario_id)
                
                activo_dto = {
                    "id": activo.id,
                    "nombre": activo.nombre
                }
                tipo_transaccion_dto = {
                    "id": tipo_transaccion.id,
                    "nombre": tipo_transaccion.nombre
                }
                cartera_usuario_dto = {
                    "id": cartera_usuario.id,
                    "nombre": cartera_usuario.nombre
                }
                
                transaccionDTO = {
                    "id": transaccion['id'],
                    "cantidad": transaccion['cantidad'],
                    "precio": transaccion['precio'],
                    "fecha": transaccion['fecha'],
                    "tipoTransaccion": tipo_transaccion_dto,
                    "carteraUsuario": cartera_usuario_dto,
                    "activo": activo_dto
                }
                transaccionesDTO.append(transaccionDTO)

            #! Hisotorico Cartera Usuario
            cartera_usuario = Cartera_Usuario.objects.get(id=cartera_usuario_id)
            historicoCarteraUsuarios = list(Historico_Cartera_Usuario.objects.filter(cartera_usuario_id=cartera_usuario_id).values())

            historicoCarteraUsuariosDTO = []
            for historicoCarteraUsuario in historicoCarteraUsuarios:
                cartera_usuario_id = historicoCarteraUsuario['cartera_usuario_id']
                cartera_usuario = Cartera_Usuario.objects.get(id=cartera_usuario_id)

                cartera_usuario_dto = {
                    "id": cartera_usuario.id,
                    "nombre": cartera_usuario.nombre
                }
                
                historicoCarteraUsuarioDTO = {
                    "id": historicoCarteraUsuario['id'],
                    "valorTotal": historicoCarteraUsuario['valor_total'],
                    "carteraUsuario": cartera_usuario_dto
                }

                historicoCarteraUsuariosDTO.append(historicoCarteraUsuarioDTO)

            rpta = JsonResponse({
                "transacciones": transaccionesDTO,
                "historicoCarteraUsuarios": historicoCarteraUsuariosDTO
            })

            # Retorna la respuesta
            return rpta

        except (ValueError, Exception) as e:
            return JsonResponse({'error': str(e)}, status=400)

