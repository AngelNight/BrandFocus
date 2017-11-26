from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from brandfocus.parser_reviews import get_reviews
import json
from brandfocus.models import Firm, Social, Review, Rank, Tag
from psqlextra.models import PostgresModel
from psqlextra.fields import HStoreField
from django.db import models
from psqlextra.query import ConflictAction
from lib.neural_network.neural_network import calculating_rating


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

#Получение отзывов с сетей
def getreviews(request):
    tags_object = Tag.objects.filter(firm=Firm.objects.get(pk=int(request.GET.get('firm_id')))).all()
    tags = [tag.name for tag in tags_object]

    reviews=get_reviews(tags, 10)
    for review in reviews:
        Review.objects.on_conflict(['temp_id'], ConflictAction.UPDATE).insert(text=review['text'], photo_link=review['photo_link'], link=review['post_link'],
                              date=review['date'], temp_id=review['temp_id'], social=Social.objects.get(pk=(review['social_id']+1)),
                              firm=Firm.objects.get(pk=int(request.GET.get('firm_id'))),
                              rank=2)
    return HttpResponse(True)

#Получение Отзывов для вывода
def getreviewsdata(request):
    try:
        return HttpResponse(serializers.serialize('json',Review.objects.filter(firm=Firm.objects.get(pk=int(request.GET.get('firm_id')))).all().order_by('-date')))
    except Exception as e:
        return HttpResponse(False)


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
        return HttpResponse(Social.objects.create(name=request.GET.get('name')).id)
    except Exception as e:
        return HttpResponse(e)

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

def generateranks(request):
    calculating_rating()
    return HttpResponse(True)




