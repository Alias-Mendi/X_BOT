import tweepy as tw
import os

class X_Conect:
    def __init__(self):
        ''' Constructor de la clase para autenticación con API v2 '''

        # Cargar las claves y tokens de las variables de entorno
        self.api_key = os.getenv('API_KEY')
        self.api_key_secret = os.getenv('API_KEY_SECRET')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('BEARER_TOKEN')

        # Autenticación usando las claves de API y token de acceso para la API v2
        self.client = tw.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_key_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            bearer_token=self.bearer_token
        )

        # Inicializar API para la carga de medios (API v1.1)
        auth = tw.OAuth1UserHandler(
            self.api_key,
            self.api_key_secret,
            self.access_token,
            self.access_token_secret
        )
        self.api = tw.API(auth)

        # Verificar la autenticación
        try:
            user = self.api.verify_credentials()  # Cambiar a la API v1.1 para verificar credenciales
            if user:
                print("Autenticación exitosa como", user.screen_name)
            else:
                print("Error: No se pudo autenticar el usuario.")
        except Exception as e:
            print("Error durante la autenticación:", e)
            exit()

    def truncar_comentario(self, comentario, max_tokens=200):
        ''' Trunca el comentario para que no exceda el límite de tokens '''
        palabras = comentario.split()
        if len(palabras) > max_tokens:
            return " ".join(palabras[:max_tokens]) + "..."
        return comentario

    def post_tweet(self, comentario):
        ''' Método para publicar un tweet usando solo la API v1.1 '''
        
        comentario_truncado = str(self.truncar_comentario(comentario, max_tokens=200))
        imagen = 'grafico.png'  # Asegúrate de que este archivo existe y es accesible

        # Verificar si el archivo existe antes de intentar subirlo
        if not os.path.isfile(imagen):
            print("Error: El archivo de imagen no existe.")
            return

        # Subir la imagen
        try:
            media = self.api.media_upload(imagen)
            media_id = media.media_id_string
            print("Imagen subida exitosamente.")
        except Exception as e:
            print(f"Error al subir la imagen: {e}")
            return  # Salimos si hay un problema con la imagen

        # Publicar el tweet con la imagen
        try:
            self.api.update_status(status=comentario_truncado, media_ids=[media_id])
            print("Tweet publicado exitosamente.")
            os.remove("grafico.png")  # Eliminar la imagen después de publicar el tweet
        except Exception as e:
            print(f"Error al publicar el tweet: {e}")

    def post_tweet1(self, comentario):
        ''' Método para publicar un tweet usando solo la API v2 sin imagen '''
        
        comentario_truncado = str(self.truncar_comentario(comentario, max_tokens=200))

        try:
            response = self.client.create_tweet(text=comentario_truncado)
            print("Tweet publicado exitosamente. ID:", response.data['id'])
        except Exception as e:
            print(f"Error al publicar el tweet: {e}")
