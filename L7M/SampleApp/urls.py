from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^sample/', csrf_exempt(test.as_view()), name='a'),
    url(r'^testapi/', csrf_exempt(tree_api.as_view()), name='b'),
    url(r'^createadmin/', csrf_exempt(CreateAdmin.as_view()), name='c'),
    url(r'^d/', csrf_exempt(test2.as_view()), name = 'd'),
    url(r'^e/', csrf_exempt(test3.as_view()), name = 'e'),
    url(r'^f/', csrf_exempt(test4.as_view()), name = 'f'),
    url(r'^g/', csrf_exempt(test5.as_view()), name = 'g'),
]
