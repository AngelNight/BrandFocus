"""brandfocus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
from django.conf.urls import patterns, url
from myapp.views import home, contact

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^login/$', login, name='login'),
]
"""

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from brandfocus.views import home
from brandfocus.base import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'getTags/$', gettags, name='gettags'),
    url(r'getReviews/$', getreviews, name='getreviews'),
    url(r'insertFirm/$', insertfirm, name='insertfirm'),
    url(r'insertTag/$', inserttag, name='inserttag'),
    url(r'insertRank/$', insertrank, name='insertrank'),
    url(r'insertSocial/$', insertsocial, name='insertsocial'),
    url(r'deleteTag/$', deletetag, name='deletetag'),
    url(r'getFirms/$', getfirms, name='getfirms'),
    url(r'getRanks/$', getranks, name='getranks'),
    url(r'getSocials/$', getsocials, name='getsocials'),
    url(r'getReviewsData/$', getreviewsdata, name='getreviewsdata'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
