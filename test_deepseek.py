import ollama

def clasificar_sentimiento(comentario):
    """
    Clasifica un comentario como 'positivo' o 'negativo' usando el modelo de Ollama.

    Parámetros:
        comentario (str): El comentario que se desea clasificar.

    Retorna:
        str: 'positivo' o 'negativo'.
    """
    # Crear el mensaje con instrucciones claras para el modelo
    mensaje = {
        'role': 'user',
        'content': f"Clasifica el siguiente comentario como 'positivo' o 'negativo'. Solo responde con una de esas dos palabras. Comentario: {comentario}",
    }

    # Realizar la consulta al modelo
    respuesta = ollama.chat(model='deepseek-r1:1.5b', messages=[mensaje])

    # Devolver la respuesta del modelo
    return respuesta['message']['content']

# Ejemplo de uso
comentario = "Me encanta este producto, es increíble."
resultado = clasificar_sentimiento(comentario)
print(resultado)  # Salida esperada: "positivo"