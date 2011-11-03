#!/usr/bin/env python

'''
Created on 17 Jul 2011

@author: oracal
'''
from cineworld import CW, cineworld
from mock import Mock
import unittest

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    # For older versions of Python.
    from urlparse import urlparse
    from cgi import parse_qs

def set_up():
    cineworld.urlopen = Mock()
    films = {u'films':[{u'edi': 39523, u'title': u'3D - Harry Potter And The Deathly Hallows Pt 2'}, {u'edi': 40501, u'title': u'3D - Transformers: Dark Of The Moon'}]}
    cineworld.json.loads = Mock(return_value=films)
    cineworld.API_KEY = 'my_api_key'

class CWClassInitTest(unittest.TestCase):


    def setUp(self):
        set_up()

    def test_uninitialized_api_key(self):
        self.assertEqual(CW().api_key, 'my_api_key')

    def test_initialized_api_key(self):
        self.assertEqual(CW('called_api_key').api_key, 'called_api_key')

class GetListTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_get_list_path(self):
        
        CW().get_list('films','some_url')
        call = cineworld.urlopen.call_args[0][0]
        parsed_call = urlparse(call)
        self.assertEqual(parsed_call.path,'some_url')
        
    def test_get_list_arguments(self):
        CW().get_list('films','some_url', argument1 = 'argument1', argument2 = 'argument2')
        call = cineworld.urlopen.call_args[0][0]
        parsed_call = urlparse(call)
        self.assertEqual(parse_qs(parsed_call.query)['argument1'],['argument1'])
        self.assertEqual(parse_qs(parsed_call.query)['argument2'],['argument2'])


class FilmListTest(unittest.TestCase):

    def setUp(self):
        set_up()

    def test_film_list_path(self):
        CW().get_film_list()
        call = cineworld.urlopen.call_args[0][0]
        parsed_call = urlparse(call)
        self.assertEqual(parsed_call.path,'/api/quickbook/films')

    def test_film_list_cache(self):
        cw = CW()
        cw.get_film_list()
        assert cw.film_list

        
    def test_film_list_return(self):
        self.assertEqual(CW().get_film_list(),[{u'edi': 39523, u'title': u'3D - Harry Potter And The Deathly Hallows Pt 2'}, {u'edi': 40501, u'title': u'3D - Transformers: Dark Of The Moon'}])
        
class FilmSearchTest(unittest.TestCase):

    def setUp(self):
        set_up()
        
    def test_search_accuracy_1(self):
        self.assertEquals(CW().film_search('harry potter and the deathly hallows'), [{u'edi': 39523, u'title': u'3D - Harry Potter And The Deathly Hallows Pt 2', u'strength':95}])
        
    def test_search_accuracy_2(self):
        self.assertEquals(CW().film_search('harry potter'), [{u'edi': 39523, u'title': u'3D - Harry Potter And The Deathly Hallows Pt 2', u'strength':90}])
        
    def test_search_accuracy_3(self):
        self.assertEquals(CW().film_search('horry putter'), [])
        
    def test_search_accuracy_4(self):
        self.assertEquals(CW().film_search('dark moon'), [{u'edi': 40501, u'title': u'3D - Transformers: Dark Of The Moon', u'strength':85}])
        
    def test_search_accuracy_5(self):
        self.assertEquals(CW().film_search('train spotting'), [])

if __name__ == "__main__":
    unittest.main()