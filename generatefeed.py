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
		feedfile = StringIO()
		feedfile.write('<?xml version="1.0"?>\n')
		feedfile.write(' <rss version="2.0">\n')
		feedfile.write('  <channel>\n')
		feedfile.write('   <title>' + self.title + '</title>\n')
		feedfile.write('   <description>' + self.description + '</description>\n')
		feedfile.write('   <copyright>Various</copyright>\n')
		feedfile.write('   <link>' + self.url + '</link>\n')
		# feedfile.write('   <pubDate>' + time.ctime() + '</pubDate>\n')

		for filename in self.mediaFilePaths:
			filenewname = filename.replace("&", "and")  # ampersands screw things up.  Actually mv the media file.
			if filename is not filenewname:
				os.rename(filename, filenewname)
				filename = filenewname
			print "adding " + filename
			feedfile.write('   <item>\n')
			feedfile.write('    <title>' + filename + '</title>\n')
			feedfile.write('    <description>' + filename + '</description>\n')
			# feedfile.write('    <pubDate>' + time.ctime() + '</pubDate>\n')
			# TODO:  Perhaps get the file size?
			feedfile.write('    <enclosure url="' + self.mediaFileURLPrefix + urllib.quote(filename) + '" length="1000000" type="audio/mpeg"> </enclosure>\n')
			feedfile.write('   </item>\n')

		feedfile.write('  </channel>\n')
		feedfile.write(' </rss>\n')
		feedfile.write('')
		feedfile.write('')
		answer = feedfile.getvalue()
		feedfile.close()
		print "done"
		print ""
		return answer


class PodcastFeedFile(object):
	podcast = Podcast()
	feedFilePath = "./feed.xml"

	@property
	def title(self):
		return self.podcast.title

	@title.setter
	def title(self, aString):
		self.podcast.title = aString

	@property
	def description(self):
		return self.podcast.description

	@description.setter
	def description(self, aString):
		self.podcast.description = aString

	@property
	def url(self):
		return self.podcast.url

	@url.setter
	def url(self, aString):
		self.podcast.url = aString

	@property
	def mediaFileURLPrefix(self):
		return self.podcast.mediaFileURLPrefix

	@mediaFileURLPrefix.setter
	def mediaFileURLPrefix(self, aString):
		self.podcast.mediaFileURLPrefix = aString

	@property
	def mediaFileDirectoryPath(self):
		return self.podcast.mediaFileDirectoryPath

	@mediaFileDirectoryPath.setter
	def mediaFileDirectoryPath(self, aString):
		self.podcast.mediaFileDirectoryPath = aString

	@property
	def mediaFilePathRegexes(self):
		return self.podcast.mediaFilePathRegexes

	@mediaFilePathRegexes.setter
	def mediaFilePathRegexes(self, aString):
		self.podcast.mediaFilePathRegexes = aString

	def generate(self):
		# TODO: will refactor Podcast generate() method.  For now, simply delegate.
		feedfile = open(self.feedFilePath, 'w')
		feedfile.write(self.podcast.generate())
		feedfile.close()


if __name__ == '__main__':
	# Define your podcasts here...
	podcastFeedFile = PodcastFeedFile()
	podcastFeedFile.title = "MacBob2 Podcast"
	podcastFeedFile.description = "Just some random MP3s on MacBob2"
	podcastFeedFile.url = "http://localhost/podcast"
	podcastFeedFile.mediaFileURLPrefix = "http://localhost/podcast/"
	podcastFeedFile.feedFilePath = "./feed.xml"
	podcastFeedFile.generate()

	podcastFeedFile = PodcastFeedFile()
	podcastFeedFile.title = "MacBob2 Video Podcast"
	podcastFeedFile.description = "Just some random videos on MacBob2"
	podcastFeedFile.url = "http://localhost/podcast"
	podcastFeedFile.mediaFileURLPrefix = "http://localhost/podcast/"
	podcastFeedFile.feedFilePath = "./feedvideo.xml"
	podcastFeedFile.mediaFilePathRegexes = [".+m4v$", ".+M4V$", ".+mov$", ".+MOV$", ".+mp4$", ".+MP4$"]
	podcastFeedFile.generate()

