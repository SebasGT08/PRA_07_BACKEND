import requests
from dotenv import load_dotenv
import os

# URL base de la API de YouTube
BASE_URL = "https://www.googleapis.com/youtube/v3"
SEARCH_URL = f"{BASE_URL}/search"  # Para buscar videos
COMMENT_THREADS_URL = f"{BASE_URL}/commentThreads"  # Para obtener comentarios

# Tu clave API de YouTube
# Cargar las variables de entorno desde el archivo .env
load_dotenv('secrets.env')
# Acceder a la API key
api_key = os.getenv('API_KEY')
API_KEY = api_key   # Reemplaza con tu clave API

# Función para buscar videos en YouTube
def search_youtube_videos(query, max_results=5):
    try:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "key": API_KEY,
            "maxResults": max_results
        }

        response = requests.get(SEARCH_URL, params=params)
        if response.status_code != 200:
            print(f"Error en la solicitud de búsqueda: {response.status_code}")
            print(response.json())  # Muestra el mensaje de error
            return []

        data = response.json()
        video_ids = [item["id"]["videoId"] for item in data.get("items", [])]
        return video_ids
    except Exception as e:
        print(f"Error al buscar videos en YouTube: {e}")
        return []

# Función para obtener comentarios de un video en YouTube
def get_youtube_comments(video_id, max_comments):
    try:
        params = {
            "part": "snippet",
            "videoId": video_id,
            "key": API_KEY,
            "maxResults": max_comments  # Máximo de comentarios por página (el máximo permitido por la API)
        }

        comments = []  # Lista para guardar comentarios

        # Paginación para obtener comentarios
        while len(comments) < max_comments:
            response = requests.get(COMMENT_THREADS_URL, params=params)
            if response.status_code != 200:
                print(f"Error en la solicitud de comentarios: {response.status_code}")
                print(response.json())  # Muestra el mensaje de error
                break

            data = response.json()

            # Extraer comentarios
            for item in data.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                comments.append(comment)
                if len(comments) >= max_comments:
                    break  # Detener si ya tenemos suficientes comentarios

            # Verificar si hay más páginas
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
            params["pageToken"] = next_page_token

        return comments[:max_comments]  # Asegurarse de no exceder el máximo de comentarios
    except Exception as e:
        print(f"Error al obtener comentarios de YouTube: {e}")
        return []

# Función principal para obtener comentarios de YouTube
def get_youtube_comments_by_topic(presidente, tema, max_comments):
    # Buscar videos relacionados con el presidente y el tema
    query = f"{presidente} {tema}"
    video_ids = search_youtube_videos(query, max_results=3)  # Buscar hasta 3 videos

    if not video_ids:
        print(f"No se encontraron videos para: {query}")
        return []

    # Obtener comentarios de los videos encontrados
    all_comments = []
    for video_id in video_ids:
        comments = get_youtube_comments(video_id, max_comments)
        all_comments.extend(comments)
        if len(all_comments) >= max_comments:
            break  # Detener si ya tenemos suficientes comentarios

    return all_comments[:max_comments]  # Asegurarse de no exceder el máximo de comentarios