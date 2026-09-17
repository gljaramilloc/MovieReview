import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Asigna imágenes de la carpeta local a las películas en la base de datos'

    def handle(self, *args, **kwargs):
        # 📂 Ruta de la carpeta donde están las imágenes descargadas
        images_folder = 'media/movie/images/'
        
        # ✅ Verifica si la carpeta existe
        if not os.path.exists(images_folder):
            self.stderr.write(f"La carpeta '{images_folder}' no existe.")
            return

        movies = Movie.objects.all()
        
        # Obtenemos la lista de todos los archivos de imagen disponibles
        available_images = os.listdir(images_folder)
        updated_count = 0

        # 📖 Recorremos cada película en la base de datos
        for movie in movies:
            image_found = False
            
            # Limpiamos el título para hacer una búsqueda más precisa
            clean_title = movie.title.replace(' ', '').replace(':', '').replace('_', '').lower()
            
            for filename in available_images:
                clean_filename = filename.replace(' ', '').replace('_', '').lower()
                
                # Si el título de la película está dentro del nombre del archivo:
                if clean_title in clean_filename:
                    # ❗ Actualiza la ruta en la base de datos
                    # (Django añade automáticamente '/media/' al renderizar)
                    movie.image = f"movie/images/{filename}"
                    movie.save()
                    
                    image_found = True
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
                    break
            
            # Si termina el ciclo y no encontró imagen, lanza una advertencia
            if not image_found:
                self.stdout.write(self.style.WARNING(f"Image not found for: {movie.title}"))

        # ✅ Al finalizar, muestra cuántas películas se actualizaron
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies with local images."))