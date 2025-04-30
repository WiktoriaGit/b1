import cloudinary #biblioteka umożliwiająca wysyłanie plików

cloudinary.config(
    cloud_name="dsqktogv8",          #nazwa konta
    api_key="92381337923258",        #klucz do identyfikacji aplikacji
    api_secret="D1fB7m2Dh4UyBTjee0td4Vi1rYc",  #hasło do autoryzacji
    secure=True #wymusza połączenie HTTPS
)
