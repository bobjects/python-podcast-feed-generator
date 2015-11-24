#!/usr/bin/python

# =======================================================================
# Copyright Bobjects Incorporated 2015.
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at
# http://opensource.org/licenses/MIT)
# =======================================================================

import os
import re
import urllib
from cStringIO import StringIO


class Podcast(object):
	title = "My podcast"
	description = "Just some miscellaneous audio files"
	url = "http://localhost/podcast"
	mediaFileURLPrefix = "http://localhost/podcast/"
	mediaFileDirectoryPath = "."
	mediaFilePathRegexes = [".+mp3$", ".+MP3$", ".+wav$", ".+WAV$", ".+m4a$"]

	@property
	def mediaFilePaths(self):
		answer = []
		for filename in os.listdir(self.mediaFileDirectoryPath):
			for regex in self.mediaFilePathRegexes:
				if re.search(regex, filename):
					answer.append(filename)
		return answer

	def generate(self):
		print "Generating feed for '" + self.description
		# feedfile = open(self.feedFilePath, 'w')
		stringio = StringIO()
		stringio.write('<?xml version="1.0"?>\n')
		stringio.write(' <rss version="2.0">\n')
		stringio.write('  <channel>\n')
		stringio.write('   <title>' + self.title + '</title>\n')
		stringio.write('   <description>' + self.description + '</description>\n')
		stringio.write('   <copyright>Various</copyright>\n')
		stringio.write('   <link>' + self.url + '</link>\n')
		# stringio.write('   <pubDate>' + time.ctime() + '</pubDate>\n')

		for filename in self.mediaFilePaths:
			filenewname = filename.replace("&", "and")  # ampersands screw things up.  Actually mv the media file.
			if filename is not filenewname:
				os.rename(filename, filenewname)
				filename = filenewname
			print "adding " + filename
			stringio.write('   <item>\n')
			stringio.write('    <title>' + filename + '</title>\n')
			stringio.write('    <description>' + filename + '</description>\n')
			# stringio.write('    <pubDate>' + time.ctime() + '</pubDate>\n')
			# TODO:  Perhaps get the file size?
			stringio.write('    <enclosure url="' + self.mediaFileURLPrefix + urllib.quote(filename) + '" length="1000000" type="audio/mpeg"> </enclosure>\n')
			stringio.write('   </item>\n')

		stringio.write('  </channel>\n')
		stringio.write(' </rss>\n')
		stringio.write('')
		stringio.write('')
		answer = stringio.getvalue()
		stringio.close()
		print "done"
		print ""
		return answer


class PodcastFeedFile(object):
	feedFilePath = "./feed.xml"

	def __init__(self, aPodcast):
		self.podcast = aPodcast

	def generate(self):
		# TODO: will refactor Podcast generate() method.  For now, simply delegate.
		feedfile = open(self.feedFilePath, 'w')
		feedfile.write(self.podcast.generate())
		feedfile.close()


if __name__ == '__main__':
	# Define your podcasts here...
	podcast = Podcast()
	podcast.title = "MacBob2 Podcast"
	podcast.description = "Just some random MP3s on MacBob2"
	podcast.url = "http://localhost/podcast"
	podcast.mediaFileURLPrefix = "http://localhost/podcast/"
	podcastFeedFile = PodcastFeedFile(podcast)
	podcastFeedFile.feedFilePath = "./feed.xml"
	podcastFeedFile.generate()

	podcast = Podcast()
	podcast.title = "MacBob2 Video Podcast"
	podcast.description = "Just some random videos on MacBob2"
	podcast.url = "http://localhost/podcast"
	podcast.mediaFilePathRegexes = [".+m4v$", ".+M4V$", ".+mov$", ".+MOV$", ".+mp4$", ".+MP4$"]
	podcast.mediaFileURLPrefix = "http://localhost/podcast/"
	podcastFeedFile = PodcastFeedFile(podcast)
	podcastFeedFile.feedFilePath = "./feedvideo.xml"
	podcastFeedFile.generate()

