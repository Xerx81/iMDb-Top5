import discord
import os
from discord import app_commands
from dotenv import load_dotenv
from scraper import Scraper

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from a .env file

    # Define intents to specify which events your bot will receive
    intents = discord.Intents.default()
    intents.message_content = True  # Allow the bot to read message content

    # Create a client instance with the specified intents
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)  # Set up a command tree for slash commands

    urls = {
        "topmovies": "https://www.imdb.com/chart/top/",
        "movies": "https://www.imdb.com/search/title/?title_type=feature",
        "series": "https://www.imdb.com/search/title/?title_type=tv_series",
        "games": "https://www.imdb.com/search/title/?title_type=video_game",
        "title": "https://www.imdb.com/search/title/?title=",
        "release": "https://www.imdb.com/search/title/?release_date=",
    }

    scraper = Scraper()

    @client.event
    async def on_ready() -> None:
        print(f'We have logged in as {client.user}')
        try:
            synced = await tree.sync()  # Sync all commands
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)


    @tree.command(name="topmovies", description="Gives list of top 5 movies of all time")
    async def topmovies(interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['topmovies']
            movies_embed = scraper.get_top_movies(url)
            await interaction.followup.send(embed=movies_embed)
        except Exception as e:
            print(e)


    @tree.command(name="movies", description="Gives list of top 5 currently popular movies")
    async def movies(interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['movies']

            # title and description for the embed object
            title = "Movies"
            description = "These are top 5 currently popular movies"

            movies_embed = scraper.advanced_search(url, title, description)
            await interaction.followup.send(embed=movies_embed)
        except Exception as e:
            print(e)


    @tree.command(name="series", description="Gives list of top 5 currently popular series")
    async def series(interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['series']
            title = "Series"
            description = "These are top 5 currently popular series"

            series_embed = scraper.advanced_search(url, title, description)
            await interaction.followup.send(embed=series_embed)
        except Exception as e:
            print(e)


    @tree.command(name="games", description="Gives list of top 5 currently popular games")
    async def games(interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['games']
            title = "Games"
            description = "These are top 5 currently popular games"

            games_embed = scraper.advanced_search(url, title, description)
            await interaction.followup.send(embed=games_embed)
        except Exception as e:
            print(e)


    @tree.command(name="title", description="Gives list of top 5 items regarding the title")
    @app_commands.describe(item_name="The title to search for")
    async def title(interaction: discord.Interaction, item_name: str) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            url = f"{urls['title']}{item_name}"
            title = item_name.title()
            description = f"These are top 5 currently popular items with '{title}' title"

            title_embed = scraper.advanced_search(url, title, description)
            await interaction.followup.send(embed=title_embed)
        except Exception as e:
            print(e)


    @tree.command(name="release", description="Gives list of top 5 items from given year")
    @app_commands.describe(item_year="The release year to search for")
    async def release(interaction: discord.Interaction, item_year: int) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            url = f"{urls['release']}{item_year}"
            title = item_year
            description = f"These are top 5 popular items of year {title}"

            release_embed = scraper.advanced_search(url, title, description)
            await interaction.followup.send(embed=release_embed)
        except Exception as e:
            print(e)


    @tree.command(name="help", description="Shows list of available commands")
    async def help(interaction: discord.Interaction) -> None:

        # Dict for all commands and its function
        commands_info = {
            "/topmovies": "Gives list of top 5 movies of all time",
            "/movies": "Gives list of top 5 currently popular movies",
            "/series": "Gives list of top 5 currently popular series",
            "/games": "Gives list of top 5 currently popular games",
            "/title item_name": "Gives list of top 5 items regarding the title",
            "/release item_year": "Gives list of top 5 items from given year"
        }
        
        embed = discord.Embed(
            title="All Commands",
            description="These are all the commands you can use to interact with the bot.",
            color=discord.Color.gold()
        )

        try:
            await interaction.response.defer(ephemeral=False)
            for command, description in commands_info.items():
                embed.add_field(name=command, value=description, inline=False)
            embed.set_footer(text="www.imdb.com")
            embed.set_thumbnail(url="https://static.amazon.jobs/teams/53/thumbnails/IMDb_Jobs_Header_Mobile.jpg?1501027253")

            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)

    # Run the bot using the token from the .env file
    client.run(os.getenv('TOKEN'))
