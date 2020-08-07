from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pickle
import spottransfer
from sys import exit
import PySimpleGUI as sg

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def spotify_transfer(username): #"qszc84oktwgj54ui831wfgvwz"
	clientid = "e6b6ffba9aa741bb80d007785f2162e5"
	clientsecret = "ccceb9144379499082630c0df67f6888"
	redirect = 'http://localhost:7777/callback'
	scope = 'playlist-modify-private'
	spotify = spottransfer.Spotify(username, clientid, clientsecret, redirect, scope)
	spotify.get_userid()
	playlist_id = spotify.create_playlist("VK dump", "These are my songs from VK")
	try:
		songs = load_obj("D:/botpy/parse/songs")
	except:
		print("ERROR: songs file not found")

	while True:
		try:
			song = songs.popitem()
		except:
			break
		song_id = spotify.search_song(song[0] + " " + song[1])
		if song_id != None:
			spotify.add_song_to_playlist(playlist_id, song_id)

sg.theme('DarkAmber')
layout = [  [sg.Text('VK Username'), sg.InputText()], 
			[sg.Text('Vk Password'), sg.InputText()], 
			[sg.Text('Spotify Username'), sg.InputText()],
			[sg.Button('Ok'), sg.Button('Cancel')] 
		]

window = sg.Window('Vpotify', layout)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel':
		break
	if event == 'Ok':
		print(values)
		break

window.close()

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
try:
	driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
	driver.get("https://vk.com/")
	assert "ВКонтакте" in driver.title
	print("Opened VK!")
except:
	print("Something wrong happened!")
	exit(1)

username = values[0]
username_field = driver.find_element_by_id('index_email')
username_field.clear()
username_field.send_keys(username)

password = values[1]
password_field = driver.find_element_by_id('index_pass')
password_field.clear()
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)
print("Logged in!")

print("Waiting to load...")
sleep(2)
driver.find_element_by_id("l_aud").click() 
sleep(2)
print("Opened audios!")

SCROLL_PAUSE_TIME = 0.5

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	sleep(SCROLL_PAUSE_TIME)
	new_height = driver.execute_script("return document.body.scrollHeight")
	if new_height == last_height:
		print("Got to the bottom!")
		break
	last_height = new_height

print("Getting songs...")
names_elem = driver.find_elements_by_class_name("audio_row__title_inner")
artists_elem = driver.find_elements_by_class_name("audio_row__performers")
names = []
artists = []
for name in names_elem:
	names.append(name.get_attribute('innerHTML'))
for artist in artists_elem:
	html = BeautifulSoup(artist.get_attribute('innerHTML'), features="lxml")
	artists.append(html.get_text())
songs = {}
for name in names:
	songs.update({name:artists[names.index(name)]})
print("Found ", len(songs), " songs")
save_obj(songs, "songs")
driver.close()
print("Songs file was created in the script repository")
spotify_transfer(values[2])
print("Finished! All available songs were added to your private Spotify playlist")

layout = [  [], 
			[sg.Text('Finished! All available songs were added to your private Spotify playlist')],
			[sg.Button('Ok')],
			[] 
		]

window = sg.Window('Vpotify', layout)

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Ok':
		break