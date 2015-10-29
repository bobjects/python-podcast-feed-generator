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


class Podcast(object):
	title = "My podcast"
	description = "Just some miscellaneous audio files"
	url = "http://localhost/podcast"
	mediaFileURLPrefix = "http://localhost/podcast/"
	mediaFileDirectoryPath = "."
	feedFilePath = "./feed.xml"
	# mediaFilePathRegexes = [".+m4v$", ".+M4V$", ".+mov$", ".+MOV$", ".+mp4$", ".+MP4$"]
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
		feedfile = open(self.feedFilePath, 'w')
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
		feedfile.close()
		print "done"
		print ""

# Define your podcasts here...
podcast = Podcast()
podcast.title = "MacBob2 Podcast"
podcast.description = "Just some random MP3s on MacBob2"
podcast.url = "http://localhost/podcast"
podcast.mediaFileURLPrefix = "http://localhost/podcast/"
podcast.feedFilePath = "./feed.xml"
podcast.generate()

podcast = Podcast()
podcast.title = "MacBob2 Video Podcast"
podcast.description = "Just some random videos on MacBob2"
podcast.url = "http://localhost/podcast"
podcast.mediaFileURLPrefix = "http://localhost/podcast/"
podcast.feedFilePath = "./feedvideo.xml"
podcast.mediaFilePathRegexes = [".+m4v$", ".+M4V$", ".+mov$", ".+MOV$", ".+mp4$", ".+MP4$"]
podcast.generate()

