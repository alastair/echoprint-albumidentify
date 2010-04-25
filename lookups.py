import musicbrainz2 as mb
import musicbrainz2.webservice as ws
import musicbrainz2.model as model
import time
import re
import pickle
import os
import memocache
import util

AMAZON_LICENSE_KEY='1WQQTEA14HEA9AERDMG2'

# 0 = No profile information
# 1 = Delay information only
# 2 = Delay and webquery time
PROFILE=2
MINDELAY=1.25

startup = time.time()
lastwsquery = {}

assert map(int,mb.__version__.split(".")) >= [0,6,0], "Need python-musicbrainz2 >= v0.6.0"

SUBMIT_SUPPORT = map(int, mb.__version__.split(".")) >= [0,7,0]

webservices = {
	"musicbrainz" : {
		"freequeries" : 13,
	},
}

def musicbrainz_retry():
        """ Decorator to retry failures in musicbrainz calls.

            For example, a 503 will result in a 20 second cooldown. A urlopen timeout
            will simply be tried again.
        """
        def ws_backoff(func):
                def backoff_func(*args, **kwargs):
                        global lastwsquery
                        try:
                                return func(*args,**kwargs)
                        except ws.WebServiceError,e:
                                if (e.msg.find("503") != -1):
                                        util.update_progress("Caught musicbrainz 503, waiting 20s and trying again...")
                                else:
					# A bare raise will reraise the current exception
                                        raise
                        except ws.ConnectionError,e:
                                if (e.msg.find("urlopen error timed out") != -1):
                                        util.update_progress("Caught musicbrainz urlopen timeout. Retrying...")
                                else:
                                        raise

                        time.sleep(20)
                        # Reset the timer delayed uses so that we don't
                        # end up with a bunch of queries causing
                        # another 503
                        lastwsquery["musicbrainz"]=time.time()
                        # Retry the call
                        return func(*args,**kwargs)

                backoff_func.__name__=func.__name__
                return backoff_func
        return ws_backoff

def delayed(webservice="default"):
	"Decorator to make sure a function isn't called more often than once every 2 seconds. used to space webservice calls"
	assert webservice in webservices,"Unknown webservice"
	def delayed2(func):
		def delay(*args,**kwargs):
			global lastwsquery
			if webservice not in lastwsquery:
				lastwsquery[webservice]=startup

			lastwsquery[webservice] = max(
				lastwsquery[webservice],
				time.time() - webservices[webservice]["freequeries"] * MINDELAY)
				
			wait=0
			if time.time()-lastwsquery[webservice]<MINDELAY:
				wait=MINDELAY-(time.time()-lastwsquery[webservice])
				if PROFILE==1:
					util.update_progress("Waiting %.2fs for %s" % (wait,func.__name__))
				time.sleep(wait)
			t=time.time()
			ret=func(*args,**kwargs)
			if PROFILE>=2:
				util.update_progress("%s took %.2fs (after a %.2fs wait)" % (func.__name__,time.time()-t,wait))
			lastwsquery[webservice]+=MINDELAY
			return ret
		delay.__name__="delayed_"+func.__name__
		return delay
	return delayed2

trackincludes = {
	"artist"	: True,
	"releases"	: True,
	"puids"		: True,
	"artistRelations": False,
	"releaseRelations": False,
	"trackRelations": False,
	"urlRelations"	: False,
	"tags"		: True,
}
if SUBMIT_SUPPORT:
	trackincludes["isrcs"]=True
	
@memocache.memoify()
@musicbrainz_retry()
@delayed("musicbrainz")
def get_track_by_id(id):
	q = ws.Query()
	results = []
        includes = ws.TrackIncludes(**trackincludes)

	t = q.getTrackById(id_ = id, include = includes)
	return t

@memocache.memoify()
@musicbrainz_retry()
@delayed("musicbrainz")
def get_release_by_releaseid(releaseid):
	""" Given a musicbrainz release-id, fetch the release from musicbrainz. """
	q = ws.Query()
	requests = {
		"artist" 	: True,
		"counts" 	: True,
		"tracks" 	: True,
		"releaseEvents" : True,
		"releaseRelations" : True,
		"urlRelations"	: True,
		"tags"		: True,
	}
        if SUBMIT_SUPPORT:
		requests["isrcs"] = True
	includes = ws.ReleaseIncludes(**requests)
	return q.getReleaseById(id_ = releaseid, include=includes)

@memocache.memoify()
@musicbrainz_retry()
@delayed("musicbrainz")
def get_track_artist_for_track(track):
	""" Returns the musicbrainz Artist object for the given track. This may
		require a webservice lookup
	"""
	if track.artist is not None:
		return track.artist

	q = ws.Query()
	includes = ws.TrackIncludes(artist = True)
	t = q.getTrackById(track.id, includes)

	if t is not None:
		return t.artist

	return None

def search_for_release_with_artistid(artistid, query):
	""" Search for all releases with a given artist id and a query for release name"""

	q = ws.Query()
	rfilter = ws.ReleaseFilter(artistId=artistid, title=query)
	r = q.getReleases(rfilter)
	return r

def search_for_release_group_with_artistid(artistid, query):
	""" Search for all releases with a given artist id and a query for release name"""

	q = ws.Query()
	rfilter = ws.ReleaseGroupFilter(artistId=artistid, title=query)
	r = q.getReleaseGroups(rfilter)
	return r

if __name__ == "__main__":
	print search_for_release_with_artistid("83d91898-7763-47d7-b03b-b92132375c47", "Dark side of the moon")
