import discord
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

headers = {"User-Agent": "Mozilla/5.0"}


def scrape_imdb_top_5_movies():
  url = "https://www.imdb.com/chart/top/"
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "lxml")

  htmlTitle = soup.findAll(class_="ipc-title__text")
  movie_containers = soup.findAll("li", class_="ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent")

  i = 0
  movies = []
  for container in movie_containers:
    if i == 5:
      break
    title = container.find("h3", class_="ipc-title__text").text
    try:
      rating = container.find("span", class_="ipc-rating-star--rating").text
    except AttributeError:
      rating = "N/A"
    try:
      year = container.find("span", class_="sc-b189961a-8 hCbzGp cli-title-metadata-item").text
    except AttributeError:
      year = "N/A"

    movie = {
      "title": title,
      "rating": rating,
      "year": year
    }
    movies.append(movie)

    i += 1

  return movies


def scrape_imdb_top_5_by_title(title):
  url = f"https://www.imdb.com/search/title/?title={title}"

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "lxml")
  
  movie_containers = soup.findAll("li", class_="ipc-metadata-list-summary-item")

  i = 0
  movies = []
  for container in movie_containers:
    if i == 5:
      break
    title = container.find("h3", class_="ipc-title__text").text
    try:
      rating = container.find("span", class_="ipc-rating-star--rating").text
    except AttributeError:
      rating = "N/A"
    try:
      year = container.find("span", class_="sc-b189961a-8 hCbzGp dli-title-metadata-item").text
    except AttributeError:
      year = "N/A"

    movie = {
      "title": title,
      "rating": rating,
      "year": year
    }
    movies.append(movie)

    i += 1

  return movies
  

def dict_to_string(movies):
  movie_msg = ""
  for movie in movies:
    movie_msg += f"{movie['title']}\n{movie['year']}  ⭐{movie['rating']}\n\n"
  
  if movie_msg:
    return movie_msg
  else:
    return "No Results! Try again."

  
if __name__ == "__main__":

  intents = discord.Intents.default()
  intents.message_content = True

  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    print(f'We have logged in as {client.user}')

  @client.event
  async def on_message(message):

    if message.author == client.user:
      return

    if message.content.startswith('.topmovies'):
      movies = scrape_imdb_top_5_movies()

      movie_msg = dict_to_string(movies)

      await message.channel.send(f"```{movie_msg}```")


    if message.content.startswith('.title'):

      title = ' '.join(message.content.split()[1:])
      movies = scrape_imdb_top_5_by_title(title)

      movie_msg = dict_to_string(movies)
      await message.channel.send(f"```{movie_msg}```")

  client.run(os.getenv('TOKEN'))

