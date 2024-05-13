import requests
import csv

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhYmU1MzlmYTNmYzc3MDI0NTRjZTNjZDFhYWIwMjc2YSIsInN1YiI6IjY1YjIxZDI5YWIxYmM3MDE0YmE4NjE4NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.W8x7wvMrW0o9YIM5rloKsmvWRRXtnPYfIT_NASDh0lQ'
MOVIES_URL = 'https://api.themoviedb.org/3/movie/popular'
CREDITS_URL = 'https://api.themoviedb.org/3/movie/{}/credits'
GENRES_URL = 'https://api.themoviedb.org/3/genre/movie/list'

def get_movies(api_key):
    """Fetch the list of popular movies."""
    response = requests.get(MOVIES_URL, params={'api_key': api_key})
    return response.json()['results'][:10]  # Limiter à 10 films

def get_credits(movie_id, api_key):
    """Fetch movie credits to get the director and actors."""
    response = requests.get(CREDITS_URL.format(movie_id), params={'api_key': api_key})
    data = response.json()
    directors = [crew['name'] for crew in data['crew'] if crew['job'] == 'Director']
    actors = [cast['name'] for cast in data['cast'][:5]]  # Top 5 actors
    return directors, actors

def get_genres(api_key):
    """Fetch genres."""
    response = requests.get(GENRES_URL, params={'api_key': api_key})
    genres = {genre['id']: genre['name'] for genre in response.json()['genres']}
    return genres

def write_csv(movies, file_name='movies.csv'):
    """Write movies information to CSV."""
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['movie_id', 'title', 'overview', 'release_date', 'poster_path', 'director', 'actors', 'category'])
        for movie in movies:
            writer.writerow([
                movie['id'],
                movie['title'],
                movie['overview'],
                movie['release_date'],
                'https://image.tmdb.org/t/p/w500' + movie['poster_path'] if movie['poster_path'] else '',
                ', '.join(movie['directors']),
                ', '.join(movie['actors']),
                ', '.join(movie['genres'])
            ])

def main(api_key):
    genres = get_genres(api_key)
    movies = get_movies(api_key)
    for movie in movies:
        movie['genres'] = [genres[genre_id] for genre_id in movie['genre_ids']]
        directors, actors = get_credits(movie['id'], api_key)
        movie['directors'] = directors
        movie['actors'] = actors
    write_csv(movies)

if __name__ == "__main__":
    main(API_KEY)
