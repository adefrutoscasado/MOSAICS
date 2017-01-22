# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.safestring import mark_safe

class Deletion(models.Model):
    identifier = models.CharField(default="null", max_length=15)
    owner = models.CharField(null=True, max_length=30)
    number_of_pieces = models.CharField(null=True, max_length=5)
    created_date = models.DateTimeField(null=True, blank=True)
    deletion_date = models.DateTimeField(null=True, blank=True)
    pieces_given = models.CharField(null=True, max_length=10)
    pieces_accepted = models.CharField(null=True, max_length=10)
    pieces_submited = models.CharField(null=True, max_length=10)
    pieces_unused = models.CharField(null=True, max_length=10)
    time_of_life = models.CharField(null=True, max_length=10)



class Piece(models.Model):
    image = models.ImageField(upload_to='pieces/%Y/%m/%d', width_field='width', height_field='height')
    state = models.CharField(default="null", max_length=30)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    documentidentifier = models.CharField(default="null", max_length=8)
    identifier = models.CharField(default="null", max_length=15)
    xposition = models.IntegerField(null=True)
    yposition = models.IntegerField(null=True)
    xpixelposition = models.IntegerField(null=True)
    ypixelposition = models.IntegerField(null=True)
    owner = models.CharField(null=True, max_length=30)
    given_date = models.DateTimeField(null=True, blank=True)
    ip = models.CharField(null=True, max_length=30)


    def admin_thumbnail_piece(self):
        if self.image:
            return mark_safe("<img style='height: auto; width: auto;max-width: 100px;max-height: 100px;' src='%s' />" % (self.image.url))
        else:
            return mark_safe("No image")
    admin_thumbnail_piece.short_description = 'Piece'

class Document(models.Model):
    #me gustaria poder subirlo a una carpeta de nombre el ID del objeto, en vez de a la fecha, para que esten todas las piezas reunidas
    docfile = models.ImageField(upload_to='documents/%Y/%m/%d', width_field='image_width', height_field='image_height')
    mosaic = models.ImageField(upload_to='documents/%Y/%m/%d', default="null")
    image_width = models.IntegerField(null=True)
    image_height = models.IntegerField(null=True)
    divx = models.IntegerField(null=True)
    divy = models.IntegerField(null=True)
    identifier = models.CharField(default="null", max_length=8)
    owner = models.CharField(default="null", max_length=30)
    created_date = models.DateTimeField(default=timezone.now)
    
    def admin_thumbnail(self):
        return mark_safe("<img style='height: auto; width: auto;max-width: 100px;max-height: 100px;' src='%s' />" % (self.docfile.url))
    admin_thumbnail.short_description = 'Image'
    
    def admin_thumbnail_mosaic(self):
        return mark_safe("<a href='%s'><img style='height: auto; width: auto;max-width: 100px;max-height: 100px;' src='%s' /></a>" % (self.mosaic.url, self.mosaic.url))
    admin_thumbnail_mosaic.short_description = 'Mosaic'
    
class Banned(models.Model):
    ip = models.CharField(default="null", max_length=30)
    documentidentifier = models.CharField(default="null", max_length=8)
    identifier = models.CharField(default="null", max_length=15)