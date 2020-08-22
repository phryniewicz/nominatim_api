NOMINATIM_API_CONFIGURATION = {
    "limit": 1,
    "format": 'json',
    "addressdetails": 1
}

REDIS_LIFE_SPAN = {
    "days": 7
}

BASE_URL = "https://nominatim.openstreetmap.org/search?q="

REDIS_CONFIGURATION = {
    'host': 'redis',
    'password': "ubuntu",
    'port': 6379
}
