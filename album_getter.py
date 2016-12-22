import spotipy
import spotipy.util as util
from os.path import expanduser
from os import path
from credentials import *
from datetime import date

def album_string(album):
    album_name = str(album['name'].encode('utf8'))
    artist_name = ', '.join([ str(artist['name'].encode('utf8')) for artist in album['artists'] ])
    album_string = album_name + ' - ' + artist_name
    if 'release_date' in album.keys():
        album_string += ' (' + str(album['release_date'].split('-')[0].encode('utf8')) + ')'
    return album_string

def track_album_string(track):
    return album_string({'name':track['album']['name'], 'artists':track['artists']})

def write_album_to_file(album, year):
    if '(' + year + ')' in album:
        filename = 'released_this_year'
    else:
        filename = 'released_different_year'
    filepath = path.dirname(path.realpath(__file__))
    file = open(filepath + '/' + filename + '.txt', 'a')
    file.write(album + "\n")
    file.close()

def clear_album_list_files():
    filepath = path.dirname(path.realpath(__file__))
    file = open(filepath + '/released_this_year.txt', 'w')
    file.close()
    file = open(filepath + '/released_different_year.txt', 'w')
    file.close()

def get_unique_albums(username, playlist_id, offset):
    tracks = sp.user_playlist_tracks(username, playlist_id, offset=offset)
    results = set()
    album_ids = set()
    for track in tracks['items']:
        if track['is_local']:
            results.add(track_album_string(track['track']))
        else:
            album_ids.add(track['track']['album']['id'])
    for id in album_ids:
        results.add(album_string(sp.album(id)))
    return (results, tracks['next'])

clear_album_list_files()
username = raw_input("Spotify User ID: ")
if not username:
    username = SPOTIFY_USER_ID
year_in_consideration = raw_input("Year in consideration: ")
if not year_in_consideration:
    year_in_consideration = str(date.today().year)

token = util.prompt_for_user_token(username, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    results = set()
    for playlist in playlists['items']:
        if year_in_consideration in playlist['name']:
            print playlist['name']
            offset = 0
            (albums, more_tracks) = get_unique_albums(username, playlist['id'], offset)
            results = results | albums
            while more_tracks:
                offset += 100
                (albums, more_tracks) = get_unique_albums(username, playlist['id'], offset)
                results = results | albums
    for entry in results:
        write_album_to_file(entry, year_in_consideration)

            

