'''
Reddit bot that searches r/listentothis for target genres and generates a playlist.txt
with the title of a matched post and the link to the song. The bot also saves the post
in the reddit account.

created by Eric Zhang 
'''

import praw 
import os
import sys


class Song(object):
	title = ""
	link = ""
    # initializer 
	def __init__(self, title, link):
		self.title = title
		self.link = link


def bot_login():
	# Authentication 
	# Creating Reddit instance using praw.ini file
	reddit = praw.Reddit('musicbot') 
	return reddit


def run_bot(reddit):
	# Main function of bot

	# array to store target genres 
	genre = [
			 "chill",
			 "Chill",
			 "electronic",
			 "Electronic",
			 "indie",
			 "Indie",
			 "rap",
			 "Rap",
			]

	related = []
	content = []

	# collect top 15 hot posts 
	submissions = reddit.subreddit('listentothis').hot(limit=15)

	# look through previous matches in playlist.txt and store in array
	if os.path.isfile('playlist.txt'):
		with open("playlist.txt", "r") as f:
			content = f.readlines()
	    	
		content = [x.strip() for x in content] 

	
	# loop through submissions in subreddit to find titles with specific genres 
	for submission in submissions:
		# check if submission title has a target genre in it
		if any(word in submission.title for word in genre):
			# check if submission has already been recorded
			if submission.url not in content:
				related.append(Song(submission.title,submission.url))
				# save the post in reddit account 
				submission.save()

	# open playlist.txt file to record title of new submission and link
	with open("playlist.txt", "a") as f:
		for song in related:
			f.write(song.title)
			f.write('\n')
			f.write(song.link)
			f.write('\n')
			f.write('\n')


def main():
	# set new encoding to recognize characters in reddit post title
	reload(sys)
	sys.setdefaultencoding('utf8')

	# run bot
	reddit = bot_login()
	run_bot(reddit)


if __name__ == '__main__':
		main() 

