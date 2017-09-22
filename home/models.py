# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    classID = models.ForeignKey('Class', null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    has_attended = models.BooleanField()
    date = models.DateField()

    def __str__(self):
        return '%s : %s' % (self.student.first_name, self.date)


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
        (6, 'Hard'),
        (5, 'Medium'),
        (4, 'Easy'),
    )

    category = models.CharField(choices=CATEGORIES, max_length=100, null=False)
    difficulty = models.IntegerField(choices=DIFFICULTIES, null=False)
    out_of = models.IntegerField(null=False)
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
        return '%s %s' % (self.student.first_name, str(self.date))


class Class(models.Model):

    TIMES = (
        (0, 'None'),
        (1, 'Saturday 9:00 - 11:00'),
        (2, 'Saturday 11:30 - 13:30'),
        (3, 'Saturday 14:00 - 16:00'),
        (4, 'Saturday 16:30 - 18:30'),
        (5, 'Saturday 19:00 - 21:00'),
        (6, 'Sunday 9:00 - 11:00'),
        (7, 'Sunday 11:30 - 13:30'),
        (8, 'Sunday 14:00 - 16:00'),
        (9, 'Sunday 16:30 - 18:30'),
        (10, 'Sunday 19:00 - 21:00'),
    )

    # NOTE: if adding extra years, make sure
    # a) corresponding difficulty of questions are present
    # b) when choosing mixed questions this is taken account for
    YEAR = (
        (4, 4),
        (5, 5),
    )

    year = models.IntegerField(choices=YEAR, default=5)
    time = models.IntegerField(choices=TIMES)
    tutor = models.ForeignKey(User)

    def __str__(self):
        return '%s - %s' % (str(self.get_time_display()), str(self.tutor))

