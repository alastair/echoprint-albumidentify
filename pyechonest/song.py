import util
from proxies import song_proxy
from results import make_results

class Song(song_proxy):
    """An Song object (loosely covers http://beta.developer.echonest.com/song.html)
    
    Create a song object like so:
        s = song.Song(SOXZYYG127F3E1B7A2')
    
    Attributes:
        **id**: Echo Nest Song ID
        **title**: Song Title
        **artist_name**: Artist Name
        **artist_id**: Artist ID
        audio_summary: Audio Summary
        song_hotttnesss: Song Hotttnesss
        artist_hotttnesss: Artist Hotttnesss
        artist_familiarity: Artist Familiarity
        artist_location: Artist Location
        tracks: Tracks 
    
    """
    def __init__(self, id, **kwargs):
        super(Song, self).__init__(id, **kwargs)
    
    def __repr__(self):
        return "<%s - %s>" % (self.type.encode('utf-8'), self.title.encode('utf-8'))
    
    def __str__(self):
        return self.title.encode('utf-8')
    
        
    def get_audio_summary(self, cache=True):
        if not (cache and ('audio_summary' in self.cache)):
            response = self.get_attribute('profile', id=self.id, bucket='audio_summary')
            self.cache['audio_summary'] = make_results('audio_summary', response, lambda x: x['songs']['song'][0]['audio_summary'])
        return self.cache['audio_summary']
    
    audio_summary = property(get_audio_summary)
    
    def get_song_hotttnesss(self, cache=True):
        if not (cache and ('song_hotttnesss' in self.cache)):
            response = self.get_attribute('profile', id=self.id, bucket='song_hotttnesss')
            self.cache['song_hotttnesss'] = make_results('song_hotttnesss', response, lambda x: x['songs']['song'][0]['song_hotttnesss'])
        return self.cache['song_hotttnesss']
    
    song_hotttnesss = property(get_song_hotttnesss)
    
    def get_artist_hotttnesss(self, cache=True):
        if not (cache and ('artist_hotttnesss' in self.cache)):
            response = self.get_attribute('profile', id=self.id, bucket='artist_hotttnesss')
            self.cache['artist_hotttnesss'] = make_results('artist_hotttnesss', response, lambda x: x['songs']['song'][0]['artist_hotttnesss'])
        return self.cache['artist_hotttnesss']
    
    artist_hotttnesss = property(get_artist_hotttnesss)
    
    def get_artist_familiarity(self, cache=True):
        if not (cache and ('artist_familiarity' in self.cache)):
            response = self.get_attribute('profile', id=self.id, bucket='artist_familiarity')
            self.cache['artist_familiarity'] = make_results('artist_familiarity', response, lambda x: x['songs']['song'][0]['artist_familiarity'])
        return self.cache['artist_familiarity']
    
    artist_familiarity = property(get_artist_familiarity)
    
    def get_artist_location(self, cache=True):
        if not (cache and ('artist_location' in self.cache)):
            response = self.get_attribute('profile', id=self.id, bucket='artist_location')
            self.cache['artist_location'] = make_results('artist_location', response, lambda x: x['songs']['song'][0]['artist_location'])
        return self.cache['artist_location']
    
    artist_location = property(get_artist_location)
    
    def get_tracks(self, catalog='paulify', limit=False, cache=True):
        if not (cache and ('tracks' in self.cache)):
            kwargs = {
                'method_name':'profile',
                'bucket':['tracks'],
                'id':self.id,
            }
            if catalog:
                kwargs['bucket'].append('id:%s' % catalog)
            if limit:
                kwargs['limit'] = 'true'
            response = self.get_attribute(**kwargs)
            self.cache['tracks'] = make_results('track', response, lambda x: x['songs']['song'][0]['tracks']['track'])
        return self.cache['tracks']
    
    tracks = property(get_tracks) 


def search(title=None, artist=None, artist_id=None, combined=None, description=None, results=None, max_tempo=None, \
                min_tempo=None, max_duration=None, min_duration=None, max_loudness=None, min_loudness=None, \
                max_familiarity=None, min_familiarity=None, max_hotttnesss=None, min_hotttnesss=None, mode=None, \
                key=None, max_latitude=None, min_latitude=None, max_longitude=None, min_longitude=None, \
                sort=None, buckets=[], limit=False):
    """search for songs"""
    kwargs = {}
    if title:
        kwargs['title'] = title
    if artist:
        kwargs['artist'] = artist
    if artist_id:
        kwargs['artist_id'] = artist_id
    if combined:
        kwargs['combined'] = combined
    if description:
        kwargs['description'] = description
    if results:
        kwargs['results'] = results
    if max_tempo:
        kwargs['max_tempo'] = max_tempo
    if min_tempo:
        kwargs['min_tempo'] = min_tempo
    if max_duration:
        kwargs['max_duration'] = max_duration
    if min_duration:
        kwargs['min_duration'] = min_duration
    if max_loudness:
        kwargs['max_loudness'] = max_loudness
    if min_loudness:
        kwargs['min_loudness'] = min_loudness
    if max_familiarity:
        kwargs['max_familiarity'] = max_familiarity
    if min_familiarity:
        kwargs['min_familiarity'] = min_familiarity
    if max_hotttnesss:
        kwargs['max_hotttnesss'] = max_hotttnesss
    if min_hotttnesss:
        kwargs['min_hotttnesss'] = min_hotttnesss
    if mode:
        kwargs['mode'] = mode
    if key:
        kwargs['key'] = key
    if max_latitude:
        kwargs['max_latitude'] = max_latitude
    if min_latitude:
        kwargs['min_latitude'] = min_latitude
    if max_longitude:
        kwargs['max_longitude'] = max_longitude
    if min_longitude:
        kwargs['min_longitude'] = min_longitude
    if sort:
        kwargs['sort'] = sort
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    
    result = util.callm("%s/%s" % ('song', 'search'), kwargs)
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Song(**fix(s_dict)) for s_dict in result['response']['songs']['song']]

def profile(ids, buckets=[], limit=False):
    """get the profiles for multiple songs at once"""
    if not isinstance(ids, list):
        ids = [ids]
    kwargs = {}
    kwargs['id'] = ids
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    
    result = util.callm("%s/%s" % ('song', 'profile'), kwargs)
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Song(**fix(s_dict)) for s_dict in result['response']['songs']['song']]

