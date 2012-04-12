#!/usr/bin/python

'''
Commonly used utilities for creating initial Django fixtures. This includes
fetching rows from the Google Docs spreadsheet and creating objects in the
format of JSON fixtures.
'''

__author__ = 'Frederick Ancheta'
__version__ = '0.1.0'

import os
import urllib2
import csv
import json

SS_URL = 'https://docs.google.com/spreadsheet/pub?key=0AiCH88rX-f1hdDRYMmRFUFc\
tTUxZNlRLSGlGX2hNbEE&output=csv'

def get_teas():
    '''
    Get the spreadsheet data from the URL as CSV data.
    '''
    ssFile = urllib2.urlopen(SS_URL)
    ssCsv = csv.reader(ssFile)
    
    next(ssCsv)     # skip the header row
    teas = []
    for row in ssCsv:
        teas.append({'name':row[1], 'category':row[2], 'caffeine':row[3],\
                     'tags':row[4].split(' ')})
    return teas

def create_json(model, objs):
    '''
    Given a list of objects representing Model entries and the name of the 
    Model, return a JSON list of Django fixtures.
    '''
    fixObjs = []
    for obj in objs:
        fields = dict(obj)
        del fields['pk']
        fixObjs.append({'model':'tea.'+model.lower(), 'pk':obj['pk'],\
                        'fields':fields})
    return json.dumps(fixObjs, indent=4)

# Module tests.
if __name__ == '__main__':
    print 'Hello'
