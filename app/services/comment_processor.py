from datetime import datetime

def process_comments(comments, presidente, tema, red_social):
    processed_comments = []
    
    for i, comment in enumerate(comments, start=1):
        # Limpiar el comentario: eliminar saltos de línea y el carácter ';'
        comment = comment.replace("\n", " ").replace(";", "")
        
        # Asegurar que el comentario esté en formato UTF-8
        cleaned_comment = comment.encode('utf-8').decode('utf-8')
        
        # Obtener la fecha actual en formato YYYY-MM-DD HH:MM:SS
        fecha_obtencion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Formatear el comentario según el formato requerido
        formatted_comment = {
            "id": i,
            "fecha_obtencion": fecha_obtencion,
            "tema": tema,
            "red_social": red_social,
            "presidente": presidente,
            "comentario": comment,  # Comentario original
            "comentario_limpio": cleaned_comment  # Comentario limpio
        }
        
        processed_comments.append(formatted_comment)
    
    return processed_comments