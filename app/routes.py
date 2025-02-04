from flask import Blueprint, request, stream_with_context, Response
from app.services.social_media_service import get_comments
from app.services.comment_processor import process_comments
from app.utils.file_handler import save_to_csv
import json
import multiprocessing
from functools import partial
import time

# Función auxiliar para multiprocessing (definida a nivel de módulo)
def worker_clasificar_sentimiento(commentario, presidente, model):
    from app.services.sentiment_analyzer import clasificar_sentimiento
    return clasificar_sentimiento(commentario, presidente, model)

main_routes = Blueprint('main', __name__)

@main_routes.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    presidente = data.get('presidente')
    tema = data.get('tema')
    red_social = data.get('red_social')
    max_comments = data.get('max_comments')
    model = data.get('model') 

    def generate():
        start_time = time.time() 
        # 1. Obtener comentarios
        yield json.dumps({"status": "Obteniendo comentarios..."}) + "\n"
        comments = get_comments(presidente, tema, red_social, max_comments)
        print(f"{len(comments)} comentarios obtenidos.")
        yield json.dumps({"status": f"{len(comments)} comentarios obtenidos."}) + "\n"

        # 2. Procesar comentarios y enviar avance por cada uno
        yield json.dumps({"status": "Procesando comentarios..."}) + "\n"
        processed_comments = []
        for formatted_comment, i, total in process_comments(comments, presidente, tema, red_social):
            processed_comments.append(formatted_comment)
            yield json.dumps({
                "status": f"Procesando comentario {i}/{total}...", 
                "progress": round((i / total) * 100, 2)
            }) + "\n"
        print("Comentarios procesados.")
        yield json.dumps({"status": "Comentarios procesados."}) + "\n"

        # 3. Analizar sentimientos en paralelo usando multiprocessing
        yield json.dumps({"status": "Cargando modelo: " + model + "..."}) + "\n"
        analyzed_comments = []
        
        # Extraer la lista de comentarios (texto limpio) a analizar
        comments_to_analyze = [comment_data["comentario_limpio"] for comment_data in processed_comments]
        total_comments = len(comments_to_analyze)

        # Configurar el Pool de procesos
        pool = multiprocessing.Pool(processes=4)
        # Fijamos los argumentos 'presidente' y 'model' con partial para worker_clasificar_sentimiento.
        worker_func = partial(worker_clasificar_sentimiento, presidente=presidente, model=model)
        
        # Imap devuelve resultados en el mismo orden de la lista de entrada.
        for i, sentimiento in enumerate(pool.imap(worker_func, comments_to_analyze), start=1):
            processed_comments[i-1]["sentimiento"] = sentimiento
            analyzed_comments.append(processed_comments[i-1])
            yield json.dumps({
                "status": f"Analizando comentario {i}/{total_comments}...", 
                "progress": round((i / total_comments) * 100, 2)
            }) + "\n"
        
        # Cerrar y esperar a que finalicen los procesos del pool
        pool.close()
        pool.join()
        print("Análisis de sentimientos completado.")

        # 4. Guardar comentarios en CSV
        yield json.dumps({"status": "Guardando comentarios en CSV..."}) + "\n"
        save_to_csv(analyzed_comments)
        print("Comentarios guardados en CSV.")
        yield json.dumps({"status": "Comentarios guardados."}) + "\n"

        # 5. Enviar respuesta final
        print("Enviando respuesta final.")
        yield json.dumps({"status": "Completado", "data": analyzed_comments}) + "\n"
        yield '[DONE]' + "\n"  # Marca de cierre explícita del stream
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"Tiempo total de procesamiento: {processing_time:.2f} segundos")

    return Response(stream_with_context(generate()), content_type='text/event-stream')
