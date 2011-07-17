#!/usr/bib/env python

'''
Created on 17 Jul 2011

@author: oracal
'''
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='cineworld',
    version='0.1.0',
    author='Thomas Whitton',
    author_email='mail@thomaswhitton.com',
    packages=['cineworld'],
    url='https://github.com/oracal/cineworld',
    license='LICENSE.txt',
    description='Cineworld API Wrapper',
    long_description=open('README.txt').read(),
)