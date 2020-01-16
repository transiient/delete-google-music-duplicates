#!/usr/bin/env python

#### Credits
# Original code by shuichinet (unfortunately lost to the internet)
# Updated by John M. Kuchta https://medium.com/@sebvance
# Thank you to shuichinet, Mr. Gothard, and Mr. Kuchta for their work!

# Converted for compatibility with Python 3.7 by Sam Cross https://github.com/sam-cross
# Now with OAuth login and additional options.

# Visit https://github.com/sam-cross/delete-google-music-duplicates

# License: MIT

try: from gmusicapi import Mobileclient
except:
	print("You're missing gmusicapi. Please install it with\n\tpip install gmusicapi\nand then run this again!")
	exit()
try: import sys, os
except:
	print("There was an error importing the sys and os packages.")
	exit()

client = Mobileclient()
logged_in = False
# True: Delete tracks with lower playcount, instead of most recently uploaded
mode_new = True

def printv(string):
	if (cmd_args.v):
		print(string)

def e_fatal(err):
	print("Error: " + err)
	exit()

# Valid command-line arguments
cmd_args = {
	'-s': False, # Safety mode - disable track deletion
	'-v': False, # Verbose mode - log EVERYTHING
	'-o': False	# Output duplicates to file
}

def set_cmd_args():
	if len(sys.argv) > 1:
		for i in range(1, len(sys.argv)):
			if sys.argv[i] == '-o':
				if not os.path.exists(os.path.basedir(sys.argv[i+1])):
					e_fatal("Output path does not exist.")
				else:
					cmd_args['-o'] = os.path.abspath(sys.argv[i+1])
			elif sys.argv[i] == '-s':
				cmd_args['-s'] = True
			elif sys.argv[i] == '-v':
				cmd_args['-v'] = True

def loginflow():
	if (client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)):
		print("Logged in")
		return True
	else:
		print("Couldn't log in automatically. Try logging in with your browser.")
		return client.perform_oauth(open_browser=True)

while not logged_in:
	logged_in = loginflow()

run_count = 0

def delete_songs(songs_list):
	if (cmd_args['-s']):
		for song_key in songs_list:
			print("\t" + song_key)
	else:
		client.delete_songs(songs_list)

def find_duplicates(all_songs):
	songs_traversed = {}
	songs_del = {}

	for song in all_songs:
		song_id = song.get('id')
		song_recenttimestamp = song.get('recentTimestamp')
		song_playcount = song.get('playCount')

		# Create key for current song
		if song.get('discNumber') == None or song.get('discNumber') == 0:
			discnum = 1
		else:
			discnum = song.get('discNumber')
		if song.get('trackNumber') == None:
			tracknum = 0
		else:
			tracknum = song.get('trackNumber')
		
		key = "%s: %d-%02d %s" % (song.get('album'), discnum, tracknum, song.get('title'))

		# If current song is in the songs_traversed list
		if key in songs_traversed:
			if mode_new: # by play count
				if songs_traversed[key]['play_count'] < play_count:
					songs_del[key] = songs_traversed[key]
				else:
					songs_del[key] = { 'id': song_id, 'recent_timestamp': song_recenttimestamp, 'play_count': song_playcount }
			else: # by most recently played
				if songs_traversed[key]['recent_timestamp'] < song_recenttimestamp:
					songs_del[key] = songs_traversed[key]
				else:
					songs_del[key] = { 'id': song_id, 'recent_timestamp': song_recenttimestamp, 'play_count': song_playcount }
		songs_traversed[key] = { 'id': song_id, 'recent_timestamp': song_recenttimestamp, 'play_count': song_playcount }
	return songs_del

def get_remove_dupes(previous_run_count):
	run_count = previous_run_count + 1
	if (run_count > 3):
		print('Run multiple times - won\'t automatically run again.')
		exit()

	print('Finding duplicates')
	duplicates = find_duplicates(client.get_all_songs())

	if len( duplicates ):
		print('Duplicate songs:')
		
		duplicates_ids = []
		
		for key in sorted(duplicates.keys()):
			duplicates_ids.append( duplicates[key]['id'] )
			print('\t' + str(key.encode('utf-8')))

		print('\nNumber of duplicates: ' + str(len(duplicates)))

		print('The following will delete all the above IRRECOVERABLY.')
		print('Only a single copy of the above tracks will remain.')
		print('Please be sure you have backups of your music, just in case!')
		
		if input('Delete duplicate songs? (y/N): ') is 'y':
			print('Deleting songs ...')
			delete_songs(duplicates_ids)
			print('Done! Checking again just in case...')
			get_remove_dupes(run_count)
		else:
			print('Okay - nothing will be deleted.')
			exit()
	else:
		print('No duplicates found!')
		exit()

set_cmd_args()
get_remove_dupes(run_count)
exit()