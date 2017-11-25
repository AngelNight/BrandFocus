from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import json
from brandfocus.models import Firm, Social, Review, Rank, Tag


#Получение тегов
def gettags(request):
    try:
        return HttpResponse(serializers.serialize('json', Tag.objects.filter(firm=Firm.objects.get(pk=int(request.GET.get('firm_id')))).all()))
    except Exception as e:
        return HttpResponse(False)

# Получение фирм
def getfirms(request):
    try:
        return HttpResponse(serializers.serialize('json', Firm.objects.all()))
    except Exception as e:
        return HttpResponse(False)

# Получение ранжировани
def getranks(request):
    try:
        return HttpResponse(serializers.serialize('json', Rank.objects.all()))
    except Exception as e:
        return HttpResponse(False)

# Получение социальных
def getsocials(request):
    try:
        return HttpResponse(serializers.serialize('json', Social.objects.all()))
    except Exception as e:
        return HttpResponse(False)

#Получение отзывов
def getreviews(request):
    Review.objects.filter()

#Вставка фирмы
def insertfirm(request):
    flag = True
    try:
        return HttpResponse(Firm.objects.create(name=request.GET.get('name')).id)
    except Exception as e:
        return HttpResponse(False)

# Вставка ранжирования
def insertrank(request):
    flag = True
    try:
        return HttpResponse(Rank.objects.create(name=request.GET.get('name')).id)
    except Exception as e:
        return HttpResponse(False)

# Вставка соц.сети
def insertsocial(request):
    flag = True
    try:
        return HttpResponse(Rank.objects.create(name=request.GET.get('name')).id)
    except Exception as e:
        return HttpResponse(False)

#Вставка тег с гет параметрами name и firm_id
def inserttag(request):
    flag = True
    try:
        return HttpResponse(Tag.objects.create(name=request.GET.get('name'), firm=Firm.objects.get(pk=int(request.GET.get('firm_id')))).id)
    except Exception as e:
        return HttpResponse(False)


#Удаление тэга
def deletetag(request):
    flag=True
    try:
        Tag.objects.get(pk=int(request.GET.get('tag_id'))).delete()
        return HttpResponse(flag)
    except Exception as e:
        flag=False
    return HttpResponse(flag)


