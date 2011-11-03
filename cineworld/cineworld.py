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
        """setup api key and API website addresses"""
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
        
    def get_list(self, datatype, url, **kwargs):
        """base function for connecting to API"""
        search_url = [url, '?']
        kwargs.update({'key': self.api_key})
        search_url.append(urlencode(kwargs))
        data = json.loads(urlopen(''.join(search_url)).read())
        return data[datatype]
    
    def get_cinemas(self, **kwargs):
        """gets a list of all cineworld cinemas and allows further customization of the list using arguments located in the API documentation"""
        return self.get_list('cinemas', self.cinemas_url, **kwargs)
    
    def get_films(self, **kwargs):
        """gets a list of all films currently playing in cineworld cinemas and allows further customization of the list using arguments located in the API documentation"""
        return self.get_list('films', self.films_url, **kwargs)
    
    def get_film_list(self):
        """cache the result of the list of films in case of multiple searching on the same object"""
        self.film_list = self.get_films()
        return self.film_list
    
    def get_dates(self, **kwargs):
        """gets a list of all dates when films are playing at cineworld cinemas and allows further customization of the list using arguments located in the API documentation"""
        return self.get_list('dates', self.dates_url, **kwargs)
      
    def get_performances(self, **kwargs):
        """not well documented but I assume it's for more specialized performances i.e. not films"""
        return self.get_list('performances', self.performances_url, **kwargs)
    
    def get_box_office_films(self):
        """uses a certain cinema (O2) and a certain day when non specialist films show (Wednesday) to get a list of the latest box office films"""
        today = datetime.date.today()
        next_wednesday = (today + datetime.timedelta((2 - today.weekday()) % 7)).strftime('%Y%m%d')
        films = self.get_films(cinema=79, date = next_wednesday)
        
        films = filter(lambda x: '3D' not in x['title'], films)
        for film in films:
            if '2D -' in film['title']:
                film['title']=film['title'][5:]
        return films

    def film_search(self, title):
        """film search using fuzzy matching"""
        films = []
        #check for cache or update
        if not hasattr(self, 'film_list'):
            self.get_film_list()
        #iterate over films and check for fuzzy string match    
        for film in self.film_list:
            strength = WRatio(title, film['title'])
            if  strength > 80:
                film.update({u'strength':strength})
                films.append(film)
        #sort films by the strength of the fuzzy string match
        films_sorted = sorted(films, key=itemgetter('strength'), reverse = True)
        return films_sorted
        
    def get_film_id(self, title, three_dimensional=False):
        """get the film id using the title in conjunction with the searching function"""
        films = self.film_search(title)
        for film in films:
            if (film['title'].find('3D') is - 1) is not three_dimensional:
                return film['edi']
        return -1
    
    def get_film_info(self, edi):
        """get the film id of a film using its edi number"""
        return self.get_films(film=edi, full='true')
    
    def get_cinemas_by_film(self, edi, **kwargs):
        """get cinemas where the film is playing using the film edi number"""
        return self.get_cinemas(film=edi, **kwargs)
    
    def get_cinema_info(self, id):
        """get cinema information using the cinema id number"""
        self.get_cinemas(cinema=id, full='true')
