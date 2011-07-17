#!/usr/bib/env python

'''
Created on 17 Jul 2011

@author: oracal
'''

from cineworld_api_key import API_KEY
from fuzzywuzzy.fuzz import WRatio
from urllib import urlencode
from operator import itemgetter

try:
    import json
except ImportError:
    import simplejson as json
    
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
    
class CW(object):
    
    def __init__(self, api_key=''):
        if not api_key:
            self.api_key = API_KEY
        else:
            self.api_key = api_key
        base_url = 'http://www.cineworld.com/api/quickbook/'
        self.base_url = base_url
        self.cinemas_url = base_url + 'cinemas'
        self.films_url = base_url + 'films'
        self.dates_url = base_url + 'dates'
        self.performances = base_url + 'performances'
        
    def get_cinemas(self, **kwargs):
        return self.get_list('cinemas', self.cinemas_url, **kwargs)
    
    def get_films(self, **kwargs):
        return self.get_list('films', self.films_url, **kwargs)
    
    def get_film_list(self):
        self.film_list = self.get_films()
        return self.film_list
    
    def get_dates(self, **kwargs):
        return self.get_list('dates', self.dates_url, **kwargs)
    
    def get_performances(self, **kwargs):
        return self.get_list('performances', self.performances_url, **kwargs)
    
    def get_list(self, datatype, url, **kwargs):
        search_url = [url, '?']
        kwargs.update({'key': self.api_key})
        search_url.append(urlencode(kwargs))
        data = json.loads(urlopen(''.join(search_url)).read())
        return data[datatype]
    
    def film_search(self, title):
        films = []
        if not hasattr(self, 'film_list'):
            self.film_list = self.get_film_list()
            
        for film in self.film_list:
            strength = WRatio(title, film['title'])
            if  strength > 80:
                film.update({u'strength':strength})
                films.append(film)
        films_sorted = sorted(films, key=itemgetter('strength'))
        return films_sorted
        
    def get_film_id(self, title, three_dimensional=False):
        films = self.film_search(title)
        for film in films:
            if (film['title'].find('3D') is - 1) is not three_dimensional:
                return film['edi']
        return -1
    
    def get_film_info(self, edi):
        return self.get_films(film=edi, full='true')
    
    def get_cinemas_by_film(self, edi, **kwargs):
        return self.get_cinemas(film=edi, **kwargs)
    
    def get_cinema_info(self, id):
        self.get_cinemas(cinema=id, full='true')
