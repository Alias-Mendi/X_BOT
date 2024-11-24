import pandas as pd
import numpy as np

class Dataset:
    """
    Clase que representa un conjunto de datos de precios de activos financieros.
    Proporciona métodos para calcular indicadores técnicos como SMA, MACD, Bandas de Bollinger, RSI, ADX,
    Estocástico, Momentum, CCI, ROC, Williams %R, Vortex Indicator, Retrocesos de Fibonacci, Pivot Points,
    Canales de Donchian, Heikin-Ashi, Parabolic SAR y el Precio Promedio.
    
    Los indicadores técnicos se calculan sobre el DataFrame proporcionado y se añaden como columnas.
    """

    def __init__(self, df):
        """
        Constructor de la clase Dataset.
        Toma un DataFrame con datos de precios históricos que debe incluir las columnas: 'open', 'high', 'low', 'close', 'volume'.
        """
        
        # Convertimos las columnas numéricas a tipo float para evitar errores de tipo
        df.close = df.close.astype(float)
        df.open = df.open.astype(float)
        df.high = df.high.astype(float)
        df.low = df.low.astype(float)
        df.vwap = df.vwap.astype(float)
        df.volume = df.volume.astype(float)
        self.data = df

    def print_data(self, n=5):
        """
        Imprime los primeros n registros del DataFrame. Por defecto muestra 5 registros.
        """
        print(self.data.head(n))

    def __calculate_sma_20(self):
        """
        Calcula la Media Móvil Simple (SMA) de 20 periodos sobre la columna 'close'.
        La SMA es un indicador de tendencia que suaviza las fluctuaciones de los precios.
        """
        self.data.loc[:, 'SMA'] = self.data['close'].rolling(window=20).mean()

    def __calculate_sma_50(self):
        """
        Calcula la Media Móvil Simple (SMA) de 50 periodos sobre la columna 'close'.
        Ayuda a identificar tendencias intermedias en los precios.
        """
        self.data.loc[:, 'SMA_50'] = self.data['close'].rolling(window=50).mean()

    def __calculate_sma_200(self):
        """
        Calcula la Media Móvil Simple (SMA) de 200 periodos sobre la columna 'close'.
        Indicador utilizado para identificar la tendencia a largo plazo.
        """
        self.data.loc[:, 'SMA_200'] = self.data['close'].rolling(window=200).mean()

    def __calculate_volume_sma_20(self):
        """
        Calcula la Media Móvil Simple del volumen (Volume SMA) de 20 periodos.
        Permite evaluar la fuerza detrás de las tendencias analizando el volumen negociado.
        """
        self.data.loc[:, 'Volume_SMA'] = self.data['volume'].rolling(window=20).mean()

    def __calculate_macd(self, short_window=12, long_window=26, signal_window=9):
        """
        Calcula el MACD (Moving Average Convergence Divergence).
        El MACD es un indicador de tendencia y momentum que muestra la diferencia entre dos EMAs (12 y 26 periodos, por defecto).
        - short_window: Período de la EMA corta (default 12).
        - long_window: Período de la EMA larga (default 26).
        - signal_window: Período para la línea de señal (default 9).
        """
        self.data.loc[:, 'EMA_12'] = self.data['close'].ewm(span=short_window, adjust=False).mean()
        self.data.loc[:, 'EMA_26'] = self.data['close'].ewm(span=long_window, adjust=False).mean()
        self.data.loc[:, 'MACD_Line'] = self.data['EMA_12'] - self.data['EMA_26']
        self.data.loc[:, 'Signal_Line'] = self.data['MACD_Line'].ewm(span=signal_window, adjust=False).mean()
        self.data.loc[:, 'Histograma'] = self.data['MACD_Line'] - self.data['Signal_Line']

    def __calculate_bollinger_bands(self):
        """
        Calcula las Bandas de Bollinger a partir de la SMA de 20 periodos.
        Las Bandas de Bollinger miden la volatilidad del mercado y proporcionan niveles de soporte/resistencia dinámicos.
        Se calculan como la SMA ± 2 desviaciones estándar.
        """
        if 'SMA' not in self.data.columns:
            self.__calculate_sma_20()

        self.data.loc[:, 'Banda_Superior'] = self.data['SMA'] + 2 * self.data['close'].rolling(window=20).std()
        self.data.loc[:, 'Banda_Inferior'] = self.data['SMA'] - 2 * self.data['close'].rolling(window=20).std()

    def __calculate_RSI(self, period=14):
        """
        Calcula el Índice de Fuerza Relativa (RSI) con un período dado (default 14).
        El RSI mide el momentum del precio y determina si un activo está sobrecomprado o sobrevendido.
        """
        delta = self.data['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        self.data.loc[:, 'RSI'] = 100 - (100 / (1 + rs))

    def __calculate_adx(self, period=14):
        """
        Calcula el Índice de Movimiento Direccional Promedio (ADX) en base a un período dado (default 14).
        El ADX mide la fuerza de una tendencia sin considerar si es alcista o bajista.
        """
        tr = np.maximum(self.data['high'] - self.data['low'],
                        np.abs(self.data['high'] - self.data['close'].shift(1)),
                        np.abs(self.data['low'] - self.data['close'].shift(1)))
        dm_plus = np.where((self.data['high'] - self.data['high'].shift(1)) > (self.data['low'].shift(1) - self.data['low']),
                           np.maximum(self.data['high'] - self.data['high'].shift(1), 0), 0)
        dm_minus = np.where((self.data['low'].shift(1) - self.data['low']) > (self.data['high'] - self.data['high'].shift(1)),
                            np.maximum(self.data['low'].shift(1) - self.data['low'], 0), 0)

        tr_ema = pd.Series(tr).ewm(span=period, adjust=False).mean()
        dm_plus_ema = pd.Series(dm_plus).ewm(span=period, adjust=False).mean()
        dm_minus_ema = pd.Series(dm_minus).ewm(span=period, adjust=False).mean()

        di_plus = 100 * (dm_plus_ema / tr_ema)
        di_minus = 100 * (dm_minus_ema / tr_ema)
        dx = 100 * np.abs(di_plus - di_minus) / (di_plus + di_minus)

        self.data.loc[:, 'ADX'] = dx.rolling(window=period).mean()

    def __calculate_stochastic(self, period=14, smooth_k=3, smooth_d=3):
        """
        Calcula el Oscilador Estocástico, que compara el precio de cierre actual con su rango de precios en un período determinado.
        - period: Número de periodos para el cálculo de %K (default 14).
        - smooth_k: Suavizado para la línea %K (default 3).
        - smooth_d: Suavizado para la línea %D (default 3).
        """
        self.data.loc[:, 'low_min'] = self.data['low'].rolling(window=period).min()
        self.data.loc[:, 'high_max'] = self.data['high'].rolling(window=period).max()

        self.data.loc[:, '%K'] = 100 * ((self.data['close'] - self.data['low_min']) / (self.data['high_max'] - self.data['low_min']))
        self.data.loc[:, '%K'] = self.data['%K'].rolling(window=smooth_k).mean()
        self.data.loc[:, '%D'] = self.data['%K'].rolling(window=smooth_d).mean()

        self.data.drop(columns=['low_min', 'high_max'], inplace=True)

    def __calculate_momentum(self, period=14):
        """
        Calcula el Indicador de Momentum, que mide la velocidad de cambio en los precios.
        - period: El número de períodos a utilizar en el cálculo del Momentum (default 14).
        """
        self.data.loc[:, 'Momentum'] = self.data['close'] - self.data['close'].shift(period)
        self.data.dropna(subset=['Momentum'], inplace=True)

    def __calculate_cci(self, period=20):
        """
        Calcula el Commodity Channel Index (CCI) con un período dado (default 20).
        El CCI mide la desviación del precio actual respecto a su media estadística.
        """
        self.data.loc[:, 'PT'] = (self.data['high'] + self.data['low'] + self.data['close']) / 3
        self.data.loc[:, 'SMA_PT'] = self.data['PT'].rolling(window=period).mean()
        self.data.loc[:, 'Mean_Deviation'] = self.data['PT'].rolling(window=period).apply(lambda x: np.mean(np.abs(x - np.mean(x))))

        self.data.loc[:, 'CCI'] = (self.data['PT'] - self.data['SMA_PT']) / (0.015 * self.data['Mean_Deviation'])
        self.data.drop(columns=['PT', 'SMA_PT', 'Mean_Deviation'], inplace=True)

    def __calculate_roc(self, period=14):
        """
        Calcula el Rate of Change (ROC), que mide el porcentaje de cambio en el precio durante un período dado.
        - period: Período para el cálculo del ROC (default 14).
        """
        self.data.loc[:, 'ROC'] = ((self.data['close'] - self.data['close'].shift(period)) / self.data['close'].shift(period)) * 100

    def __calculate_williams_r(self, period=14):
        """
        Calcula el Williams %R, que mide el nivel de sobrecompra o sobreventa en una escala de -100 a 0.
        - period: Período para el cálculo del Williams %R (default 14).
        """
        self.data.loc[:, 'high_max'] = self.data['high'].rolling(window=period).max()
        self.data.loc[:, 'low_min'] = self.data['low'].rolling(window=period).min()

        self.data.loc[:, 'Williams_%R'] = ((self.data['high_max'] - self.data['close']) / 
                                           (self.data['high_max'] - self.data['low_min'])) * -100
        self.data.drop(columns=['high_max', 'low_min'], inplace=True)

    def __calculate_vortex(self, period=14):
        """
        Calcula el Vortex Indicator (VI), que ayuda a identificar el comienzo de nuevas tendencias.
        - period: Período para el cálculo del Vortex Indicator (default 14).
        """
        self.data.loc[:, 'TR'] = np.maximum(self.data['high'] - self.data['low'], 
                                            np.abs(self.data['high'] - self.data['close'].shift(1)),
                                            np.abs(self.data['low'] - self.data['close'].shift(1)))

        self.data.loc[:, 'VM+'] = np.abs(self.data['high'] - self.data['low'].shift(1))
        self.data.loc[:, 'VM-'] = np.abs(self.data['low'] - self.data['high'].shift(1))

        tr_sum = self.data['TR'].rolling(window=period).sum()
        vm_plus_sum = self.data['VM+'].rolling(window=period).sum()
        vm_minus_sum = self.data['VM-'].rolling(window=period).sum()

        self.data.loc[:, 'VI+'] = vm_plus_sum / tr_sum
        self.data.loc[:, 'VI-'] = vm_minus_sum / tr_sum

        self.data.drop(columns=['TR', 'VM+', 'VM-'], inplace=True)

    def __calculate_fibonacci_retracements(self, period=None):
        """
        Calcula los niveles de retroceso de Fibonacci, identificando posibles niveles de soporte y resistencia.
        - period: El período de tiempo en el que se calcula el rango (opcional). Si no se especifica, usaremos todo el rango de datos.
        """
        data_subset = self.data if period is None else self.data.tail(period)

        high = data_subset['high'].max()
        low = data_subset['low'].min()
        diff = high - low

        self.data.loc[:, 'Fibonacci_23.6'] = high - (0.236 * diff)
        self.data.loc[:, 'Fibonacci_38.2'] = high - (0.382 * diff)
        self.data.loc[:, 'Fibonacci_50.0'] = high - (0.500 * diff)
        self.data.loc[:, 'Fibonacci_61.8'] = high - (0.618 * diff)
        self.data.loc[:, 'Fibonacci_100.0'] = low

    def __calculate_pivot_points(self):
        """
        Calcula los Pivot Points extendidos, incluyendo PP, R1, S1, R2, S2, R3 y S3.
        Los Pivot Points se utilizan para identificar niveles de soporte y resistencia.
        """
        self.data.loc[:, 'PP'] = (self.data['high'].shift(1) + self.data['low'].shift(1) + self.data['close'].shift(1)) / 3
        self.data.loc[:, 'R1'] = (2 * self.data['PP']) - self.data['low'].shift(1)
        self.data.loc[:, 'S1'] = (2 * self.data['PP']) - self.data['high'].shift(1)
        self.data.loc[:, 'R2'] = self.data['PP'] + (self.data['high'].shift(1) - self.data['low'].shift(1))
        self.data.loc[:, 'S2'] = self.data['PP'] - (self.data['high'].shift(1) - self.data['low'].shift(1))
        self.data.loc[:, 'R3'] = self.data['high'].shift(1) + 2 * (self.data['PP'] - self.data['low'].shift(1))
        self.data.loc[:, 'S3'] = self.data['low'].shift(1) - 2 * (self.data['high'].shift(1) - self.data['PP'])

    def __calculate_donchian_channels(self, period=20):
        """
        Calcula los Canales de Donchian, que identifican zonas de soporte y resistencia basadas en el máximo y mínimo de un periodo.
        - period: Período para calcular los canales (default 20).
        """
        self.data.loc[:, 'Donchian_High'] = self.data['high'].rolling(window=period).max()
        self.data.loc[:, 'Donchian_Low'] = self.data['low'].rolling(window=period).min()
        self.data.loc[:, 'Donchian_Mid'] = (self.data['Donchian_High'] + self.data['Donchian_Low']) / 2

    def __calculate_gann_levels(self, period=20):
        """
        Calcula los niveles de Gann, que dividen el rango de precios en 8 partes, proporcionando zonas geométricas de soporte y resistencia.
        - period: El número de periodos sobre los que se calcula el rango (default 20).
        """
        high = self.data['high'].rolling(window=period).max()
        low = self.data['low'].rolling(window=period).min()
        range = high - low

        self.data.loc[:, 'Gann_1/8'] = low + range * 1/8
        self.data.loc[:, 'Gann_2/8'] = low + range * 2/8
        self.data.loc[:, 'Gann_3/8'] = low + range * 3/8
        self.data.loc[:, 'Gann_4/8'] = low + range * 4/8
        self.data.loc[:, 'Gann_5/8'] = low + range * 5/8
        self.data.loc[:, 'Gann_6/8'] = low + range * 6/8
        self.data.loc[:, 'Gann_7/8'] = low + range * 7/8

    def __calculate_heikin_ashi(self):
        """
        Calcula las velas Heikin-Ashi, que suavizan el precio para mostrar mejor las tendencias.
        """
        self.data.loc[:, 'HA_close'] = (self.data['open'] + self.data['high'] + self.data['low'] + self.data['close']) / 4
        self.data.loc[:, 'HA_open'] = (self.data['open'].shift(1) + self.data['close'].shift(1)) / 2
        self.data.loc[:, 'HA_high'] = self.data[['high', 'open', 'close']].max(axis=1)
        self.data.loc[:, 'HA_low'] = self.data[['low', 'open', 'close']].min(axis=1)

    def __calculate_parabolic_sar(self, af_start=0.02, af_increment=0.02, af_max=0.2):
        """
        Calcula el Parabolic SAR (Stop and Reverse), un indicador que sigue la tendencia y ayuda a identificar puntos de entrada/salida.
        - af_start: Factor de aceleración inicial (default 0.02).
        - af_increment: Incremento del factor de aceleración (default 0.02).
        - af_max: Factor de aceleración máximo (default 0.2).
        """
        self.data.loc[:, 'PSAR'] = self.data['close'].shift(1)
        af = af_start
        ep = self.data['high'].iloc[0] if self.data['close'].iloc[0] > self.data['open'].iloc[0] else self.data['low'].iloc[0]
        trend = 1 if self.data['close'].iloc[0] > self.data['open'].iloc[0] else -1

        for i in range(1, len(self.data)):
            if trend == 1:
                self.data.loc[self.data.index[i], 'PSAR'] = self.data.loc[self.data.index[i - 1], 'PSAR'] + af * (ep - self.data.loc[self.data.index[i - 1], 'PSAR'])
                if self.data['low'].iloc[i] < self.data['PSAR'].iloc[i]:
                    trend = -1
                    self.data.loc[self.data.index[i], 'PSAR'] = ep
                    af = af_start
                    ep = self.data['low'].iloc[i]
                else:
                    if self.data['high'].iloc[i] > ep:
                        ep = self.data['high'].iloc[i]
                        af = min(af + af_increment, af_max)
            else:
                self.data.loc[self.data.index[i], 'PSAR'] = self.data.loc[self.data.index[i - 1], 'PSAR'] - af * (self.data.loc[self.data.index[i - 1], 'PSAR'] - ep)
                if self.data['high'].iloc[i] > self.data['PSAR'].iloc[i]:
                    trend = 1
                    self.data.loc[self.data.index[i], 'PSAR'] = ep
                    af = af_start
                    ep = self.data['high'].iloc[i]
                else:
                    if self.data['low'].iloc[i] < ep:
                        ep = self.data['low'].iloc[i]
                        af = min(af + af_increment, af_max)

    def __calculate_average_price(self):
        """
        Calcula el precio promedio del período, basado en los precios 'open', 'high', 'low' y 'close'.
        """
        self.data.loc[:, 'Average_Price'] = (self.data['open'] + self.data['high'] + self.data['low'] + self.data['close']) / 4

    def __calculate_atr(self, period=14):
        """
        Calcula el ATR (Average True Range), que mide la volatilidad de un activo a lo largo de un período determinado.
        - period: El número de períodos sobre los que calcular el ATR (default 14).
        """
        # Calcular el True Range (TR)
        self.data.loc[:, 'TR'] = np.maximum(self.data['high'] - self.data['low'], 
                                            np.abs(self.data['high'] - self.data['close'].shift(1)),
                                            np.abs(self.data['low'] - self.data['close'].shift(1)))
        
        # Calcular el ATR como una media móvil del TR
        self.data.loc[:, 'ATR'] = self.data['TR'].rolling(window=period).mean()

        # Eliminar la columna temporal TR
        self.data.drop(columns=['TR'], inplace=True)

        # Asegurarse de eliminar los valores NaN

    def __calculate_keltner_channels(self, period=20, multiplier=2):
        """
        Calcula los Canales de Keltner, que son un indicador de volatilidad basado en el ATR y la EMA.
        - period: El número de períodos para la EMA y el ATR (default 20).
        - multiplier: El multiplicador del ATR para calcular las bandas superior e inferior (default 2).
        """
        # Asegurarse de que se haya calculado el ATR
        if 'ATR' not in self.data.columns:
            self.__calculate_atr(period)

        # Calcular la EMA del precio de cierre
        self.data.loc[:, 'EMA_Keltner'] = self.data['close'].ewm(span=period, adjust=False).mean()

        # Calcular las bandas superior e inferior
        self.data.loc[:, 'Keltner_Superior'] = self.data['EMA_Keltner'] + (multiplier * self.data['ATR'])
        self.data.loc[:, 'Keltner_Inferior'] = self.data['EMA_Keltner'] - (multiplier * self.data['ATR'])

        # Asegurarse de eliminar los valores NaN

    def __calculate_mfi(self, period=14):
        """
        Calcula el Money Flow Index (MFI), un indicador que mide la presión de compra/venta combinando precio y volumen.
        - period: El número de períodos sobre los que calcular el MFI (default 14).
        """
        # Calcular el Precio Típico (Typical Price)
        self.data.loc[:, 'Typical_Price'] = (self.data['high'] + self.data['low'] + self.data['close']) / 3

        # Calcular el Flujo de Dinero (Money Flow)
        self.data.loc[:, 'Money_Flow'] = self.data['Typical_Price'] * self.data['volume']

        # Identificar los flujos de dinero positivo y negativo
        self.data.loc[:, 'Positive_Flow'] = np.where(self.data['Typical_Price'] > self.data['Typical_Price'].shift(1),
                                                     self.data['Money_Flow'], 0)
        self.data.loc[:, 'Negative_Flow'] = np.where(self.data['Typical_Price'] < self.data['Typical_Price'].shift(1),
                                                     self.data['Money_Flow'], 0)

        # Calcular la suma de flujos de dinero positivo y negativo
        positive_flow_sum = self.data['Positive_Flow'].rolling(window=period).sum()
        negative_flow_sum = self.data['Negative_Flow'].rolling(window=period).sum()

        # Calcular la Razón del Flujo de Dinero
        money_flow_ratio = positive_flow_sum / negative_flow_sum

        # Calcular el MFI
        self.data.loc[:, 'MFI'] = 100 - (100 / (1 + money_flow_ratio))

        # Eliminar las columnas temporales
        self.data.drop(columns=['Typical_Price', 'Money_Flow', 'Positive_Flow', 'Negative_Flow'], inplace=True)

        # Asegurarse de eliminar los valores NaN

    def __calculate_chaikin_volatility(self, period=10):
        """
        Calcula el Chaikin Volatility, que mide los cambios en el rango (high - low) de un activo durante un período determinado.
        - period: El número de períodos para la EMA del rango (default 10).
        """
        # Calcular el rango de precios (high - low)
        self.data.loc[:, 'Price_Range'] = self.data['high'] - self.data['low']

        # Calcular la EMA del rango de precios
        self.data.loc[:, 'EMA_Range'] = self.data['Price_Range'].ewm(span=period, adjust=False).mean()

        # Calcular el cambio porcentual en la EMA del rango de precios
        self.data.loc[:, 'Chaikin_Volatility'] = (self.data['EMA_Range'].diff(period) / self.data['EMA_Range'].shift(period)) * 100

        # Eliminar las columnas temporales
        self.data.drop(columns=['Price_Range', 'EMA_Range'], inplace=True)

        # Asegurarse de eliminar los valores NaN

    def __calculate_ad_line(self):
        """
        Calcula la línea de Acumulación/Distribución (A/D Line), que mide el flujo acumulado de dinero basado en el precio y el volumen.
        """
        # Calcular el Multiplicador de Clímax (Money Flow Multiplier)
        self.data.loc[:, 'Money_Flow_Multiplier'] = ((self.data['close'] - self.data['low']) - (self.data['high'] - self.data['close'])) / (self.data['high'] - self.data['low'])

        # Calcular el Volumen de Flujo de Dinero (Money Flow Volume)
        self.data.loc[:, 'Money_Flow_Volume'] = self.data['Money_Flow_Multiplier'] * self.data['volume']

        # Calcular la A/D Line acumulada
        self.data.loc[:, 'A/D_Line'] = self.data['Money_Flow_Volume'].cumsum()

        # Eliminar las columnas temporales
        self.data.drop(columns=['Money_Flow_Multiplier', 'Money_Flow_Volume'], inplace=True)

        # Asegurarse de eliminar los valores NaN

    def __calculate_eom(self, period=14):
        """
        Calcula el Ease of Movement (EOM), que mide la relación entre el cambio de precios y el volumen.
        - period: Número de períodos sobre los cuales suavizar el EOM (default 14).
        """
        # Calcular el cambio de distancia (Distance Moved)
        self.data.loc[:, 'Distance_Moved'] = ((self.data['high'] + self.data['low']) / 2) - ((self.data['high'].shift(1) + self.data['low'].shift(1)) / 2)

        # Calcular el Box Ratio (relación entre volumen y rango de precios)
        self.data.loc[:, 'Box_Ratio'] = self.data['volume'] / (self.data['high'] - self.data['low'])

        # Calcular el Ease of Movement (EOM)
        self.data.loc[:, 'EOM'] = self.data['Distance_Moved'] / self.data['Box_Ratio']

        # Suavizar el EOM usando una media móvil simple (SMA)
        self.data.loc[:, 'EOM_Smoothed'] = self.data['EOM'].rolling(window=period).mean()

        # Eliminar las columnas temporales
        self.data.drop(columns=['Distance_Moved', 'Box_Ratio', 'EOM'], inplace=True)

        # Asegurarse de eliminar los valores NaN
    def __calculate_connors_rsi(self, rsi_period=3, streak_rsi_period=2, lookback_period=100):
        """
        Calcula el Connors RSI (CRSI), un oscilador que combina el RSI de 3 periodos, el RSI de la racha, 
        y el porcentaje de retroceso en 100 días.
        - rsi_period: Período para calcular el RSI básico (default 3).
        - streak_rsi_period: Período para calcular el RSI de la longitud de la racha (default 2).
        - lookback_period: Período para calcular el retroceso de 100 días (default 100).
        """
        # Componente 1: RSI de 3 periodos (RSI básico)
        delta = self.data['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=rsi_period).mean()
        avg_loss = loss.rolling(window=rsi_period).mean()
        rs = avg_gain / avg_loss
        self.data.loc[:, 'RSI_3'] = 100 - (100 / (1 + rs))

        # Componente 2: Longitud de la Racha
        streak = np.where(self.data['close'] > self.data['close'].shift(1), 1, np.where(self.data['close'] < self.data['close'].shift(1), -1, 0))
        
        # Convertir streak a una Serie de pandas para usar shift y cumsum
        streak_series = pd.Series(streak)
        streak_cumsum = streak_series.groupby((streak_series != streak_series.shift()).cumsum()).cumsum()
        self.data.loc[:, 'Streak'] = streak_cumsum

        # Componente 3: RSI de la Racha
        delta_streak = self.data['Streak'].diff()
        gain_streak = delta_streak.where(delta_streak > 0, 0)
        loss_streak = -delta_streak.where(delta_streak < 0, 0)
        avg_gain_streak = gain_streak.rolling(window=streak_rsi_period).mean()
        avg_loss_streak = loss_streak.rolling(window=streak_rsi_period).mean()
        rs_streak = avg_gain_streak / avg_loss_streak
        self.data.loc[:, 'RSI_Streak'] = 100 - (100 / (1 + rs_streak))

        # Componente 4: Porcentaje de Retroceso de 100 días
        self.data.loc[:, 'Pct_Retracement'] = 100 * ((self.data['close'] - self.data['low'].rolling(window=lookback_period).min()) / 
                                                     (self.data['high'].rolling(window=lookback_period).max() - self.data['low'].rolling(window=lookback_period).min()))

        # Calcular el Connors RSI (Promedio de los tres componentes)
        self.data.loc[:, 'Connors_RSI'] = (self.data['RSI_3'] + self.data['RSI_Streak'] + self.data['Pct_Retracement']) / 3

        # Eliminar las columnas temporales
        self.data.drop(columns=['RSI_3', 'Streak', 'RSI_Streak', 'Pct_Retracement'], inplace=True)

        # Asegurarse de eliminar los valores NaN



    def __calculate_mfi(self, period=14):
        """
        Calcula el Money Flow Index (MFI), un indicador que mide la presión de compra/venta combinando precio y volumen.
        - period: El número de períodos sobre los que calcular el MFI (default 14).
        """
        # Calcular el Precio Típico (Typical Price)
        self.data.loc[:, 'Typical_Price'] = (self.data['high'] + self.data['low'] + self.data['close']) / 3

        # Calcular el Flujo de Dinero (Money Flow)
        self.data.loc[:, 'Money_Flow'] = self.data['Typical_Price'] * self.data['volume']

        # Identificar los flujos de dinero positivo y negativo
        self.data.loc[:, 'Positive_Flow'] = np.where(self.data['Typical_Price'] > self.data['Typical_Price'].shift(1),
                                                     self.data['Money_Flow'], 0)
        self.data.loc[:, 'Negative_Flow'] = np.where(self.data['Typical_Price'] < self.data['Typical_Price'].shift(1),
                                                     self.data['Money_Flow'], 0)

        # Calcular la suma de flujos de dinero positivo y negativo
        positive_flow_sum = self.data['Positive_Flow'].rolling(window=period).sum()
        negative_flow_sum = self.data['Negative_Flow'].rolling(window=period).sum()

        # Calcular la Razón del Flujo de Dinero (Money Flow Ratio)
        money_flow_ratio = positive_flow_sum / negative_flow_sum

        # Calcular el MFI
        self.data.loc[:, 'MFI'] = 100 - (100 / (1 + money_flow_ratio))

        # Eliminar las columnas temporales
        self.data.drop(columns=['Typical_Price', 'Money_Flow', 'Positive_Flow', 'Negative_Flow'], inplace=True)

        # Asegurarse de eliminar los valores NaN








    def get_metrics(self):
        """
        Calcula y devuelve las métricas clave del DataFrame:
        - Media Móvil Simple (SMA 20, SMA 50, SMA 200)
        - Bandas de Bollinger
        - MACD
        - RSI
        - ADX
        - Estocástico
        - Momentum
        - CCI
        - ROC
        - Williams %R
        - Vortex Indicator
        - Retrocesos de Fibonacci
        - Pivot Points
        - Canales de Donchian
        - Heikin-Ashi
        - Parabolic SAR
        - Precio Promedio
        - Niveles de Gann
        """
        self.__calculate_sma_20()
        self.__calculate_sma_50()
        self.__calculate_sma_200()
        self.__calculate_bollinger_bands()
        self.__calculate_volume_sma_20()
        self.__calculate_macd()
        self.__calculate_RSI()
        self.__calculate_adx()
        self.__calculate_stochastic()
        self.__calculate_momentum()
        self.__calculate_cci()
        self.__calculate_roc()
        self.__calculate_williams_r()
        self.__calculate_vortex()
        self.__calculate_fibonacci_retracements()
        self.__calculate_pivot_points()
        self.__calculate_donchian_channels()
        self.__calculate_heikin_ashi()
        self.__calculate_parabolic_sar()
        self.__calculate_average_price()
        self.__calculate_atr()
        self.__calculate_keltner_channels
        self.__calculate_mfi()
        self.__calculate_chaikin_volatility()
        self.__calculate_ad_line()
        self.__calculate_eom()
        self.__calculate_connors_rsi()
        self.__calculate_mfi()
        self.__calculate_gann_levels()
        self.data = self.data.iloc[-60:]
        self.data = self.data.reset_index(drop=True)  # Restablecer el índice para mantener el DataFrame limpio
        print(self.data,self.data.columns)
        return self.data
