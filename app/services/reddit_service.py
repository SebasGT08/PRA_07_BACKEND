import requests
from bs4 import BeautifulSoup

# Cabeceras para evitar ser bloqueado por el servidor
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def search_reddit_posts(presidente, tema):
    # Construir la URL de búsqueda en Old Reddit
    search_url = f"https://old.reddit.com/search?q={presidente}+{tema}&sort=relevance&t=all"
    
    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()

        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar los enlaces de los posts
        post_links = []
        for post in soup.find_all("div", class_="search-result-link"):
            link = post.find("a", href=True)
            if link:
                # Asegurarse de que el enlace sea absoluto
                post_url = link['href']
                if not post_url.startswith('http'):
                    post_url = 'https://old.reddit.com' + post_url
                post_links.append(post_url)

        return post_links
    except Exception as e:
        print(f"Error al buscar posts en Reddit: {e}")
        return []

def get_comments_from_post(post_url, max_comments):
    try:
        response = requests.get(post_url, headers=HEADERS)
        response.raise_for_status()

        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrar los comentarios
        comment_elements = soup.find_all("div", class_="md")  # Clase que contiene los comentarios
        
        # Filtrar comentarios eliminados y omitir el primer comentario
        comments = []
        for comment in comment_elements[1:]:  # Omitir el primer comentario
            comment_text = comment.get_text(strip=True)
            if comment_text != "[deleted]" and comment_text != "[removed]":
                comments.append(comment_text)
            if len(comments) >= max_comments:
                break  # Limitar a max_comments por publicación

        return comments
    except Exception as e:
        print(f"Error al obtener comentarios de Reddit: {e}")
        return []

def get_comments(presidente, tema, max_comments):
    # Buscar posts relacionados con el presidente y el tema
    post_links = search_reddit_posts(presidente, tema)
    
    if not post_links:
        return []  # Si no se encuentran posts, devolvemos una lista vacía

    # Obtener comentarios de los primeros posts encontrados
    all_comments = []
    for post_link in post_links[:5]:  # Limitar a los primeros 3 posts para no sobrecargar
        comments = get_comments_from_post(post_link, 10)  # Limitar a 5 comentarios por publicación
        all_comments.extend(comments)
        if len(all_comments) >= max_comments:
            break  # Detener si ya tenemos suficientes comentarios

    return all_comments[:max_comments]  # Asegurarse de no exceder el máximo de comentarios