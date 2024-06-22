# spotify artist scraper

this python script scrapes all albums and tracks from a specified spotify artist profile and displays details such as album name, track name, isrc, upc, artists, album cover, and album label.

## setup

1. **clone the repository**:
    ```bash
    git clone https://github.com/yourusername/spotify-artist-scraper.git
    cd spotify-artist-scraper
    ```

2. **create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # on windows use `venv\scripts\activate`
    ```

3. **install required packages**:
    ```bash
    pip install requests
    ```

4. **run the script**:
    ```bash
    python spotify_scraper.py
    ```

## usage

1. when prompted, enter your spotify client id and secret. these will be saved to a `config.json` file for future use.
2. enter the spotify artist link.
3. the script will fetch and display the albums and tracks along with their details.

## example

enter spotify client id: your-client-id
enter spotify client secret: your-client-secret
enter spotify artist link: https://open.spotify.com/artist/ENTERSPOTIFYIDHERE

album: album name
cover: cover link
upc: upc code
label: label on the album
tracks:
name: track name
isrc: us1234567890
artists: artist name
source: track source
