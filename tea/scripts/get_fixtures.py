#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2
import json
import os

storeUrl = 'http://store.remedyteas.com/'

storeBs = BeautifulSoup(''.join(urllib2.urlopen(storeUrl).read()))

catUl = storeBs.find('ul', {'id':'menuList'})

# holds unique fixtures
categories = {}
caffeines = {}
tags = {}
teas = []
teaTags = []

for catLi in catUl.findAll('li'):
    try:
        # category information
        catName = catLi.find('a').contents[0].strip()
        catDesc = catLi.find('span', {'class': 'content'}).contents[0].strip()
        catUrl = catLi.find('a')['href'].strip()
        
        # add a category fixture
        categories[catName] = {
                                'model':'tea.category', \
                                'pk':catName.upper(), \
                                'fields': { \
                                    'name':catName, \
                                    'description':catDesc \
                               }}

        catBs = BeautifulSoup(''.join(urllib2.urlopen(catUrl).read()))
        teaUl = catBs.find('div', {'id': 'mycarousel'}).find('ul')
    except Exception as e:
        print ''.join(['Error getting Category: ',str(e)])
        continue

    try:
        for t in teaUl.findAll('li'):
            try:
                # each tea for this category
                teaName = t.find('span', {'class':'title'}).contents[0].strip()
                teaNum = t.find('span', {'class':'itemNum'}).contents[0].strip()
                teaUrl = t.find('a')['href'].strip()

                teaBs = BeautifulSoup(''.join(urllib2.urlopen(teaUrl).read()))
                teaDesc = teaBs.find('div', {'id':'itemDescription'}).\
                            find('p').contents[0].strip()
                teaCaff = teaBs.find('div', {'id':'itemCaffeineLevels'}).\
                            find('div', {'class':'itemVal'}).contents[0].strip()
                
                # add the tags to Tag and TeaTag fixtures
                for tt in teaBs.find('div', {'id':'itemTags'}).findAll('a'):
                    tagName = tt.contents[0].strip()
                    if tagName not in tags:
                        tags[tagName] = {'model':'tea.tag', \
                                         'pk':tagName.upper(), \
                                         'fields':{'name':tagName}}

                    teaTags.append({'model':'tea.teatag',
                                    'pk':len(teaTags),
                                    'fields':{ \
                                        'tea':teaNum, \
                                        'tag':tagName.upper() \
                                    }})

                # add the caffeine if no added already
                if teaCaff not in caffeines:
                    caffeines[teaCaff] = {'model':'tea.caffeine', \
                                          'pk':teaCaff.upper(), \
                                          'fields': {'name':teaCaff}}
                
                # finally, add the tea
                teas.append({'model':'tea.tea',
                             'pk': int(teaNum),
                             'fields':{
                                'category':catName.upper(),
                                'caffeine':teaCaff.upper(),
                                'description':teaDesc,
                                'name':teaName}})
            except Exception as e:
                print ''.join(['Error getting Tea: ',str(e)])
                continue
    except Exception as e:
        continue

catFile = open('Category.json', 'w')
catFile.write(json.dumps(categories.values(), indent=4))
catFile.close()

cafFile = open('Caffeine.json', 'w')
cafFile.write(json.dumps(caffeines.values(), indent=4))
cafFile.close()

tagFile = open('Tag.json', 'w')
tagFile.write(json.dumps(tags.values(), indent=4))
tagFile.close()

teaFile = open('Tea.json', 'w')
teaFile.write(json.dumps(teas, indent=4))
teaFile.close()

teaTagFile = open('TeaTag.json', 'w')
teaTagFile.write(json.dumps(teaTags, indent=4))
teaTagFile.close()


