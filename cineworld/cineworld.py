#!/usr/bin/env python

'''
Created on 17 Jul 2011

@author: oracal
'''

from cineworld_api_key import API_KEY
from fuzzywuzzy.fuzz import WRatio
from operator import itemgetter
from urllib import urlencode
import datetime

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
    
    #uses a certain cinema (O2) and a certain day when non specialist films show (Wednesday) to get a list of the latest box office films
    def get_box_office_films(self):
        today = datetime.date.today()
        next_wednesday = (today + datetime.timedelta((2 - today.weekday()) % 7)).strftime('%Y%m%d')
        films = self.get_films(cinema=79, date = next_wednesday)
        
        films = filter(lambda x: '3D' not in x['title'], films)
        for film in films:
            if '2D -' in film['title']:
                film['title']=film['title'][5:]
        return films
    
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
            self.get_film_list()
            
        for film in self.film_list:
            strength = WRatio(title, film['title'])
            if  strength > 80:
                film.update({u'strength':strength})
                films.append(film)
        films_sorted = sorted(films, key=itemgetter('strength'), reverse = True)
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
