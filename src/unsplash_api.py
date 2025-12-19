import requests
import os

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
UNSPLASH_API_URL = 'https://api.unsplash.com/search/photos'

def get_unsplash_image(query):
    if not UNSPLASH_ACCESS_KEY:
        return None
    params = {
        'query': query,
        'per_page': 1,
        'client_id': UNSPLASH_ACCESS_KEY
    }
    try:
        response = requests.get(UNSPLASH_API_URL, params=params)
        data = response.json()
        if data.get('results'):
            return data['results'][0]['urls']['regular']
    except Exception:
        pass
    return None
