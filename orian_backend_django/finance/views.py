from django.http import JsonResponse
from django.views import View
import yfinance as yf
import requests
from binance.client import Client
import json, datetime, os
from finance.experts.information import getStockInformation
from finance.experts.simulacionDTO.estrategiaDTO import EstrategiaDTO
from finance.experts.simulacionDTO.parametroDTO import ParametroDTO
from finance.experts.simulacionDTO.simulacionDTO import SimulacionDTO
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

class SimulacionAutomatizada(View):
    def post(self, request, *args, **kwargs):
        try:
            # Lee el body de la solicitud y lo convierte a un diccionario de Python
            data = json.loads(request.body)

            # Crea una instancia de EstrategiaDTO
            estrategia_dto = EstrategiaDTO()

            # Asigna los datos del cuerpo de la solicitud al DTO
            estrategia_dto._id = data.get('id', None)
            estrategia_dto.parametros = data.get('parametros', [])  # Esta es la lista de ParametroDTO

            print(data)

            return JsonResponse({"message": "Simulación procesada exitosamente"})

        except (ValueError, Exception) as e:
            return JsonResponse({'error': str(e)}, status=400)