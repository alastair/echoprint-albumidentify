import util
from proxies import artist_proxy
from results import make_results

class Artist(artist_proxy):
    """An Artist object (loosely covers http://beta.developer.echonest.com/artist.html)
    
    Create an artist object like so:
        a = artist.Artist('ARH6W4X1187B99274F')
    
    Args:
        **id**: Echo Nest Artist ID
        **name**: Artist Name
    
    """
    def __init__(self, id, **kwargs):
        super(Artist, self).__init__(id, **kwargs)
    
    def __repr__(self):
        return "<%s - %s>" % (self.type.encode('utf-8'), self.name.encode('utf-8'))
    
    def __str__(self):
        return self.name.encode('utf-8')
    
    def get_hotttnesss(self, cache=True):
        if not (cache and ('hotttnesss' in self.cache)):
            response = self.get_attribute('hotttnesss', id=self.id)
            self.cache['hotttnesss'] = make_results('hotttnesss', response, lambda x: x['artist']['hotttnesss'])
        return self.cache['hotttnesss']
    
    hotttnesss = property(get_hotttnesss)
    
    def get_audio(self, results=15, start=0, cache=True):
        if not (cache and ('audio' in self.cache)):
            response = self.get_attribute('audio', id=self.id, results=results, start=start)
            self.cache['audio'] = make_results('audio', response, lambda x: x['audios']['audio'])
        return self.cache['audio']
    
    audio = property(get_audio)
    
    def get_biographies(self, results=15, start=0, license='unknown', cache=True):
        if not (cache and ('biographies' in self.cache)):
            response = self.get_attribute('biographies', id=self.id, results=results, start=start)
            self.cache['biographies'] = make_results('biographies', response, lambda x: x['biographies']['biography'])
        return self.cache['biographies']
    
    biographies = property(get_biographies)    
    
    def get_blogs(self, results=15, start=0, cache=True):
        if not (cache and ('blogs' in self.cache)):
            response = self.get_attribute('blogs', id=self.id, results=results, start=start)
            self.cache['blogs'] = make_results('blogs', response, lambda x: x['blogs']['blog'])
        return self.cache['blogs']
    
    blogs = property(get_blogs)
       
    def get_familiarity(self, cache=True):
        if not (cache and ('familiarity' in self.cache)):
            response = self.get_attribute('familiarity', id=self.id)
            self.cache['familiarity'] = make_results('familiarity', response, lambda x: x['artist']['familiarity'])
        return self.cache['familiarity']
    
    familiarity = property(get_familiarity)    
    
    def get_images(self, results=15, start=0, license='unknown', cache=True):
        if not (cache and ('images' in self.cache)):
            response = self.get_attribute('images', id=self.id, results=results, start=start)
            self.cache['images'] = make_results('images', response, lambda x: x['images']['image'])
        return self.cache['images']
    
    images = property(get_images)    
    
    def get_news(self, results=15, start=0, cache=True):
        if not (cache and ('news' in self.cache)):
            response = self.get_attribute('news', id=self.id, results=results, start=start)
            self.cache['news'] = make_results('news', response, lambda x: x['news']['news'])
        return self.cache['news']
    
    news = property(get_news)
    
    def get_reviews(self, results=15, start=0, cache=True):
        if not (cache and ('reviews' in self.cache)):
            response = self.get_attribute('reviews', id=self.id, results=results, start=start)
            self.cache['reviews'] = make_results('reviews', response, lambda x: x['reviews']['review'])
        return self.cache['reviews']
    
    reviews = property(get_reviews)
    
    def get_similar(self, results=15, start=0, cache=True):
        if not (cache and ('similar' in self.cache)):
            response = self.get_attribute('similar', id=self.id, results=results, start=start)
            fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
            self.cache['similar'] = [Artist(**fix(a_dict)) for a_dict in response['artists']['artist']]
        return self.cache['similar']
    
    similar = property(get_similar)    
    
    def get_urls(self, cache=True):
        if not (cache and ('urls' in self.cache)):
            response = self.get_attribute('urls', id=self.id)
            self.cache['urls'] = make_results('urls', response, lambda x: x['urls'])
        return self.cache['urls']
    
    urls = property(get_urls)    
    
    def get_video(self, results=15, start=0, cache=True):
        if not (cache and ('video' in self.cache)):
            response = self.get_attribute('video', id=self.id, results=results, start=start)
            self.cache['video'] = make_results('video', response, lambda x: x['videos']['video'])
        return self.cache['video']
    
    video = property(get_video)


def search(query, results=15, buckets=[], limit=False, exact=False, sounds_like=False, type=None):
    kwargs = {}
    kwargs['query'] = query
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    if exact:
        kwargs['exact'] = 'true'
    if sounds_like:
        kwargs['sounds_like'] = 'true'
    if type:
        if type=='description':
            kwargs['type'] = 'description'
        elif type=='name':
            kwargs['type'] = 'name'
        else:
            pass
    
    """Search for artists"""
    result = util.callm("%s/%s" % ('artist', 'search'), kwargs)
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Artist(**fix(a_dict)) for a_dict in result['response']['artists']['artist']]

def top_hottt(start=0, results=15, buckets=[], limit=False):
    kwargs = {}
    if start:
        kwargs['start'] = start
    if results:
        kwargs['results'] = results
    if buckets:
        kwargs['bucket'] = buckets
    if limit:
        kwargs['limit'] = 'true'
    
    """Get top hottt artists"""
    result = util.callm("%s/%s" % ('artist', 'top_hottt'), kwargs)
    fix = lambda x : dict((str(k), v) for (k,v) in x.iteritems())
    return [Artist(**fix(a_dict)) for a_dict in result['response']['artists']['artist']]    
