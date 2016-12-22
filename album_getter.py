import spotipy
import spotipy.util as util
from os.path import expanduser
from os import path

def album_string(album):
    album_name = str(album['name'].encode('utf8'))
    artist_name = ', '.join([ str(artist['name'].encode('utf8')) for artist in album['artists'] ])
    album_string = album_name + ' - ' + artist_name
    if 'release_date' in album.keys():
        album_string += ' (' + str(album['release_date'].split('-')[0].encode('utf8')) + ')'
    return album_string

def track_album_string(track):
    return album_string({'name':track['album']['name'], 'artists':track['artists']})

def write_album_to_file(album):
    if '(2016)' in album:
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

clear_album_list_files()
username = '123845899'
token = util.prompt_for_user_token(username)
if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if '2016' in playlist['name']:
            print playlist['name']
            tracks = sp.user_playlist_tracks(username, playlist['id'])
            results = set()
            album_ids = set()
            for track in tracks['items']:
                if track['is_local']:
                    results.add(track_album_string(track['track']))
                else:
                    album_ids.add(track['track']['album']['id'])
            for id in album_ids:
                results.add(album_string(sp.album(id)))
            for entry in results:
                write_album_to_file(entry)

