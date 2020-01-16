#!/usr/bin/env python

#### Credits
# Original code by shuichinet (unfortunately lost to the internet)
# Updated by John M. Kuchta https://medium.com/@sebvance
# Thank you to shuichinet, Mr. Gothard, and Mr. Kuchta for their work!

# Converted for compatibility with Python 3.7 by Sam Cross https://github.com/sam-cross
# Now with OAuth login and additional options.

# Visit https://github.com/sam-cross/delete-google-music-duplicates

# License: MIT

try:
	from gmusicapi import Mobileclient
except:
	print("You're missing gmusicapi. Please install it with\n\tpip install gmusicapi\nand then run this again!")
	exit()

# True: Delete tracks with lower playcount, instead of most recently uploaded
mode_new = True

client = Mobileclient()
logged_in = False

def loginflow():
	if (client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)):
		print("Logged in")
		return True
	else:
		print("Couldn't log in automatically. Try logging in with your browser.")
		return client.perform_oauth(open_browser=True)

while (not logged_in):
	logged_in = loginflow()

run_count = 0

def get_remove_dupes(previous_run_count):
	run_count = previous_run_count + 1
	if (run_count > 3):
		print('Run multiple times - won\'t automatically run again.')
		exit()

	print('Getting a list of your songs...')
	all_songs = client.get_all_songs()
	songs = {}
	songs_old = {}

	for song in all_songs:
		song_id = song.get('id')
		recent_timestamp = song.get('recentTimestamp')
		play_count = song.get('playCount')

		# Create key for current song
		if song.get('discNumber') is None:
			discnum = 1
		else:
			discnum = song.get('discNumber')
		if discnum is 0:
			discnum = 1
		if song.get('trackNumber') is None:
			tracknum = 0
		else:
			tracknum = song.get('trackNumber')
		
		key = "%s: %d-%02d %s" % ( song.get('album'), discnum, tracknum, song.get('title') )
		
		# If current song is in the new_songs list
		# Compare keys
		if key in songs:
			if mode_new: # by play count
				if songs[key]['play_count'] < play_count:
					songs_old[key] = songs[key]
					songs[key] = { 'id': song_id, 'recent_timestamp': recent_timestamp, 'play_count': play_count }
				else:
					songs_old[key] = { 'id': song_id, 'recent_timestamp': recent_timestamp, 'play_count': play_count }
			else: # by most recently played
				if songs[key]['recent_timestamp'] < recent_timestamp:
					songs_old[key] = songs[key]
					songs[key] = { 'id': song_id, 'recent_timestamp': recent_timestamp, 'play_count': play_count }
				else:
					songs_old[key] = { 'id': song_id, 'recent_timestamp': recent_timestamp, 'play_count': play_count }
		
		songs[key] = { 'id': song_id, 'recent_timestamp': recent_timestamp, 'play_count': play_count }

	if len( songs_old ):
		print('Duplicate songs')
		
		old_song_ids = []
		
		for key in sorted( songs_old.keys() ):
			old_song_ids.append( songs_old[key]['id'] )
			print('\t' + str(key.encode('utf-8')))

		print('\nNumber of duplicates: ' + str(len(songs_old)))

		print('The following will delete all the above IRRECOVERABLY.')
		print('Only a single copy of the above tracks will remain.')
		print('Please be sure you have backups of your music, just in case!')
		
		if input('Delete duplicate songs? (y/N): ') is 'y':
			print('Deleting songs ...')
			client.delete_songs( old_song_ids )
			print('Done! Checking again just in case...')
			get_remove_dupes(run_count)
		else:
			print('Okay - nothing will be deleted.')
			exit()
	else:
		print('No duplicates found!')
		exit()

get_remove_dupes(run_count)
exit()