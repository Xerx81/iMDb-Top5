import discord
import requests
from bs4 import BeautifulSoup
from typing import Optional

class Scraper:
    # Default headers to mimic a browser request
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # Common HTML tags used for scraping movie details
    common_list_tag = ("li", {"class": "ipc-metadata-list-summary-item"})
    common_title_tag = ("h3", {"class": "ipc-title__text"})
    common_rating_tag = ("span", {"class": "ipc-rating-star--rating"})
    common_year_tag = ("span", {"class": "sc-300a8231-7 eaXxft dli-title-metadata-item"})
    
    # Sends a GET request to the provided URL and returns a BeautifulSoup object
    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            response = requests.get(url, headers=self.headers, timeout=10) 
            return BeautifulSoup(response.content, "lxml")
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
    
    # Scrapes the provided BeautifulSoup object for movie data
    def scrape(self, soup, list_tag, title_tag, rating_tag, year_tag) -> list[dict[str, any]]:
        if soup is None:
            return []
        
        # Find all containers with the specified list_tag
        movie_containers = soup.findAll(*list_tag)
        movies = []
        
        # Iterate through the first 5 movie containers
        for container in movie_containers[:5]:
            movie = {}
            
            # Extract the title, rating, and year
            title = container.find(*title_tag)
            movie['title'] = title.text if title else "N/A"
            
            rating = container.find(*rating_tag)
            movie['rating'] = rating.text if rating else "N/A"
            
            year = container.find(*year_tag)
            movie['year'] = year.text if year else "N/A"
            
            movies.append(movie)  # Add the movie to the list
        
        return movies
    
    # Converts the list of movie dictionaries into a formatted string
    def dict_to_embed(self, movies: list[dict[str, any]], embed: discord.Embed) -> discord.Embed:
        if not movies:
            embed.add_field(name="No Results! Try again.", value="", inline=False)
            return embed
        
        for movie in movies:
            title = movie['title']
            info = f"{movie['year']} ⭐{movie['rating']}"
            embed.add_field(name=title, value=info, inline=False)
            embed.set_footer(text="www.imdb.com")
            embed.set_thumbnail(url="https://static.amazon.jobs/teams/53/thumbnails/IMDb_Jobs_Header_Mobile.jpg?1501027253")
        
        return embed
    
    # Fetches and returns the top movies from the provided URL
    def get_top_movies(self, url: str) -> discord.Embed:
        soup = self.get_soup(url)
        year_tag = ("span", {"class": "sc-300a8231-7 eaXxft cli-title-metadata-item"})  # Specific tag for year     
        movies = self.scrape(soup, self.common_list_tag, self.common_title_tag, self.common_rating_tag, year_tag)
        embed = discord.Embed(
            title="Top Movies",
            description="These are all time top 5 movies on imdb based on rating.",
            color=discord.Color.gold()
        )
        return self.dict_to_embed(movies, embed)
    
    # Performs an advanced search and returns the results
    def advanced_search(self, url: str, title: str, description: str) -> discord.Embed:
        soup = self.get_soup(url)
        movies = self.scrape(soup, self.common_list_tag, self.common_title_tag, self.common_rating_tag, self.common_year_tag)
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.gold()
        )
        return self.dict_to_embed(movies, embed)
