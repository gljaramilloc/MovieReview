import os
import requests
from django.core.management.base import BaseCommand
from openai import OpenAI
from dotenv import load_dotenv
from movie.models import Movie

# ✅ Load environment variables from the .env file
load_dotenv('../openAI.env')

# ✅ Initialize the OpenAI client with the API key
client = OpenAI(
    api_key=os.environ.get('openai_apikey'),
)

class Command(BaseCommand):
    help = 'Genera imágenes de portada para las películas usando OpenAI'

    # ✅ Función auxiliar que hace todo el trabajo con la API
    def generate_and_download_image(self, client, movie_title, save_folder):
        prompt = f"Movie poster of {movie_title}"
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        # Limpiamos un poco el nombre para que no tenga espacios al guardar el archivo
        safe_title = movie_title.replace(' ', '_').replace(':', '')
        image_filename = f"m_{safe_title}.png"
        image_path_full = os.path.join(save_folder, image_filename)

        image_response = requests.get(image_url)
        image_response.raise_for_status()
        with open(image_path_full, 'wb') as f:
            f.write(image_response.content)

        return f"movie/images/{image_filename}"

    def handle(self, *args, **kwargs):
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        # ✅ Dentro del ciclo:
        for movie in movies:
            # Llama la función auxiliar
            image_relative_path = self.generate_and_download_image(client, movie.title, images_folder)
            
            # Actualiza la imagen en la base de datos
            movie.image = image_relative_path
            movie.save()
            
            self.stdout.write(self.style.SUCCESS(f"Saved and updated image for: {movie.title}"))
            
            # Detiene la ejecución en la primera película
            break