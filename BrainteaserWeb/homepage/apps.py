from django.apps import AppConfig
from sentence_transformers import SentenceTransformer


class HomepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'

    # 머신러닝 모델 서버 시작할 때 불러오기 (검색 하려면 하나만 주석 제거)
    # 60% https://huggingface.co/jhgan/ko-sbert-nli
    embedder = SentenceTransformer("jhgan/ko-sbert-nli")

    # 50% https://huggingface.co/jhgan/ko-sbert-sts
    # embedder = SentenceTransformer("jhgan/ko-sbert-sts")
    name = 'homepage'

