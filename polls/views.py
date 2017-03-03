# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import requests

def index(request):
    r = requests.get('https://www.reddit.com/user/BeneficEvil/comments/.json')
    d = r.json()
    # return HttpResponse(d.keys())     # works
    # return HttpResponse(d['kind'])    # works
    # return HttpResponse(d['data']['modhash'])     #fails
    # return HttpResponse(r, content_type="application/json") # works
    # return HttpResponse(d['data']['children'][0]['kind'])     # works
    # return HttpResponse(d['data']['children'][0]['data']['link_id']) #works
    return HttpResponse(d['data']['children'][0]['data']['body']) #works
  
    
# Three queries to get user comments using after value from previous    
# https://www.reddit.com/user/stp2007/comments/.json    
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d8fi1ll
# https://www.reddit.com/user/stp2007/comments/.json?after=t1_d6b14um
     
    





# >>> r.encoding
# 'utf-8'
# >>> r.text
# u'{"type":"User"...'
# >>> r.json()
# {u'private_gists': 419, u'total_private_repos': 77, ...}
