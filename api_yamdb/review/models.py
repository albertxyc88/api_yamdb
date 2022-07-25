from unicodedata import name
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название'
    )
    year = 
    rating = 
    description = 
    genre = 
    category = 

class Categorie(models.Model):
    name = 
    slug = 

class Genre(models.Model):
    name = 
    slug = 