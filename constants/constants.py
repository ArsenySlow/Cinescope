BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
BASE_MOVIE_URL = 'https://api.dev-cinescope.coconutqa.ru'

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

BASE_MOVIE_FIELDS = [
    "id", "name", "price", "description", "imageUrl", "location",
    "published", "genreId", "genre", "createdAt", "rating"
]

PARAMS = {
    "pageSize": 5,
    "page": 2,
    "minPrice": 100,
    "maxPrice": 500,
    "locations": ["MSK", "SPB"],
    "published": True,
    "genreId": 1,
    "createdAt": "desc",
}

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'