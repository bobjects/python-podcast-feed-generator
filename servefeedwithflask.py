#!/usr/bin/python

# =======================================================================
# Copyright Bobjects Incorporated 2015.
# Distributed under the MIT License.
# (See accompanying file LICENSE or copy at
# http://opensource.org/licenses/MIT)
# =======================================================================

from flask import Flask
from flask import Response
from generatefeed import Podcast

mediaFileDirectoryPath = "."

app = Flask(__name__, static_folder=mediaFileDirectoryPath)


# define feed functions here.
@app.route('/podcast/feed.xml')
def feed():
	podcast = Podcast()
	podcast.title = "MacBob2 Podcast"
	podcast.description = "Just some random MP3s on MacBob2"
	podcast.url = "http://localhost/podcast"
	podcast.mediaFileDirectoryPath = mediaFileDirectoryPath
	podcast.mediaFileURLPrefix = "http://localhost/podcast/"
	return Response(podcast.generate(), mimetype='application/xml')


@app.route('/podcast/feedvideo.xml')
def feedvideo():
	podcast = Podcast()
	podcast.title = "MacBob2 Video Podcast"
	podcast.description = "Just some random videos on MacBob2"
	podcast.url = "http://localhost/podcast"
	podcast.mediaFileDirectoryPath = mediaFileDirectoryPath
	podcast.mediaFileURLPrefix = "http://localhost/podcast/"
	podcast.mediaFilePathRegexes = [".+m4v$", ".+M4V$", ".+mov$", ".+MOV$", ".+mp4$", ".+MP4$"]
	return Response(podcast.generate(), mimetype='application/xml')


# This route is for serving the media files statically.
@app.route('/podcast/<path:path>')
def static_proxy(path):
	# send_static_file will guess the correct MIME type
	return app.send_static_file(path)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=80)
