import csv
from app.config import Config

def save_to_csv(comments):
    """
    Guarda los comentarios analizados en un archivo CSV.

    Parámetros:
        comments (list): Lista de diccionarios con los comentarios analizados.
    """
    try:
        with open(Config.CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            
            # Escribir la cabecera si el archivo está vacío
            if file.tell() == 0:
                writer.writerow(["id", "fecha_obtencion", "tema", "red_social", "presidente", "comentario", "comentario_limpio", "sentimiento"])
            
            # Escribir cada comentario en el archivo CSV
            for comment in comments:
                writer.writerow([
                    comment["id"],
                    comment["fecha_obtencion"],
                    comment["tema"],
                    comment["red_social"],
                    comment["presidente"],
                    comment["comentario"],
                    comment["comentario_limpio"],
                    comment["sentimiento"]
                ])
        
        print(f"Comentarios guardados en {Config.CSV_FILE_PATH}")
    except Exception as e:
        print(f"Error al guardar los comentarios en CSV: {e}")