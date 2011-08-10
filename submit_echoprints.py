#!/usr/bin/python

import sys
import os

import tag
from musicbrainz import musicbrainz
import echonest

import conf

musicbrainz.auth(conf.mb_user, conf.mb_pass)
musicbrainz.hostname = "echoprint.musicbrainz.org"

def submit_dir(directory):
    if not os.path.isdir(directory):
        print "Skipping (not a direcory):", directory

    print "Processing directory", directory

    files = os.listdir(directory)
    metadata = {}
    for f in sorted(files):
        filename = os.path.join(directory, f)
        if os.path.splitext(filename)[1] in tag.supported_extensions:
            metadata.update(get_metadata(filename))

    if len(metadata):    
        print "Submitting...",
        try:
            resp = musicbrainz.submit_echoprints(metadata)
        except musicbrainz.urllib2.HTTPError:
            print "Auth failed. Is your password 'mb'?"
            return
        if resp["message"]["text"] == "OK":
            print "done"
        else:
            print "Error submitting:", resp["message"]["text"]
    else:
        print "No files found"

def get_metadata(filename):
    print os.path.basename(filename)
    try:
        trackid = tag.read_tags(filename)['MUSICBRAINZ_TRACKID']
    except:
        print "    Track has no tagged musicbrainz track id"
        return {}

    echoprint = echonest.fingerprint(filename)
    if echoprint:
        print "    %s:%s" % (trackid, echoprint)
        return {trackid:echoprint}
    else:
        print "    Not found in echoprint"
        return {}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s [directories ...]" % sys.argv[0]
        sys.exit(1)
    for d in sys.argv[1:]:
        submit_dir(d)
