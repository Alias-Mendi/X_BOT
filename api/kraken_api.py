# api/kraken_api.py

import krakenex as k
import os
import pandas as pd
import numpy as np
from utils.symbol_mapping import ohlc_mapping  # Importar el diccionario de mapeo de símbolos
import dotenv


class Kraken_API:

    ''' Clase para interactuar con la API de Kraken '''
    
    def __init__(self):
        ''' Constructor de la clase para autenticación con Kraken API '''       
        for i in range(3):
            try:
                dotenv.load_dotenv()
                self.api_key = os.getenv('KRAKEN_KEY')
                self.api = k.API(key=self.api_key)
                print('Conexión exitosa a Kraken API')
                break
            except Exception as e:
                print(f'Error al conectarse a Kraken API, reintentándolo... Intento {i+1}: {e}')

    def get_OHCL_data(self):
        ''' Método para obtener datos OHLC de Kraken '''
        # pair = self.get_Kraken_map(pair) Disponible en la versión v2 
        pair = 'XBTUSD'
        interval = 1  # Intervalo de tiempo en minutos para los datos OHLC en segundos
        print(f"Obteniendo datos OHLC para el par {pair}...")
        query = self.api.query_public('OHLC', {'pair': pair, 'interval': interval})
        
        # Manejo de posibles errores en la consulta
        if 'error' in query and query['error']:
            print("Errores en la consulta a Kraken API:", query['error'])
            return pd.DataFrame()  # Retornar DataFrame vacío en caso de error

        pair_mapped = ohlc_mapping.get(pair, pair) 
        if pair_mapped not in query['result']:
            print(f"Par {pair_mapped} no encontrado en la respuesta de Kraken API.")
            return pd.DataFrame()

        df = pd.DataFrame(query['result'][pair_mapped], columns=[
            'date', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'
        ])  # Crear un DataFrame con los datos OHLC
        df['date'] = pd.to_datetime(df['date'], unit='s')  # Convertir la columna timestamp a formato datetime
        df['date'] = df['date'] + pd.Timedelta(hours=1)  # Sumar una hora a cada fila para corregir el desfase horario

        return df , pair

    def get_coins(self):
        
        ''' Metodo para obtener las 5 monedas con mayor capitalización de mercado en CoinMarketCap '''
        pass

    def get_Kraken_map(self, simbolo_cmc):
        ''' Método para obtener el símbolo de Kraken a partir del símbolo de CoinMarketCap obtenido en la funcion get_coins() '''
        pass
