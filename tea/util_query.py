'''
Query Utilities

Utilities for interacting with the Django database. 
'''
from tea.models import *
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

__author__ = 'Frederick Ancheta'
__version__ = '0.1'

def get_queryset(name, query, start, count):
    '''
    Returns a QuerySet of the specified Model (name). A search query can be used to further
    filter the results. Paging is also supported.
    '''
    start = int(start) if start else 0
    count = int(count) if count else None

    model = None
    for m in models.get_models():
        if m.__name__ == name:
            model = m
            break

    if not(model):
		raise Exception('No Model defined with name: '+name)

    qs = model.objects.all()

    fields = [f.name for f in model._meta.fields if not(f.rel)]

	# create the QuerySet filter based on search query
    if query:
        qfilter = None
        for qor in query.split(','):	# commas are ORed
            qandfilt = None
            for qand in qor.strip().split(' '):		# spaces are ANDed
                ffilt = None
                for f in fields:		# all fields in the Model are searched
                    if not(ffilt):
                        ffilt = Q(**{f+'__icontains': qand})
                    else:
                        ffilt |= Q(**{f+'__icontains': qand})
                if not(qandfilt):
                    qandfilt = ffilt
                else:
                    qandfilt &= ffilt
            if not(qfilter):
                qfilter = qandfilt
            else:
                qfilter |= qandfilt
        qs = qs.filter(qfilter)
    
    if start and count:
        return qs[start:start+count]

    return qs

def get_or_filter(field, values):
    '''
    Creates an OR Q() filter for use in a QuerySet.filter() call. Specify the
    name of the field and the values to create ORs over.
    '''
    qfilter = None
    for v in values:
        if qfilter:
            qfilter |= Q(**{field: v})
        else:
            qfilter = Q(**{field: v})
    return qfilter
