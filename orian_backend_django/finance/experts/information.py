import requests
import json
import os
from django.http import JsonResponse
import yfinance as yf
from finance.experts.InfoDTO import InfoDTO
from finance.experts.EmpleadoDTO import EmpleadoDTO
from finance.experts.GananciaTrimestralDTO import GananciaTrimestralDTO

def getAlphaInfo(ticker, api_key):
    try:
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        return data

    except requests.exceptions.RequestException as e:
        raise ValueError('Network error: ' + str(e))

def getPoligonInfo(ticker, api_key):
    try:
        url = f'https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={api_key}'
        r = requests.get(url)
        data = r.json()
        return data

    except requests.exceptions.RequestException as e:
        raise ValueError('Network error: ' + str(e))
    
    
def getAlphaEarnings(ticker, api_key):
    try:
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()
        return data

    except requests.exceptions.RequestException as e:
        raise ValueError('Network error: ' + str(e))

def getYahooInfo(ticker):
    try:
        stock_data = yf.Ticker(ticker)
        info = stock_data.info
        return info

    except (ValueError, yf.YFNetworkError, yf.YFResponseError) as e:
        raise ValueError('Error fetching Yahoo Finance data: ' + str(e))

def getStockInformation(ticker, api_key_alpha, api_key_poligon):
    infoDTO = InfoDTO()

    try:
        infoYahoo = getYahooInfo(ticker)
        
        if not infoYahoo:
            raise ValueError("No information found for the ticker.")

        infoDTO.ticker = infoYahoo.get('symbol')
        if infoYahoo.get('country') is not None: infoDTO.pais = infoYahoo.get('country')
        if infoYahoo.get('website') is not None:
            infoDTO.sitioWeb = infoYahoo.get('website')
        else:
            infoDTO.sitioWeb = infoYahoo.get('coinMarketCapLink')
        if infoYahoo.get('industry') is not None:
            infoDTO.industria = infoYahoo.get('industry')
        if infoYahoo.get('sector') is not None:
            infoDTO.sector = infoYahoo.get('sector')
        if infoYahoo.get('longBusinessSummary') is not None:
            infoDTO.descripcion = infoYahoo.get('longBusinessSummary')
        else:
            infoDTO.descripcion = infoYahoo.get('description')
        if infoYahoo.get('fullTimeEmployees') is not None:
            infoDTO.totalEmpleados = infoYahoo.get('fullTimeEmployees')
        if infoYahoo.get('marketCap') is not None:
            infoDTO.capitalizacion = str(infoYahoo.get('marketCap'))

        company_officers = infoYahoo.get('companyOfficers')
        if isinstance(company_officers, list):
            empleados = []
            for officer in company_officers:
                nombre = officer.get('name', 'Sin nombre')
                puesto = officer.get('title', 'Sin puesto')
                edad = officer.get('age', None)
                empleado = EmpleadoDTO(nombre, puesto, edad)
                empleados.append(empleado)

            infoDTO.empleados = empleados  
            infoDTO.empleados = [empleado.to_dict() for empleado in infoDTO.empleados]

    except ValueError as e:
        raise e  

    try:
        infoAlpha = getAlphaInfo(ticker.upper().split('-')[0], api_key_alpha)
        
        if infoAlpha.get('MarketCapitalization') is not None:
            if infoDTO.capitalizacion == None : infoDTO.capitalizacion = infoAlpha.get('MarketCapitalization')
            infoDTO.divisa = infoAlpha.get('Currency')
            infoDTO.exchange = infoAlpha.get('Exchange')
            infoDTO.fechaDividendos = infoAlpha.get('DividendDate')
            infoDTO.exFechaDividendos = infoAlpha.get('ExDividendDate')
            if infoAlpha.get('exFechaDividendos') is None or infoAlpha.get('exFechaDividendos') == "" or infoAlpha.get('exFechaDividendos') == "None":
                infoDTO.exFechaDividendos = ""
            infoDTO.ultimoCuarto = infoAlpha.get('LatestQuarter')
        else:
            print("No se encontró información en Alpha Vantage")
            infoPoligon = getPoligonInfo(ticker.upper().split('-')[0], api_key_poligon)
            results = infoPoligon.get('results')

            if infoDTO.capitalizacion == None : infoDTO.capitalizacion = str(results.get('market_cap'))
            infoDTO.divisa = str(results.get('currency_name'))
            infoDTO.exchange = str(results.get('primary_exchange'))

    except ValueError as e:
        raise e  
    
    try:
        earnings = getAlphaEarnings(ticker, api_key_alpha)
        quarterly_earnings = earnings.get('quarterlyEarnings')
        if isinstance(quarterly_earnings, list):
            gananciaTrimestrales = []
            for quarter in quarterly_earnings:
                gananciaTrimestral = GananciaTrimestralDTO()
                gananciaTrimestral.fechaFinalFiscal = quarter.get('fiscalDateEnding')
                gananciaTrimestral.fechaReportada = quarter.get('reportedDate')
                gananciaTrimestral.gananciaReportada = quarter.get('reportedEPS')
                gananciaTrimestral.gananciaEstimada = quarter.get('estimatedEPS')
                gananciaTrimestral.sorpresaNeta = quarter.get('surprise')
                gananciaTrimestral.sorpresaPorcentaje = quarter.get('surprisePercentage')
                gananciaTrimestrales.append(gananciaTrimestral)

            infoDTO.gananciaTrimestrales = gananciaTrimestrales
            infoDTO.gananciaTrimestrales = [ganancia.to_dict() for ganancia in infoDTO.gananciaTrimestrales]

    except ValueError as e:
        raise e

    print(infoDTO.to_dict())
    return infoDTO
