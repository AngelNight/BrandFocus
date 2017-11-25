from django.db import models

class Social(models.Model):

    # поля данных
    name = models.CharField(max_length=255, unique=True) # Название сети

    # строковое представление
    def __str__(self):
        return self.name

    # информация для базы данных
    class Meta:
        db_table = 'social'   # имя таблицы

class Rank(models.Model):

    # поля данных
    name = models.CharField(max_length=255, unique=True) # Статус

    # строковое представление
    def __str__(self):
        return self.name

    # информация для базы данных
    class Meta:
        db_table = 'rank'   # имя таблицы


class Firm(models.Model):

    # поля данных
    name = models.CharField(max_length=255, unique=True) # Название фирмы

    # строковое представление
    def __str__(self):
        return self.name

    # информация для базы данных
    class Meta:
        db_table = 'firm'   # имя таблицы

class Tag(models.Model):

    # поля данных
    name = models.CharField(max_length=255, unique=True) # Название Тэга
    firm = models.ForeignKey(Firm)  # Ключ на фирму

    # строковое представление
    def __str__(self):
        return self.name

    # информация для базы данных
    class Meta:
        db_table = 'tag'   # имя таблицы

class Review(models.Model):

    # поля данных
    link = models.CharField(max_length=255) # Ссылка на отзыв
    text = models.TextField() # Текст отзыва
    date = models.DateField() # Дата поста
    photo_link = models.TextField() # Ссылка на аватар
    temp_id=models.CharField(max_length=255) # Временний ИД для загрузки поста
    rank = models.IntegerField(default=None)  # Ранжирование по кэтбуст
    social = models.ForeignKey(Social) # Ключ на соц. сеть
    firm = models.ForeignKey(Firm) # Ключ на фирму


    # строковое представление
    def __str__(self):
        return self.link

    # информация для базы данных
    class Meta:
        db_table = 'review'   # имя таблицы

