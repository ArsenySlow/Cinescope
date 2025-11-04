BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
BASE_MOVIE_URL = 'https://api.dev-cinescope.coconutqa.ru'

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"

SUPERADMIN_CREDS= ("api1@gmail.com", "asdqwe123Q")

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

BASE_MOVIE_FIELDS = [
    "id", "name", "price", "description", "imageUrl", "location",
    "published", "genreId", "genre", "createdAt", "rating"
]
