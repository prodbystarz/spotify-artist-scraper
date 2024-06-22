import requests
import json
import os
from requests.auth import HTTPBasicAuth

CONFIG_FILE = 'config.json' # do not make this it will automatically make it

def save_config(client_id, client_secret):
    config = {
        'client_id': client_id,
        'client_secret': client_secret
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def get_token(client_id, client_secret):
    r = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'grant_type': 'client_credentials'},
        auth=HTTPBasicAuth(client_id, client_secret)
    )
    return r.json().get('access_token')

def fetch_albums(token, artist_id):
    h = {'Authorization': f'Bearer {token}'}
    albums, url = [], f'https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single&limit=50'
    while url:
        d = requests.get(url, headers=h).json()
        albums.extend(d['items'])
        url = d['next']
    return albums

def fetch_album_details(token, album_id):
    h = {'Authorization': f'Bearer {token}'}
    return requests.get(f'https://api.spotify.com/v1/albums/{album_id}', headers=h).json()

def fetch_isrc(token, track_id):
    h = {'Authorization': f'Bearer {token}'}
    d = requests.get(f'https://api.spotify.com/v1/tracks/{track_id}', headers=h).json()
    return d.get('external_ids', {}).get('isrc', 'N/A')

def format_data(token, albums, details):
    for album in albums:
        a = details[album['id']]
        print(f"Album: {album['name']}")
        print(f"Cover: {a['images'][0]['url'] if a['images'] else 'N/A'}")
        print(f"UPC: {a['external_ids'].get('upc', 'N/A')}")
        print(f"Label: {a.get('label', 'N/A')}")
        print("Tracks:")
        for track in a['tracks']['items']:
            code = track.get('external_ids', {}).get('isrc', 'N/A')
            if code == 'N/A':
                code = fetch_isrc(token, track['id'])
            print(f"  Name: {track['name']}")
            print(f"  ISRC: {code}")
            print(f"  Artists: {', '.join(artist['name'] for artist in track['artists'])}")
            print(f"  Source: {a.get('label', 'N/A')}")
        print("="*50)

def main():
    config = load_config()
    if not config:
        client_id = input("Enter Spotify Client ID: ")
        client_secret = input("Enter Spotify Client Secret: ")
        save_config(client_id, client_secret)
    else:
        client_id = config['client_id']
        client_secret = config['client_secret']

    artist_link = input("Enter Spotify Artist Link: ")
    artist_id = artist_link.split('/')[-1].split('?')[0]

    token = get_token(client_id, client_secret)
    if not token:
        print('Failed to get token')
        return

    albums = fetch_albums(token, artist_id)
    details = {album['id']: fetch_album_details(token, album['id']) for album in albums}
    format_data(token, albums, details)

if __name__ == "__main__":
    main()
