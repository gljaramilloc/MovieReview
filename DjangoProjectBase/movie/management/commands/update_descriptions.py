import os
from django.core.management.base import BaseCommand
from openai import OpenAI
from dotenv import load_dotenv
from movie.models import Movie  # Importa el modelo de tu base de datos

# Carga las variables de entorno desde el archivo .env (ajusta la ruta si es necesario)
load_dotenv('../openAI.env')

# Inicializa el cliente de OpenAI con la API Key
client = OpenAI(api_key=os.environ.get('openai_apikey'))

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0  
    )
    return response.choices[0].message.content.strip()

# Estructura obligatoria para un comando de Django
class Command(BaseCommand):
    help = 'Actualiza descripciones de películas usando OpenAI'

    def handle(self, *args, **kwargs):
        instruction = "Escribe un resumen atractivo para la siguiente película:"
        movies = Movie.objects.all()
        
        for movie in movies:
            prompt = f"{instruction} Actualiza la descripción '{movie.description}' de la película '{movie.title}'"
            response = get_completion(prompt)
            movie.description = response
            movie.save()
            
            self.stdout.write(self.style.SUCCESS(f"Actualizada: {movie.title}"))
            
            # El break asegura que el taller solo gaste saldo en la primera película
            break