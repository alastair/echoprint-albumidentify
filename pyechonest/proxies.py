import util
from util import attrdict

class generic_proxy(attrdict):
    def __init__(self):
        self.cache = {}
    
    def get_attribute(self, method_name, use_cache=False, **kwargs):
        if use_cache and method_name in self.cache:
            return self.cache[method_name]
        result = util.callm("%s/%s" % (self.type, method_name), kwargs)
        self.cache[method_name] = result['response']
        return result['response']


class artist_proxy(generic_proxy):
    def __init__(self, identifier, **kwargs):
        super(artist_proxy, self).__init__()
        self.id = identifier
        self.type = 'artist'
        kwargs = dict((str(k), v) for (k,v) in kwargs.iteritems())
        self.__dict__.update(kwargs)
        if (not self.__dict__.get('name')):
            profile = self.get_attribute('profile', False, **{'id':self.id})
            self.__dict__.update(profile.get('artist'))

 

class song_proxy(generic_proxy):
    def __init__(self, identifier, **kwargs):
        super(song_proxy, self).__init__()
        self.id = identifier
        self.type = 'song'
        kwargs = dict((str(k), v) for (k,v) in kwargs.iteritems())
        self.__dict__.update(kwargs)
        if (not self.__dict__.get('title')) or (not self.__dict__.get('artist_name')) or (not self.__dict__.get('artist_id')):
            profile = self.get_attribute('profile', False, **{'id':self.id})
            self.__dict__.update(profile.get('songs').get('song')[0])
        


