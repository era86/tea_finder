# Create your views here.

from django.template import *
from django.http import HttpResponse
from django.shortcuts import *
from tea.models import *
from django.utils import simplejson as json
from django.db.models import Q
from util_query import get_queryset
from util_query import get_or_filter

def index(request):
    categories = Category.objects.all()
    caffeines = Caffeine.objects.all()
    tags = Tag.objects.order_by('name')
    context = {'categories': categories, 'caffeines': caffeines, 'tags':tags}
    return render_to_response('index.html', context, RequestContext(request))

def get_teas(request):
    query = request.GET.get('query') if request.GET.get('query') else ''
    categories = request.GET.get('categories')
    caffeines = request.GET.get('caffeines')
    tags = request.GET.get('tags')

    if categories:
        categories = json.loads(categories)
    if caffeines:
        caffeines = json.loads(caffeines)
    if tags:
        tags = json.loads(tags)

    teaObjs = get_queryset('Tea', query, 0, None)
    
    if caffeines:
        teaObjs = teaObjs.filter(get_or_filter('caffeine', caffeines))
    
    if categories:
        teaObjs = teaObjs.filter(get_or_filter('category', categories))

    teaList = [{'name':tea.name, \
             'partDesc':tea.description[0:50], \
             'id':tea.id \
            } for tea in teaObjs]

    teas = []
    print tags
    if tags:
        for tea in teaList:
            teaTags = [tt.tag.id for tt in \
                                        TeaTag.objects.filter(tea=tea['id'])]
            print teaTags
            found = True
            for tag in tags:
                if tag not in teaTags:
                    found = False
                    break
            if found:
                teas.append(tea)
    else:
        teas = teaList
        
    return HttpResponse(json.dumps({'teas':teas}),\
                        mimetype='application/json')

def get_tea(request):
    id = request.GET.get('id')
    
    teaObj = Tea.objects.get(id=id)

    teaTagObjs = TeaTag.objects.filter(tea=id)
    teaTags = [{'tag':tt.tag.name.strip()} for tt in teaTagObjs]

    tea = {'id':teaObj.id, \
           'name':teaObj.name, \
           'desc':teaObj.description, \
           'caffeine':teaObj.caffeine.name, \
           'category':teaObj.category.name, \
           'tags':teaTags
          }

    return HttpResponse(json.dumps(tea), mimetype='application/json')
