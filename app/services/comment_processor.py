from datetime import datetime
from deep_translator import GoogleTranslator
import re
import string
import nltk
from nltk.corpus import stopwords
from langdetect import detect  # Asegúrate de tener instalada la librería: pip install langdetect

# Descarga de recursos necesarios de NLTK
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('punkt_tab') 

# Función auxiliar para traducir el texto, manejando el límite de 5000 caracteres
def translate_text(text, source_lang='auto', target_lang='es'):
    # Si se usa detección automática, se verifica si el texto ya está en el idioma destino
    if source_lang == 'auto':
        try:
            detected_lang = detect(text)
        except Exception:
            detected_lang = None
        if detected_lang == target_lang:
            return text  # No es necesario traducir si ya está en el idioma destino

    max_chars = 5000
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    if len(text) <= max_chars:
        return translator.translate(text)
    else:
        translated_parts = []
        # Dividir el texto en fragmentos de hasta 5000 caracteres
        for i in range(0, len(text), max_chars):
            chunk = text[i:i + max_chars]
            translated_chunk = translator.translate(chunk)
            translated_parts.append(translated_chunk)
        # Unir los fragmentos traducidos con un espacio entre ellos
        return ' '.join(translated_parts)

def process_comments(comments, presidente, tema, red_social):
    stopwords_es = set(stopwords.words('spanish'))
    total = len(comments)
    
    for i, comment in enumerate(comments, start=1):
        # 1. Eliminar saltos de línea, tabulaciones y el carácter ';'
        comment = comment.replace("\n", " ").replace("\t", " ").replace(";", "")
        # 2. Reemplazar múltiples espacios por uno solo
        comment = re.sub(r'\s+', ' ', comment).strip()

        # Obtener la fecha actual en formato YYYY-MM-DD HH:MM:SS
        fecha_obtencion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 3. Traducir el comentario
        if red_social == 'twitter':
            translated_comment = comment
        else:
            translated_comment = translate_text(comment, source_lang='auto', target_lang='es')
            if translated_comment != comment:
                translated_comment = "[T] " + translated_comment
        
        # 4. Tokenización y filtrado
        text_for_tokens = translated_comment.lower()
        text_for_tokens = text_for_tokens.translate(str.maketrans('', '', string.punctuation))
        tokens = nltk.word_tokenize(text_for_tokens, language='spanish')
        filtered_tokens = [
            token for token in tokens
            if token.isalpha() and len(token) >= 4 and token not in stopwords_es
        ]
        
        # 5. Formatear el comentario
        formatted_comment = {
            "id": i,
            "fecha_obtencion": fecha_obtencion,
            "tema": tema,
            "red_social": red_social,
            "presidente": presidente,
            "comentario": comment,                   # Comentario original ya limpio
            "comentario_limpio": translated_comment,   # Comentario traducido (con [T] si fue traducido)
            "tokens": filtered_tokens                # Tokens resultantes
        }
        
        # Emite el comentario procesado junto con el avance actual
        yield formatted_comment, i, total

