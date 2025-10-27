BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
BASE_MOVIE_URL = 'https://api.dev-cinescope.coconutqa.ru'
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"

MOVIE_PARAMS = {
    "page_size": 'pageSize=20',
    "page": 'page=3',
    'min_price': 'minPrice=1',
    'max_price': 'maxPrice=1000',
    'location1': 'locations=SPB',
    'location2': 'locations=MSK',
    'published': "published=true",
    'genre_id': 'genreId=3',
    #genre.name 3 == "Фантастика"
    'genre_name': 'Фантастика',

    "created_at": 'createdAt=asc'
}
