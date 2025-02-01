from .reddit_service import get_comments as get_reddit_comments
from .youtube_service import get_youtube_comments_by_topic
from .x_service import get_x_comments

def get_comments(presidente, tema, red_social, max_comments):
    if red_social.lower() == "reddit":
        return get_reddit_comments(presidente, tema, max_comments)
    elif red_social.lower() == "youtube":
        return get_youtube_comments_by_topic(presidente, tema, max_comments)
    elif red_social.lower() == "x":
        return get_x_comments(presidente, tema, max_comments)
    else:
        print(f"Red social no soportada: {red_social}")
        return []