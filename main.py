# main.py

from api.kraken_api import Kraken_API
from models.dataset import Dataset
from models.graph import Grafico
from api.twitter_client import X_Conect
from models.openai import generar_comentario_openai


def main():
    # Inicializar la API de Kraken
    api = Kraken_API()
    df , pair = api.get_OHCL_data()
    
    if df.empty:
        print("No se pudieron obtener datos OHLC de Kraken API.")
        return
    else : 
        # Procesar los datos con Dataset
        data = Dataset(df)  # Crear un objeto Dataset con el DataFrame
        df_metrics = data.get_metrics()  # Calcular las métricas clave
        grafico = Grafico(df_metrics, pair)
        grafico.candlestick_with_volume()
        
        comentario = generar_comentario_openai(df_metrics)
        print(f"{comentario}")



   
if __name__ == "__main__":
    main()
