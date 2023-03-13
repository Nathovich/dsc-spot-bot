import configparser
import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random


# DISCORD AUTHORIZATIONS

def get_dsc_token():
    config = configparser.ConfigParser()
    config.read('dsctoken.ini')
    dsc_token = config['Config']['dsctoken']

    return dsc_token


def get_dsc_intents():
    dsc_intents = discord.Intents.default()
    dsc_intents.typing = True
    dsc_intents.messages = True
    dsc_intents.message_content = True

    return dsc_intents


dsc_bot = discord.Client(intents=get_dsc_intents())


# SPOTIFY AUTHORIZATIONS

def get_spf_auths():
    config = configparser.ConfigParser()
    config.read('spfauths.ini')
    spf_auths = (
        config['Config']['client_id'],
        config['Config']['client_secret']
    )

    return spf_auths


def get_spf_data():
    spf_auths = get_spf_auths()
    spf_client = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=spf_auths[0],
            client_secret=spf_auths[1]
        )
    )
    return spf_client


# LOOKING FOR A SONG ON SPOTIFY

# RANDOMIZERS

def offset_randomizer():
    offset_parameter = random.randint(0, 500)

    return offset_parameter


def letter_randomizer():
    letters = [
        "%25a%25",
        "%25b%25",
        "%25c%25",
        "%25d%25",
        "%25e%25",
        "%25f%25",
        "%25g%25",
        "%25h%25",
        "%25i%25",
        "%25i%25",
        "%25k%25",
        "%25l%25",
        "%25m%25",
        "%25n%25",
        "%25o%25",
        "%25p%25",
        "%25r%25",
        "%25s%25",
        "%25t%25",
        "%25u%25",
        "%25w%25",
        "%25x%25",
        "%25y%25",
        "%25z%25",
    ]

    random_letter = random.choice(letters)

    return random_letter


# SONG SEARCHER

def look_for_random_song_on_spf(spf_client):
    random_song_searcher = spotipy.Spotify.search(
        spf_client,
        q=letter_randomizer(),
        limit=1,
        offset=offset_randomizer(),
        type="track",
        market=None
    )

    return random_song_searcher


# GETTING A LINK TO A SONG

def extract_random_spf_link(spf_client) -> str:
    spf_song_dict = look_for_random_song_on_spf(spf_client)
    spf_track_data = spf_song_dict["tracks"]
    spf_items_data = spf_track_data["items"]
    spf_further_items_data = spf_items_data[0]
    spf_external_urls_data = spf_further_items_data["external_urls"]
    random_spf_link = spf_external_urls_data["spotify"]

    return random_spf_link


# LOGGING INTO DISCORD

@dsc_bot.event
async def on_ready():
    print("{0.user} is ready.".format(dsc_bot))


# MESSAGES

@dsc_bot.event
async def on_message(message):
    if message.author == dsc_bot.user:
        return

    if message.content.startswith("!song"):
        spf_client = get_spf_data()
        await message.reply(f"The random song for you :notes: : \n{extract_random_spf_link(spf_client)}")

dsc_bot.run(get_dsc_token())
