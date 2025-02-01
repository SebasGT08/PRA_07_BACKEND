from flask import Blueprint, request, jsonify,stream_with_context, Response
from app.services.social_media_service import get_comments
from app.services.comment_processor import process_comments
from app.services.sentiment_analyzer import clasificar_sentimiento
from app.utils.file_handler import save_to_csv
import json

main_routes = Blueprint('main', __name__)

@main_routes.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    presidente = data.get('presidente')
    tema = data.get('tema')
    red_social = data.get('red_social')
    max_comments = data.get('max_comments')

    def generate():
        # Obtener comentarios
        yield json.dumps({"status": "Obteniendo comentarios..."}) + "\n"
        comments = get_comments(presidente, tema, red_social, max_comments)
        print(f"{len(comments)} comentarios obtenidos.")
        yield json.dumps({"status": f"{len(comments)} comentarios obtenidos."}) + "\n"

        # Procesar comentarios
        yield json.dumps({"status": "Procesando comentarios..."}) + "\n"
        processed_comments = process_comments(comments, presidente, tema, red_social)
        print("Comentarios procesados.")
        yield json.dumps({"status": "Comentarios procesados."}) + "\n"

        # Analizar sentimientos
        yield json.dumps({"status": "Analizando sentimientos..."}) + "\n"
        analyzed_comments = []
        for i, comment_data in enumerate(processed_comments):
            comentario = comment_data["comentario_limpio"]
            sentimiento = clasificar_sentimiento(comentario)
            comment_data["sentimiento"] = sentimiento
            analyzed_comments.append(comment_data)
            yield json.dumps({
                "status": f"Analizando comentario {i + 1}/{len(processed_comments)}...", 
                "progress": round(((i + 1) / len(processed_comments)) * 100, 2)
            }) + "\n"

        # Guardar comentarios en CSV
        yield json.dumps({"status": "Guardando comentarios en CSV..."}) + "\n"
        save_to_csv(analyzed_comments)
        print("Comentarios guardados en CSV.")
        yield json.dumps({"status": "Comentarios guardados."}) + "\n"

        # Devolver respuesta final con salto adicional para el cierre
        print("Enviando respuesta final.")
        yield json.dumps({"status": "Completado", "data": analyzed_comments}) + "\n"
        yield '[DONE]' + "\n"  # Marca de cierre explícita del stream

    return Response(stream_with_context(generate()), content_type='text/event-stream')