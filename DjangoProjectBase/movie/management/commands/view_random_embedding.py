import numpy as np
import random
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Muestra el embedding de una película seleccionada al azar'

    def handle(self, *args, **kwargs):
        movies = list(Movie.objects.all())
        if not movies:
            self.stderr.write("No hay películas en la base de datos.")
            return

        movie = random.choice(movies)
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)

        self.stdout.write(self.style.SUCCESS(f"🎬 Película seleccionada: {movie.title}"))
        self.stdout.write(f"Valores del embedding (primeros 5): {embedding_vector[:5]}")