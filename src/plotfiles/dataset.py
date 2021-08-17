import os
from pathlib import Path
import pandas as pd


def load_movies():
  data_path = Path(os.path.dirname(__file__)).parent.parent / 'data'

  movies = pd.read_json(data_path / 'movies.json')

  movies = movies.drop(columns=['adult', 'backdrop_path', 'belongs_to_collection',
  'homepage', 'poster_path', 'status', 'video', 'production_companies', 'release_dates', 'watch/providers'])
  movies['release_date'] = pd.to_datetime(movies.release_date)
  movies['release_year'] = movies.release_date.dt.year
  movies['release_month'] = movies.release_date.dt.month_name()
  movies['release_day'] = movies.release_date.dt.day_name()
  movies['genres'] = movies.genres.apply(lambda row: list(map(lambda v: v['name'], row)))
  movies['production_countries'] = movies.production_countries.apply(lambda row: list(map(lambda v: v['name'], row)))
  movies['keywords'] = movies.keywords.apply(lambda row: list(map(lambda v: v['name'], row['keywords'])))
  movies['spoken_languages'] = movies.spoken_languages.apply(lambda row: list(map(lambda v: v['iso_639_1'], row)))

  return movies


def load_tv():
  data_path = Path(os.path.dirname(__file__)).parent.parent / 'data'

  tv = pd.read_json(data_path / 'tv.json')

  tv = tv.drop(columns=['backdrop_path', 'homepage', 'languages',
    'next_episode_to_air', 'last_episode_to_air', 'poster_path', 'production_companies',
    'watch/providers'])
  tv['first_air_date'] = pd.to_datetime(tv.first_air_date)
  tv['last_air_date'] = pd.to_datetime(tv.last_air_date)
  tv['first_air_year'] = tv.first_air_date.dt.year
  tv['first_air_month'] = tv.first_air_date.dt.month_name()
  tv['first_air_day'] = tv.first_air_date.dt.day_name()
  tv['genres'] = tv.genres.apply(lambda row: list(map(lambda v: v['name'], row)))
  tv['networks'] = tv.networks.apply(lambda row: list(map(lambda v: v['name'], row)))
  tv['production_countries'] = tv.production_countries.apply(lambda row: list(map(lambda v: v['name'], row)))
  tv['keywords'] = tv.keywords.apply(lambda row: list(map(lambda v: v['name'], row['results'])))
  tv['spoken_languages'] = tv.spoken_languages.apply(lambda row: list(map(lambda v: v['iso_639_1'], row)))
  
  return tv
