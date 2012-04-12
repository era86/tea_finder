from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)

    def __unicode__(self):
        return self.name

class Caffeine(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name


class Tag(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.name


class Tea(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    caffeine = models.ForeignKey(Caffeine)
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name


class TeaTag(models.Model):
    tea = models.ForeignKey(Tea)
    tag = models.ForeignKey(Tag)
    
    def __unicode__(self):
        return ''.join([str(self.tea), '->', str(self.tag)])

class TeaReview(models.Model):
    tea = models.ForeignKey(Tea)
    rating = models.IntegerField()
    author = models.CharField(max_length=128)
    review = models.CharField(max_length=1024)
    date = models.DateField()

    def __unicode__(self):
        return ''.join([self.tea, '[',str(self.date),']'])
