#!/usr/bin/python

import sys
import os
import echonest
from musicbrainz import musicbrainz

musicbrainz.hostname = "echoprint.musicbrainz.org"

supported_types = [".mp3", ".ogg", ".flac"]

"""
def artist_enid_to_mbid(enid):
	artist_profile = echonest.artist_profile(enid)
	foreign = artist_profile["response"]["artist"]["foreign_ids"]
	mbid = foreign[0]["foreign_id"].split(":")[2]
	return mbid

def release_check(artists):
	for artist in artists.keys():
		# mbid of this artist
		mbid = artist_enid_to_mbid(artist)
		# map of each song -> all the releases it comes on
		songtorelease = {}
		for song in artists[artist]:
			title = song["title"]
			mbtracks = lookups.search_for_track_with_artistid(mbid, title)
			trackid = song["id"]
			songtorelease[trackid] = [[t.getTrack().getId(), t.getTrack().getReleases()[0].getId()] for t in mbtracks]

		# map of releases -> all songs we have on that release
		rels = {}
		for f in songtorelease.keys():
			for r in songtorelease[f]:
				release = r[1]
				if release in rels:
					rels[release].append([f, r[0]])
				else:
					rels[release] = [[f, r[0]]]
		#print "rels:"
		#echonest.pp(rels)
		return rels

def print_map(rels, filemap, count):
	for k in rels.keys():
		r = rels[k]
		if len(r) == count:
			mbrel = lookups.get_release_by_releaseid(k)
			relname = mbrel.getTitle()
			artistname = mbrel.getArtist().getName()
			print "Could be release: %s, by %s (%s.html)" % (relname, artistname, k)
			count = 1
			for track in mbrel.getTracks():
				filename = "(missing)"
				for [a,b] in r:
					if b == track.getId():
						filename = filemap[a]
				ext = os.path.splitext(filename)[1]
				print "%s --> %d - %s - %s%s" % (filename, count, artistname, track.getTitle(), ext)
				count += 1
"""

def main(dir):
    if os.path.isfile(dir):
        pass
    else:
        matches = {}
        artists = {}
        count = 0
        filemap = {}
        for f in os.listdir(dir):
            if os.path.splitext(f)[1] not in supported_types:
                print "skipping",f
                continue
            count +=1
            echoprint = echonest.fingerprint(os.path.join(dir, f))
            if echoprint:
                mb_rec = musicbrainz.get_recordings_by_echoprint(echoprint, ["releases"])
                print mb_rec

        #rels = release_check(artists)
        #print_map(rels, filemap, count)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >>sys.stderr, "usage: %s <dir>" % sys.argv[0]
		sys.exit(1)
	else:
		main(sys.argv[1])
