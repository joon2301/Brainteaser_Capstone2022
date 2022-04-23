from django.apps import AppConfig
from sentence_transformers import SentenceTransformer


class HomepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 60% https://huggingface.co/jhgan/ko-sbert-nli
    embedder = SentenceTransformer("jhgan/ko-sbert-nli")

    # 50% https://huggingface.co/jhgan/ko-sbert-sts
    # embedder = SentenceTransformer("jhgan/ko-sbert-sts")
    name = 'homepage'

