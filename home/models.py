# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    tutor = models.ForeignKey('Tutor', on_delete=models.SET_NULL, null=True)
    classID = models.IntegerField(default=-1)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Tutor(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Question(models.Model):

    CATEGORIES = (
        ('Algebra', 'Algebra'),
        ('Shapes', 'Shapes'),
    )

    DIFFICULTIES = (
        ('Hard', 'Hard'),
        ('Medium', 'Medium'),
        ('Easy', 'Easy'),
    )

    category = models.CharField(choices=CATEGORIES, max_length=20)
    difficulty = models.CharField(choices=DIFFICULTIES, max_length=15)
    out_of = models.IntegerField()
    answer = models.CharField(max_length=25, blank=True)
    image = models.ImageField(upload_to='questions', height_field="height_field",
                              width_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return 'Question %s' % self.id
