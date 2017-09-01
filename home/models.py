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
            ('maths : numbers and place value', 'maths : numbers and place value'),
            ('maths : number sequences and properties', 'maths : number sequences and properties'),
            ('maths : addition and subtraction', 'maths : addition and subtraction'),
            ('maths : short and long multiplication', 'maths : short and long multiplication'),
            ('maths : times tables', 'maths : times tables'),
            ('maths : mode, median and mean', 'maths : mode, median and mean'),
            ('maths : fractions', 'maths : fractions'),
            ('maths : decimals', 'maths : decimals'),
            ('maths : coordinates', 'maths : coordinates'),
            ('maths : negative numbers', 'maths : negative numbers'),
            ('maths : multiplication involving decimals', 'maths : multiplication involving decimals'),
            ('maths : division', 'maths : division'),
            ('maths : calculations', 'maths : calculations'),
            ('maths : percentages', 'maths : percentages'),
            ('maths : rounding numbers', 'maths : rounding numbers'),
            ('maths : measurements', 'maths : measurements'),
            ('maths : solving problems', 'maths : solving problems'),
            ('maths : line graphs', 'maths : line graphs'),
            ('maths : algebra', 'maths : algebra'),
            ('maths : square, cube and triangular numbers', 'maths : square, cube and triangular numbers'),
            ('maths : factors, multiples and prime numbers', 'maths : factors, multiples and prime numbers'),
            ('maths : estimation', 'maths : estimation'),
            ('maths : ratio and proportion', 'maths : ratio and proportion'),
            ('maths : perimeter and area', 'maths : perimeter and area'),
            ('maths : angles', 'maths : angles'),
            ('maths : shapes', 'maths : shapes'),
            ('maths : volume', 'maths : volume'),
            ('maths : probability', 'maths : probability'),
            ('maths : statistics', 'maths : statistics'),
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


class QuestionDone(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField(default=-1)

    def __str__(self):
        return '{} {}'.format(self.student.first_name, self.date)
