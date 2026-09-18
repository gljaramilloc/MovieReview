import os
import numpy as np
from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv
from movie.models import Movie  # Traemos el modelo de películas

load_dotenv('../openAI.env')
client = OpenAI(api_key=os.environ.get('openai_apikey'))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommendation(request):
    search_term = request.GET.get('searchMovie')
    best_movie = None
    max_similarity = -1

    if search_term:
        response = client.embeddings.create(
            input=[search_term],
            model="text-embedding-3-small"
        )
        prompt_emb = np.array(response.data[0].embedding, dtype=np.float64)

        for movie in Movie.objects.all():
            movie_emb = np.frombuffer(movie.emb, dtype=np.float64)
            if len(movie_emb) > 0:
                similarity = cosine_similarity(prompt_emb, movie_emb)
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_movie = movie

    return render(request, 'recommendation.html', {
        'search_term': search_term, 
        'best_movie': best_movie, 
        'max_similarity': max_similarity
    })
