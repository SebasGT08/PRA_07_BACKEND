import ollama
import re


def clasificar_sentimiento(comentario):
    """
    Clasifica un comentario como 'positivo', 'negativo' o 'neutro' usando el modelo de Ollama.

    Parámetros:
        comentario (str): El comentario que se desea clasificar.

    Retorna:
        str: 'positivo', 'negativo' o 'neutro'.
    """
    # Crear el mensaje con instrucciones claras para el modelo
    mensaje = {
        'role': 'user',
        'content': f"Tu objetivo es clasificar comentarios, si es positivo responderas '1', si es negativo '2' , si es neutral '3' si no te es posible identificar '4'. No des explicaciones ni nada solo puedes responder con '1', '2', '3' o '4'. Comentario: {comentario}",
    }

    # Realizar la consulta al modelo
    respuesta = ollama.chat(model='deepseek-r1:1.5b', messages=[mensaje])

    # Extraer el contenido de la respuesta
    respuesta_completa = respuesta['message']['content']

    # Eliminar el contenido entre <think> y </think> usando una expresión regular
    respuesta_filtrada = re.sub(r'<think>.*?</think>', '', respuesta_completa, flags=re.DOTALL).strip()

    # Determinar el resultado según el valor filtrado
    if respuesta_filtrada == "1":
        return "positivo"
    elif respuesta_filtrada == "2":
        return "negativo"
    elif respuesta_filtrada == "3":
        return "neutral"
    else:
        return "NA"