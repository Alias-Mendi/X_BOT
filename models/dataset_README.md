Dataset de Indicadores Técnicos para Análisis Financiero
========================================================

Descripción General
-------------------

Esta clase, `Dataset`, toma un conjunto de datos de precios de un activo financiero y calcula una serie de **indicadores técnicos** comúnmente utilizados en el análisis de mercados financieros. Estos indicadores pueden ser utilizados para evaluar tendencias, medir la fuerza de un activo, detectar volatilidad, y determinar posibles puntos de entrada y salida en estrategias de trading.

El conjunto de datos debe incluir precios `open`, `high`, `low`, `close`, `volume`, y `vwap` (precio medio ponderado por volumen), los cuales son utilizados en los cálculos de los indicadores.

Indicadores Calculados
----------------------

A continuación, se explica cada uno de los indicadores implementados, su significado en el análisis técnico, y cómo se calculan.

* * * * *

### 1\. **SMA (Simple Moving Average)**

La **Media Móvil Simple (SMA)** es el promedio de los precios de cierre de un activo durante un número específico de períodos. Se utiliza para suavizar los datos de precios y ayudar a identificar tendencias a largo y corto plazo.

-   **SMA 20**: Promedio de los últimos 20 períodos, usado para identificar tendencias a corto plazo.
-   **SMA 50**: Promedio de los últimos 50 períodos, usado para tendencias de mediano plazo.
-   **SMA 200**: Promedio de los últimos 200 períodos, utilizado para tendencias de largo plazo.

* * * * *

### 2\. **Bandas de Bollinger (Bollinger Bands)**

Las **Bandas de Bollinger** son un indicador de volatilidad. Consisten en una banda superior y una banda inferior que se sitúan a dos desviaciones estándar por encima y por debajo de la media móvil simple de 20 períodos.

-   **Cálculo**:
    -   Banda Superior = SMA 20 + (2 * Desviación Estándar)
    -   Banda Inferior = SMA 20 - (2 * Desviación Estándar)

* * * * *

### 3\. **RSI (Relative Strength Index)**

El **RSI (Índice de Fuerza Relativa)** mide la magnitud de los recientes movimientos de precios para evaluar si un activo está sobrecomprado o sobrevendido. Se calcula comparando las ganancias y pérdidas promedio durante un período determinado (normalmente 14 días).

-   **Cálculo**: RSI=100-(1001+Ganancia PromedioPeˊrdida Promedio)RSI = 100 - \left( \frac{100}{1 + \frac{\text{Ganancia Promedio}}{\text{Pérdida Promedio}}} \right)RSI=100-(1+Peˊrdida PromedioGanancia Promedio​100​)

* * * * *

### 4\. **Volume SMA 20**

Es la **Media Móvil Simple del Volumen** calculada durante 20 períodos. Esto se utiliza para evaluar la tendencia del volumen y ver si hay un incremento o disminución en la actividad comercial durante un período.

* * * * *

### 5\. **MACD (Moving Average Convergence Divergence)**

El **MACD** es un oscilador de momentum que muestra la relación entre dos medias móviles exponenciales de los precios de cierre: una media de 12 períodos y una de 26 períodos. Se utiliza para identificar cambios en la dirección o la intensidad de una tendencia.

-   **Cálculo**:
    -   **Línea MACD** = EMA 12 - EMA 26
    -   **Línea de Señal**: EMA de la Línea MACD durante 9 períodos.
    -   **Histograma**: Diferencia entre la Línea MACD y la Línea de Señal.

* * * * *

### 6\. **ADX (Average Directional Index)**

El **ADX** mide la fuerza de una tendencia. No indica la dirección de la tendencia, sino su intensidad. Un valor de ADX superior a 25 suele indicar una tendencia fuerte.

-   **Cálculo**: Basado en el rango verdadero promedio y la comparación de los movimientos direccionales positivos y negativos.

* * * * *

### 7\. **Estocástico (Stochastic Oscillator)**

El **Oscilador Estocástico** mide el momentum comparando el precio de cierre con su rango de precios durante un período específico. Ayuda a identificar condiciones de sobrecompra o sobreventa.

-   **Cálculo**: %K=100×(Cierre Actual-Mıˊnimo del PerıˊodoMaˊximo del Perıˊodo-Mıˊnimo del Perıˊodo)\%K = 100 \times \left( \frac{\text{Cierre Actual} - \text{Mínimo del Período}}{\text{Máximo del Período} - \text{Mínimo del Período}} \right)%K=100×(Maˊximo del Perıˊodo-Mıˊnimo del PerıˊodoCierre Actual-Mıˊnimo del Perıˊodo​)
    -   **%D**: Media móvil de %K.

* * * * *

### 8\. **Momentum**

El **Indicador de Momentum** mide la velocidad a la que cambia el precio de un activo. Es útil para detectar la fuerza de una tendencia.

-   **Cálculo**: Momentum=Cierre Actual-Cierre de N Perıˊodos Atraˊs\text{Momentum} = \text{Cierre Actual} - \text{Cierre de N Períodos Atrás}Momentum=Cierre Actual-Cierre de N Perıˊodos Atraˊs

* * * * *

### 9\. **CCI (Commodity Channel Index)**

El **CCI** mide la desviación del precio de un activo respecto a su media estadística durante un período. Se utiliza para identificar condiciones extremas de sobrecompra y sobreventa.

-   **Cálculo**: CCI=Precio Tıˊpico-SMA del Precio Tıˊpico0.015×Desviacioˊn PromedioCCI = \frac{\text{Precio Típico} - \text{SMA del Precio Típico}}{0.015 \times \text{Desviación Promedio}}CCI=0.015×Desviacioˊn PromedioPrecio Tıˊpico-SMA del Precio Tıˊpico​

* * * * *

### 10\. **ROC (Rate of Change)**

El **ROC** mide la tasa de cambio porcentual en el precio durante un período. Es útil para identificar la fuerza del movimiento de los precios.

-   **Cálculo**: ROC=Cierre Actual-Cierre de N Perıˊodos AtraˊsCierre de N Perıˊodos Atraˊs×100ROC = \frac{\text{Cierre Actual} - \text{Cierre de N Períodos Atrás}}{\text{Cierre de N Períodos Atrás}} \times 100ROC=Cierre de N Perıˊodos AtraˊsCierre Actual-Cierre de N Perıˊodos Atraˊs​×100

* * * * *

### 11\. **Williams %R**

El **Williams %R** es un oscilador que mide las condiciones de sobrecompra y sobreventa, pero utiliza un enfoque diferente al RSI.

-   **Cálculo**: %R=Maˊximo del Perıˊodo-Cierre ActualMaˊximo del Perıˊodo-Mıˊnimo del Perıˊodo×(-100)\%R = \frac{\text{Máximo del Período} - \text{Cierre Actual}}{\text{Máximo del Período} - \text{Mínimo del Período}} \times (-100)%R=Maˊximo del Perıˊodo-Mıˊnimo del PerıˊodoMaˊximo del Perıˊodo-Cierre Actual​×(-100)

* * * * *

### 12\. **Vortex Indicator (VI)**

El **Vortex Indicator** identifica el comienzo de nuevas tendencias midiendo el movimiento direccional positivo y negativo.

-   **Cálculo**:
    -   **VI+**: Movimiento positivo del precio.
    -   **VI-**: Movimiento negativo del precio.

* * * * *

### 13\. **Fibonacci Retracements**

Los **Retrocesos de Fibonacci** identifican niveles clave de soporte y resistencia basados en el comportamiento del precio en el rango reciente de máximos y mínimos.

* * * * *

### 14\. **Pivot Points Extendidos**

Los **Puntos Pivote** identifican niveles clave de soporte y resistencia para predicciones de movimientos intradía.

-   **Cálculo**:
    -   **PP**: (High + Low + Close) / 3
    -   **R1**, **S1**, **R2**, **S2**, etc., para niveles de resistencia y soporte adicionales.

* * * * *

### 15\. **Donchian Channels**

Los **Canales de Donchian** se usan para detectar rupturas de precio, calculando los máximos y mínimos en un período determinado.

* * * * *

### 16\. **Heikin-Ashi Candles**

Las **Velas Heikin-Ashi** son una variante de las velas japonesas que suavizan el precio para representar mejor las tendencias.

* * * * *

### 17\. **Parabolic SAR**

El **Parabolic SAR** es un indicador que se utiliza para identificar posibles puntos de entrada o salida en una tendencia. Cuando el precio cruza el SAR, se indica una posible reversión.

* * * * *

### 18\. **Average Price**

El **Precio Promedio** es el promedio de los precios máximo, mínimo, de apertura y de cierre de un período.

* * * * *

### 19\. **Keltner Channels**

Los **Canales de Keltner** son similares a las Bandas de Bollinger, pero utilizan el **ATR (Average True Range)** para medir la volatilidad.

* * * * *

### 20\. **Chaikin Volatility**

El **Chaikin Volatility** mide los cambios en el rango de precios (alto y bajo) para detectar aumentos o disminuciones de volatilidad.

* * * * *

### 21\. **Accumulation/Distribution Line (A/D Line)**

La **A/D Line** mide el flujo acumulado de capital en un activo, basado en la diferencia entre el cierre y el rango de precios.

* * * * *

### 22\. **Ease of Movement (EOM)**

El **EOM** mide cuán fácil es que el precio de un activo se mueva en función del volumen.

* * * * *

### 23\. **Connors RSI**

El **Connors RSI** es una versión mejorada del RSI que incluye el RSI de 3 períodos, la longitud de la racha y un porcentaje de retroceso.

* * * * *

### 24\. **MFI (Money Flow Index)**

El **MFI** es un oscilador que mide la presión de compra y venta al combinar el precio y el volumen. Es similar al RSI, pero con un componente de volumen añadido.

* * * * *

Cómo Usar la Clase
------------------

1.  Inicializa un objeto de la clase `Dataset` pasando un DataFrame de pandas con los datos de precios (debe incluir `open`, `high`, `low`, `close`, `volume`, `vwap`).
2.  Llama al método `get_metrics()` para calcular todos los indicadores disponibles.
3.  Usa los resultados devueltos para tus análisis de trading o inversión.

python

Copiar código

`import pandas as pd
from dataset import Dataset

# Cargar los datos de precios
df = pd.read_csv('data.csv')

# Inicializar la clase con el DataFrame
data = Dataset(df)

# Calcular los indicadores
metrics = data.get_metrics()

# Visualizar las primeras filas del DataFrame con indicadores calculados
print(metrics.head())`

* * * * *

Conclusión
----------

La clase `Dataset` implementa un amplio conjunto de indicadores técnicos, permitiendo un análisis completo del comportamiento de los precios en los mercados financieros. Los usuarios pueden utilizar estos indicadores para identificar tendencias, medir la volatilidad y tomar decisiones informadas sobre sus estrategias de inversión.

* * * * *

Este `README.md` proporciona una visión detallada de la clase y cómo utilizarla, junto con explicaciones de los indicadores implementados y su utilidad en el análisis técnico financiero. ¡Espero que sea útil para tus necesidades!