#!/usr/bin/python

import sys
import os
import fp
import echonest
import lookups

supported_types = [".mp3", ".ogg", ".flac"]

def mb_lookup(artistid, releasename):
	artist_profile = echonest.artist_profile(artistid)
	if artist_profile["response"]["artist"].get("musicbrainz", None) is not None:
		mbid = artist_profile["response"]["artist"]["musicbrainz"].split(":")[2]
		# print "mbid",mbid
		releases = lookups.search_for_release_group_with_artistid(mbid, releasename)
		for r in releases:
			print "      * %s.html" % r.getReleaseGroup().getId()
	#echonest.pp(artist_profile)

def release_check(artists, count):
	for a in artists.keys():
		if len(artists[a]["releases"]) > 0:
			print "Considering artist %s (%s)" % (a, artists[a]["name"])
			releases = artists[a]["releases"]
			for r in releases.keys():
				print "    %s" % r
				prob = float(releases[r])/count*100
				print "    probability: %d%%" % (prob)
				if prob > 70:
					print "      I think it could be this one.  Here are some musicbrainz releases"
					mb_lookup(a, r)


def main(dir):
	if os.path.isfile(dir):
			query = fp.fingerprint(dir)
			echonest.pp(echonest.fp_lookup(query))

	else:
		matches = {}
		artists = {}
		count = 0
		for f in os.listdir(dir):
			if os.path.splitext(f)[1] not in supported_types:
				print "skipping",f
				continue
			count +=1
			query = fp.fingerprint(os.path.join(dir, f))
			match = echonest.fp_lookup(query)
			matches[f] = match
			for song in match["results"]:
				artist = song["artistID"]
				release = song["release"]
				aname = song["artist"]
				if artist in artists:
					if release in artists[artist]["releases"]:
						artists[artist]["releases"][release] += 1
					else:
						artists[artist]["releases"][release] = 1
				else:
					artists[artist] = {"releases": {}, "name": aname}
		newartists = {}
		for a in artists.keys():
			if len(artists[a]["releases"]) > 0:
				newartists[a] = artists[a]
		echonest.pp(newartists)
		release_check(newartists, count)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >>sys.stderr, "usage: %s <dir>" % sys.argv[0]
		sys.exit(1)
	else:
		main(sys.argv[1])
		#release_check({"ARD4C1I1187FB4B0C3": {"name": "Pink Floyd", "releases": { "Dark Side Of The Moon": 10, "The Dark Side Of The Moon": 7  }}}, 9)
