import json
import requests
import spotipy.util as util
import pickle

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Spotify(object):
	def __init__(self, username, client_id, client_secret, redirect_uri, scope):
		self.username = username  #'your-spotify-username'
		self.client_id = client_id #'your-client-id'
		self.client_secret = client_secret #'your-client-secret'
		self.redirect_uri = redirect_uri #'http://localhost:7777/callback'
		self.scope = scope #'playlist-modify-private'
		self.token = util.prompt_for_user_token(username=self.username, scope=self.scope, client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri)
		print("Spotify initialised!")

	def get_userid(self):
		query = "https://api.spotify.com/v1/me"
		response = requests.get(
			query,
			headers = {
				"Authorization": "Bearer {}".format(self.token)
			}
		)
		response_json = response.json()
		self.user_id = response_json["id"]
		print("Got a user id!")
		return(response_json["id"])

	def create_playlist(self, name, description):
		request_body = json.dumps({
			"name":name,
			"description":description,
			"public": False
		})

		query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
		response = requests.post(
			query,
			data = request_body,
			headers = {
				"Authorization":"Bearer {}".format(self.token),
				"Content-Type":"application/json"
			}
		)
		response_json = response.json()
		print("Created a new playlist named", name)
		return(response_json["id"])

	def search_song(self, q, type = "track", limit = 1):
		query = "https://api.spotify.com/v1/search?q=" + q.replace(" ", "%20") + "&type=" + type + "&limit=" + str(limit)
		response = requests.get(
			query,
			headers = {
				"Authorization":"Bearer {}".format(self.token),
			}
		)
		try:
			response_json = response.json()
			response_json = response_json.popitem()
			response_json = response_json[1].get('items')
			response_json = response_json[0]
			songid = response_json['id']
			return(songid)
		except:
			print("Wasn't able to find ", q)
			return(None)

	def add_song_to_playlist(self, playlist_id, song_id):
		query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
		try:
			query = query + "?uris=spotify:track:" + song_id.pop(0)
			for id in song_id:
				query = query + ",spotify:track:" + id
		except:
			query = query + "?uris=" + song_id
		query = query + "&position=0"
		response = requests.post(
			query,
			headers = {
				"Authorization":"Bearer {}".format(self.token),
				"Content-Type":"application/json"
			}
		)
		response_json = response.json()
		print("Added", song_id, "to the playlist")
		print(response_json)

# username = input("Input Spotify username (i.e. qszc84surgfj54ui831wfgvw):\n")#"qszc84oktwgj54ui831wfgvwz"
# clientid = "e6b6ffba9aa741bb80d007785f2162e5"
# clientsecret = "ccceb9144379499082630c0df67f6888"
# redirect = 'http://localhost:7777/callback'
# scope = 'playlist-modify-private'
# spotify = Spotify(username, clientid, clientsecret, redirect, scope)
# spotify.get_userid()
# playlist_id = spotify.create_playlist("VK dump", "These are my songs from VK")
# try:
# 	songs = load_obj("D:/botpy/parse/songs")
# except:
# 	print("ERROR: songs file not found")

# while True:
# 	try:
# 		song = songs.popitem()
# 	except:
# 		break
# 	song_id = spotify.search_song(song[0] + " " + song[1])
# 	if song_id != None:
# 		spotify.add_song_to_playlist(playlist_id, song_id)