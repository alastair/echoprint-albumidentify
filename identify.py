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

def artist_enid_to_mbid(enid):
	artist_profile = echonest.artist_profile(enid)
	echonest.pp(artist_profile)
	foreign = artist_profile["response"]["artist"]["foreign_ids"]
	mbid = foreign[0]["foreign_id"].split(":")[2]
	return mbid

def release_check(artists, count):
	print artists
	for artist in artists.keys():
		mbid = artist_enid_to_mbid(artist)
		print mbid
		foo = {}
		for track in artists[artist]:
			mbtracks = lookups.search_for_track_with_artistid(mbid, track)
			foo[track] = [t.getTrack().getReleases()[0].getId() for t in mbtracks]
		echonest.pp(foo)

		# Releases
		rels = {}
		for f in foo.keys():
			for r in foo[f]:
				if r in rels:
					rels[r].append(f)
				else:
					rels[r] = [f]

		echonest.pp(rels)

def main(dir):
	if os.path.isfile(dir):
		query = fp.fingerprint(dir)
		match = echonest.fp_lookup(query)
		echonest.pp(match)
		id = match["response"]["songs"][0]["id"]
		artist = match["response"]["songs"][0]["artist_id"]
		title = match["response"]["songs"][0]["title"]
		echonest.pp(echonest.track_profile(id))
		echonest.pp(echonest.artist_profile(artist))
		artist_profile = echonest.artist_profile(artist)
		foreign = artist_profile["response"]["artist"]["foreign_ids"]
		mbid = foreign[0]["foreign_id"].split(":")[2]
		print "mbid",mbid
		tracks = lookups.search_for_track_with_artistid(mbid, title)
		print tracks
		for t in tracks:
			print t.getTrack().getReleases()[0].getId()

	else:
		matches = {}
		artists = {}
		count = 0
		for f in os.listdir(dir):
			if os.path.splitext(f)[1] not in supported_types:
				print "skipping",f
				continue
			count +=1
			code = fp.fingerprint(os.path.join(dir, f))
			match = echonest.fp_lookup(code)
			echonest.pp(match)
			matches[f] = match
			for song in match["response"]["songs"]:
				artist = song["artist_id"]
				title = song["title"]
				if artist in artists:
					artists[artist].append(title)
				else:
					artists[artist] = [title]
		release_check(artists, count)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >>sys.stderr, "usage: %s <dir>" % sys.argv[0]
		sys.exit(1)
	else:
		main(sys.argv[1])
