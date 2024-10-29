from django.urls import path
from .views import StockInformation, StockHistory, CryptocurrencyInformation, CryptocurrencyHistory, StockNews, TranslateInformation, SimulacionAutomatizada

urlpatterns = [
    path('ticker/<str:ticker>/', StockInformation.as_view(), name='asset_information'),
    path('ticker/history/<str:ticker>/<str:period>/<str:interval>', StockHistory.as_view(), name='asset_history'),
    path('crypto/<str:crypto>/', CryptocurrencyInformation.as_view(), name='crypto_information'),
    path('crypto/history/<str:crypto>/', CryptocurrencyHistory.as_view(), name='crypto_history'),
    path('news/<str:ticker>/', StockNews.as_view(), name='stock_news'),
    path('translate/', TranslateInformation.as_view(), name='translate_information'),
    path('simulate/', SimulacionAutomatizada.as_view(), name='simulate')
]

