import os
from pathlib import Path
import pandas as pd
import json
import tmdbsimple
from tqdm.auto import tqdm


def fetch_movie(id, rating):
  movie_info = tmdbsimple.Movies(id).info(
    append_to_response='credits,keywords,release_dates,watch/providers')
  movie_info['rating'] = rating
  return movie_info


def fetch_tv(id, rating):
  tv_info = tmdbsimple.TV(id).info(
    append_to_response='aggregate_credits,keywords,watch/providers')
  tv_info['rating'] = rating
  return tv_info


def main(data_path: Path, ratings_path: str = 'ratings.csv'):
  ratings = pd.read_csv(data_path / ratings_path)
  ratings = ratings.rename(columns={ 'TMDb ID': 'id', 'Your Rating': 'rating', 'Type': 'type' })
  ratings = ratings[['id', 'type', 'rating']].values.tolist()

  movie_details, tv_details = [], []
  for _id, _type, _rating in tqdm(ratings):
    if _type == 'movie':
      movie_details.append(fetch_movie(_id, _rating))
    elif _type == 'tv':
      tv_details.append(fetch_tv(_id, _rating))
    else:
      raise NotImplementedError

  with open(data_path / 'movies.json', 'w') as f:
    json.dump(movie_details, f, indent=2)

  with open(data_path / 'tv.json', 'w') as f:
    json.dump(tv_details, f, indent=2)
  
  print(f'Written {len(movie_details)} movies and {len(tv_details)} TV titles.')


if __name__ == '__main__':
  main(data_path=(Path(os.path.dirname(__file__)).parent.parent / 'data'))
