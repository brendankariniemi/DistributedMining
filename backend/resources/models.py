from django.db import models


class Cryptocurrency(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()


class Guide(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()


class Tutorial(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
