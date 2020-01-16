#!/usr/bin/env python

# created by shuichinet https://gist.github.com/shuichinet
# forked from https://gist.github.com/shuichinet/8159878 21 Nov 2015
# using minor edits by fcrimins https://www.reddit.com/user/fcrimins from https://www.reddit.com/r/google/comments/2xzgyv/remove_duplicate_songs_from_google_play_music/csh6mrh
# also using clever edits by Morgan Gothard https://medium.com/@mgothard
# updated for Python 3.5 by John M. Kuchta https://medium.com/@sebvance 22 Nov 2016 (hey I was busy)
# compiled by John M. Kuchta https://medium.com/@sebvance
# thanks to shuichinet, fcrimins and Mr. Gothard for their work

# Edited and converted to Python 3.7 by Sam Cross https://github.com/sam-cross
# Now using OAuth login!

# License: MIT

from gmusicapi import Mobileclient
from getpass import getpass

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
		client.perform_oauth(open_browser=True)
		return True

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

	# hsongs = []
	# for song in all_songs:
	# 	if song.get('artist') == 'Hundredth':
	# 		hsongs.append([song.get('artist'),
	# 			song.get('album'),
	# 			song.get('title'),
	# 			song.get('discNumber'),
	# 			song.get('trackNumber'),
	# 			'Extra info follows',
	# 			song.get('genre'),
	# 			song.get('trackNumber'),
	# 			song.get('playCount')])

	# def tS(el):
	# 	return el[1]
	# for s in sorted(hsongs, key=tS): print(s)
	# exit()

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
			if mode_new: # by playCount
				if songs[key]['play_count'] < play_count:
					songs_old[key] = songs[key]
					songs[key] = { 'id': song_id, 'recent_timestamp': recent_timestamp, 'play_count': play_count }
				else:
					songs_old[key] = { 'id': song_id, 'recent_timestamp': recent_timestamp, 'play_count': play_count }
			else:
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
		
		if input('Delete duplicate songs? (y/N): ') is 'y':
			print('Deleting songs ...')
			#print('\t' + str(old_song_ids))
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