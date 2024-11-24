import openai

def generar_comentario_openai(df_metrics):
    # Convierte las últimas observaciones a un formato de texto
    observaciones = "\n".join([
        f"{row.Index} - Precio cierre: {row.close:.2f}, Volumen: {row.volume:.2f}"
        for row in df_metrics.tail(30).itertuples()
    ])

    # Extrae los indicadores técnicos de la última fila del DataFrame
    ultimos_indicadores = df_metrics.iloc[-1]
    indicadores = (
        f"SMA (50): {ultimos_indicadores['SMA_50']:.2f}\n"
        f"SMA (200): {ultimos_indicadores['SMA_200']:.2f}\n"
        f"Banda de Bollinger Superior: {ultimos_indicadores['Banda_Superior']:.2f}\n"
        f"Banda de Bollinger Inferior: {ultimos_indicadores['Banda_Inferior']:.2f}\n"
        f"MACD: {ultimos_indicadores['MACD_Line']:.2f}, Señal MACD: {ultimos_indicadores['Signal_Line']:.2f}\n"
        f"RSI: {ultimos_indicadores['RSI']:.2f}\n"
        f"Momentum: {ultimos_indicadores['Momentum']:.2f}\n"
        f"Volumen promedio: {df_metrics['volume'].tail(30).mean():.2f}"
    )

    # Define el prompt con el rol de trader intradiario y el ejemplo
    prompt = (
        "Eres un trader intradiario especializado en criptomonedas. Vas a generar un mensaje técnico para tus traders juniors "
        "para ayudarles a entender el comportamiento reciente del mercado de BTC/USD en la última hora. Usa un lenguaje claro y "
        "didáctico, y proporciona una perspectiva de lo que podría ocurrir en las próximas horas. Aquí tienes un ejemplo del tono que buscamos:\n\n"
        "Ejemplo:\n"
        "'En las últimas horas, hemos visto cómo el precio de BTC ha estado rondando los niveles de resistencia clave, pero sin romperlos con suficiente fuerza. "
        "Esto podría indicar una falta de impulso en el corto plazo, especialmente con el RSI mostrando señales de sobrecompra. Si el volumen se mantiene bajo, "
        "es posible que veamos un retroceso hacia los soportes cercanos. En el caso de un aumento en el volumen, podríamos esperar una ruptura con más convicción.'\n\n"
        "Ahora, con base en los datos reales, proporciona tu análisis.\n\n"
        f"Resumen de las últimas observaciones de BTC/USD:\n{observaciones}\n\n"
        f"Indicadores técnicos:\n{indicadores}\n\n"
        "Con base en los datos anteriores, analiza el comportamiento del mercado de BTC/USD en la última hora y ofrece un comentario técnico para ayudar a los juniors "
        "a entender las posibles tendencias y estrategias."
    )

    # Llama a la API de OpenAI con gpt-3.5-turbo
    try:
        response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,  # Aumentado para permitir una respuesta más completa
        temperature=0.7
         )
        # Extraer el contenido del mensaje
        content = response.choices[0].message.content


        # Retornar el contenido
        return content

    except Exception as e:
            print(f"Error: {e}")





