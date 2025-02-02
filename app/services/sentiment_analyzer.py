import ollama
import re


def clasificar_sentimiento(comentario, presidente):
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
        'content': f"Tu objetivo es clasificar comentarios hacia al presidente {presidente}. Si el comentario no menciona a {presidente}, analiza el tono general del comentario. Si lo menciona, analiza la parte que mencione al presidente {presidente} y responde '1' si es positivo, '2' si es negativo, o '3' si es neutral. Ignora palabras o frases que puedan parecer negativas si la parte en que se habla de {presidente} es positivo. No des explicaciones, solo responde con '1', '2', '3' o '4'. El comentario es: '{comentario}'"
    }

    # Realizar la consulta al modelo
    respuesta = ollama.chat(model='deepseek-r1:1.5b', messages=[mensaje])
    # respuesta = ollama.chat(model='deepseek-r1:7b', messages=[mensaje])

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