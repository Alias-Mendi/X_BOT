### Clase Grafico
from utils.symbol_mapping import mapped_ohlc_reverse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import matplotlib.dates as mdates


class Grafico:
    """
    Clase que se encarga de generar gráficos para visualizar los datos financieros.
    Ofrece varios tipos de gráficos: gráficos de línea, gráficos de velas, y combinaciones con volumen.
    """

    def __init__(self, df, pair):
        """Constructor de la clase. Recibe un DataFrame con los datos financieros."""
        self.df = df
        self.pair = mapped_ohlc_reverse.get(pair, 'No mapeado')
    
    def last_n_days(self):
        """
        Calcula el número de días de datos en el DataFrame.
        """
        n = 90 # Número de días por defecto
        
        self.df = self.df.tail(n) # Seleccionar los últimos n días
      
    
    def lineplot(self):
        """
        Genera un gráfico de líneas con:
        - Precio de cierre
        - Media Móvil Simple (SMA)
        - Bandas de Bollinger
        """
        self.last_n_days()
        # Evita que el gráfico se muestre en la consola (para WSL)
        matplotlib.use('Agg')

        # Estilo visual para el gráfico - modo oscuro ajustado
        plt.style.use("dark_background")

        # Crear figura
        plt.figure(figsize=(24, 12))

        # Añadir líneas al gráfico con colores más brillantes
        sns.lineplot(x=self.df.date, y=self.df['close'], color='#82CAFA', label='Precio de cierre')  # Azul claro
        sns.lineplot(x=self.df.date, y=self.df.SMA, label='SMA', color='#FF6F61', linewidth=1, linestyle='--')  # Naranja claro, línea discontinua
        sns.lineplot(x=self.df.date, y=self.df.SMA_50, label='SMA 50', color='#FFD700', linewidth=1, linestyle='--')  # Amarillo, línea discontinua
        sns.lineplot(x=self.df.date, y=self.df.SMA_200, label='SMA 200', color='#FF69B4', linewidth=1, linestyle='--')  # Rosa, línea discontinua
        #sns.lineplot(x=self.df.Date, y=self.df.Banda_Superior, label='Bandas de Bollinger superior e inferior', color='#FFD700', linewidth=2)  # Amarillo # Disponible en la versión v2
        #sns.lineplot(x=self.df.Date, y=self.df.Banda_Inferior, color='#FFD700', linewidth=2)  # Amarillo # Disponible en la versión v2

        
        # Configurar etiquetas y leyenda
        plt.title(f'Evolución del precio de {self.pair} en Kraken', fontsize=20, color='white')
        plt.xlabel('')
        plt.ylabel('')
        plt.ylabel('Precio', color='white')
        plt.legend(facecolor='black', frameon=True, fontsize=12)
        plt.grid(True, color='grey')
        #plt.tight_layout()
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.savefig('grafico.png',dpi=200)

        # Cambiar el fondo a gris oscuro en lugar de negro puro
        plt.gca().set_facecolor('#2E2E2E')

        # En lugar de guardar, devolvemos la figura
        return plt.gcf()
    


    def candlestick_with_volume(self):
        # Asegurar que 'date' sea de tipo datetime y que esté como índice
        self.df.set_index('date', inplace=True)

        plt.style.use("dark_background")
        fig, axs = plt.subplots(2, figsize=(24, 12), gridspec_kw={'height_ratios': [3, 1]})

        # Dibujar las velas en el subplot 1 usando plot_date
        colors = ['#00FF7F' if close > open else '#FF6347' for open, close in zip(self.df['open'], self.df['close'])]
        axs[0].vlines(self.df.index, self.df['low'], self.df['high'], colors=colors, linewidth=1)  # Líneas verticales para mechas
        axs[0].vlines(self.df.index, self.df['open'], self.df['close'], colors=colors, linewidth=15)  # Líneas verticales para cuerpos

        # Añadir SMA y Bandas de Bollinger
        sns.lineplot(data=self.df, x=self.df.index, y='SMA', label='SMA', color='#FFA07A', linewidth=2, ax=axs[0])
        sns.lineplot(data=self.df, x=self.df.index, y='Banda_Superior', label='Banda de Bollinger Superior', color='#FFD700', linewidth=2, ax=axs[0])
        sns.lineplot(data=self.df, x=self.df.index, y='Banda_Inferior', label='Banda Inferior', color='#FFD700', linewidth=2, ax=axs[0])

        # Calcular el precio mínimo y máximo
        precio_minimo = self.df['low'].min()
        precio_maximo = self.df['high'].max()

        # Dibujar líneas horizontales para el precio mínimo y máximo
        axs[0].hlines(precio_minimo, xmin=self.df.index.min(), xmax=self.df.index.max(), colors='cyan', linestyles='dashed')
        axs[0].hlines(precio_maximo, xmin=self.df.index.min(), xmax=self.df.index.max(), colors='magenta', linestyles='dashed')

        # Mostrar el precio mínimo y máximo sobre las líneas horizontales
        axs[0].text(self.df.index[-1], precio_minimo, f'{precio_minimo:.2f}', color='cyan', ha='left', va='center', fontsize=10, backgroundcolor='#2E2E2E')
        axs[0].text(self.df.index[-1], precio_maximo, f'{precio_maximo:.2f}', color='magenta', ha='left', va='center', fontsize=10, backgroundcolor='#2E2E2E')

        # Subplot 2: Volumen en gráfico de barras
        axs[1].bar(self.df.index, self.df['volume'], color='#1E90FF', label='Volumen', width=0.0005)
        axs[1].plot(self.df.index, self.df.Volume_SMA, color='red', label='Media móvil de volumen', linewidth=2)

        # Configuraciones adicionales
        axs[0].set_title(f'Evolución del precio de {self.pair} en Kraken', fontsize=20, color='white')
        axs[1].set_title('Volumen de operaciones', fontsize=20, color='white')

        # Añadir la leyenda al gráfico de precios con un tamaño más pequeño
        axs[0].legend(loc='upper left', fontsize=10, facecolor='black', framealpha=0.8, edgecolor='white')

        for ax in axs:
            ax.set_facecolor('#2E2E2E')
            ax.grid(True, color='grey')
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))  # Cada minuto como una marca mayor
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Formato de hora y minuto
            ax.tick_params(axis='x', colors='white', rotation=45)
            ax.tick_params(axis='y', colors='white')

        plt.tight_layout()
        plt.savefig('grafico.png', dpi=200)
        return fig
