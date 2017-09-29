# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, default='')
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
        ('Place value, Order and compare numbers', 'Place value, Order and compare numbers'),
        ('Negative numbers', 'Negative numbers'),
        ('Number sequences', 'Number sequences'),
        ('Estimation and Rounding', 'Estimation and Rounding'),
        ('Solve problems on Number and Place Value, Roman Numerals',
         'Solve problems on Number and Place Value, Roman Numerals'),
        ('Mental addition/subtraction, via column method (including decimals)',
         'Mental addition/subtraction, via column method (including decimals)'),
        ('Estimation to check answers, and solve problems on addition and subtraction',
         'Estimation to check answers, and solve problems on addition and subtraction'),
        ('Timetables, Multiples, Mental/Basic multiplication', 'Timetables, Multiples, Mental/Basic multiplication'),
        ('Long multiplication (including decimals) ', 'Long multiplication (including decimals) '),
        ('Mental/Basic division, short division (including decimals) and testing divisibility',
         'Mental/Basic division, short division (including decimals) and testing divisibility'),
        ('Long division (including decimals)', 'Long division (including decimals)'),
        ('Prime numbers', 'Prime numbers'),
        ('HCF and LCM, Questions and Problems on factors and multiples',
         'HCF and LCM, Questions and Problems on factors and multiples'),
        ('Square and cube numbers, and problems on this', 'Square and cube numbers, and problems on this'),
        ('Mental mixed calculations, BIDMAS, Problems on BIDMAS and mixed calculations',
         'Mental mixed calculations, BIDMAS, Problems on BIDMAS and mixed calculations'),
        ('Basic fraction questions, Addition and Subtraction of fractions',
         'Basic fraction questions, Addition and Subtraction of fractions'),
        ('Multiplication and division of fractions, Mixed and improper fractions',
         'Multiplication and division of fractions, Mixed and improper fractions'),
        ('Mixture of fraction questions, simplifying fractions',
         'Mixture of fraction questions, simplifying fractions'),
        ('Equivalent fractions, Comparing and ordering fractions',
         'Equivalent fractions, Comparing and ordering fractions'),
        ('Unit and non-unit fractions, Complex fraction questions, andSolve fraction problems',
         'Unit and non-unit fractions, Complex fraction questions, andSolve fraction problems'),
        ('Equivalent decimals to fractions, Decimal place value, Order decimal fractions',
         'Equivalent decimals to fractions, Decimal place value, Order decimal fractions'),
        ('Percentage/decimal/fraction equivalents, and questions',
         'Percentage/decimal/fraction equivalents, and questions'),
        ('Solve problems on fractions/decimals/percentages', 'Solve problems on fractions/decimals/percentages'),
        ('Ratio and proportion', 'Ratio and proportion'),
        ('Solve problems on ratio and proportion', 'Solve problems on ratio and proportion'),
        ('Algebra', 'Algebra'),
        ('Solve problems on algebra', 'Solve problems on algebra'),
        ('Measure and compare, Add and subtract measurements, Convert between units',
         'Measure and compare, Add and subtract measurements, Convert between units'),
        ('Convert between metric and imperial, Solve problems on measurement, Solve problems on money',
         'Convert between metric and imperial, Solve problems on measurement, Solve problems on money'),
        ('Time including Analogue and digital clocks (12hr/24hr), Estimating '
         'times, Calenders, months, dates and problems',
         'Time including Analogue and digital clocks (12hr/24hr), Estimating '
         'times, Calenders, months, dates and problems'),
        ('Perimeter, Area', 'Perimeter, Area'),
        ('Area of parallelograms and triangles, Solve problems on area and perimeter',
         'Area of parallelograms and triangles, Solve problems on area and perimeter'),
        ('Volume and Solve volume problems', 'Volume and Solve volume problems'),
        ('2D shapes, Compare and classify 2D shapes, Draw 2-D shapes, and Questions on shapes',
         '2D shapes, Compare and classify 2D shapes, Draw 2-D shapes, and Questions on shapes'),
        ('Name parts of circle, radius, diameter, circumference, and Solve problems on 2D shapes',
         'Name parts of circle, radius, diameter, circumference, and Solve problems on 2D shapes'),
        ('3D shapes, Features of a 3D shape, and Solve problems on 3D shapes',
         '3D shapes, Features of a 3D shape, and Solve problems on 3D shapes'),
        ('Angles', 'Angles'),
        ('Solve problems on angles', 'Solve problems on angles'),
        ('Symmetry in 2D shapes', 'Symmetry in 2D shapes'),
        ('Coordinates, Drawing shapes on a coordinates graph, and Solve problems on coordinates',
         'Coordinates, Drawing shapes on a coordinates graph, and Solve problems on coordinates'),
        ('Bar Charts, Bar graphs, tally chart, pictograms and tables, time graphs, and interpretingVenn, '
         'Carroll diagrams, Pie charts, line graphs and solving related problems',
         'Bar Charts, Bar graphs, tally chart, pictograms and tables, time graphs, and interpretingVenn, '
         'Carroll diagrams, Pie charts, line graphs and solving related problems'),
        ('Mean, Median and Mode, and solving related problems', 'Mean, Median and Mode, and solving related problems'),
    )

    OLD_CATEGORIES = \
        (
            ('Place value', 'Place value'),
            ('Order and compare numbers', 'Order and compare numbers'),
            ('Negative numbers', 'Negative numbers'),
            ('Number sequences', 'Number sequences'),
            ('Estimation and Rounding', 'Estimation and Rounding'),
            ('Roman Numerals', 'Roman Numerals'),
            ('Solve problems on Number and Place Value', 'Solve problems on Number and Place Value'),
            ('Mental addition/subtraction', 'Mental addition/subtraction'),
            ('Addition/subtraction with decimals?', 'Addition/subtraction with decimals?'),
            ('Addition/Subtraction via column method', 'Addition/Subtraction via column method'),
            ('Estimation to check answers', 'Estimation to check answers'),
            ('Solve problems on addition and subtraction', 'Solve problems on addition and subtraction'),
            ('Timetables', 'Timetables'),
            ('Multiples', 'Multiples'),
            ('Mental/Basic multiplication', 'Mental/Basic multiplication'),
            ('Long multiplication', 'Long multiplication'),
            ('Long multiplication including decimals?', 'Long multiplication including decimals?'),
            ('Mental/Basic division', 'Mental/Basic division'),
            ('Short division', 'Short division'),
            ('Short division with decimals?', 'Short division with decimals?'),
            ('Testing divisibility', 'Testing divisibility'),
            ('Long division', 'Long division'),
            ('Long division with decimals', 'Long division with decimals'),
            ('Prime numbers', 'Prime numbers'),
            ('HCF and LCM', 'HCF and LCM'),
            ('Questions and Problems on factors and multiples', 'Questions and Problems on factors and multiples'),
            ('Square and cube numbers', 'Square and cube numbers'),
            ('Questions and Problems on square and cube numbers', 'Questions and Problems on square and cube numbers'),
            ('Mental mixed calculations', 'Mental mixed calculations'),
            ('BIDMAS', 'BIDMAS'),
            ('Questions and Problems on BIDMAS and mixed calculations', 'Questions and Problems on BIDMAS and mixed calculations'),
            ('Solve complex problems on all of the above (including real life)', 'Solve complex problems on all of the above (including real life)'),
            ('Basic fraction questions', 'Basic fraction questions'),
            ('Addition and Subtraction of fractions', 'Addition and Subtraction of fractions'),
            ('Multiplication and division of fractions', 'Multiplication and division of fractions'),
            ('Mixed and improper fractions', 'Mixed and improper fractions'),
            ('Mixture of fraction questions', 'Mixture of fraction questions'),
            ('Simplifying fractions', 'Simplifying fractions'),
            ('Equivalent fractions', 'Equivalent fractions'),
            ('Comparing and ordering fractions', 'Comparing and ordering fractions'),
            ('Unit and non-unit fractions', 'Unit and non-unit fractions'),
            ('Complex fraction questions', 'Complex fraction questions'),
            ('Solve fraction problems', 'Solve fraction problems'),
            ('Equivalent decimals to fractions', 'Equivalent decimals to fractions'),
            ('Decimal place value', 'Decimal place value'),
            ('Order decimal fractions', 'Order decimal fractions'),
            ('Percentage/decimal/fraction equivalents', 'Percentage/decimal/fraction equivalents'),
            ('Questions on percentages/decimals/fractions', 'Questions on percentages/decimals/fractions'),
            ('Solve problems on fractions/decimals/percentages', 'Solve problems on fractions/decimals/percentages'),
            ('Ratio and proportion', 'Ratio and proportion'),
            ('Solve problems on ratio and proportion', 'Solve problems on ratio and proportion'),
            ('Algebra', 'Algebra'),
            ('Solve problems on algebra', 'Solve problems on algebra'),
            ('Measure and compare', 'Measure and compare'),
            ('Add and subtract measurements', 'Add and subtract measurements'),
            ('Convert between units', 'Convert between units'),
            ('Convert between metric and imperial', 'Convert between metric and imperial'),
            ('Solve problems on measurement', 'Solve problems on measurement'),
            ('Solve problems on money', 'Solve problems on money'),
            ('What do I do for stuff that is exclusively year 4???', 'What do I do for stuff that is exclusively year 4???'),
            ('Analogue and digital clocks', 'Analogue and digital clocks'),
            ('12hour/24 hour', '12hour/24 hour'),
            ('Estimating times', 'Estimating times'),
            ('Time for calendars, timetables, roman numerals', 'Time for calendars, timetables, roman numerals'),
            ('Solve problems time)?', 'Solve problems time)?'),
            ('Perimeter', 'Perimeter'),
            ('Area', 'Area'),
            ('Area of parallelograms and triangles', 'Area of parallelograms and triangles'),
            ('Solve problems on area and perimeter', 'Solve problems on area and perimeter'),
            ('Volume', 'Volume'),
            ('Solve volume problems', 'Solve volume problems'),
            ('2D shapes', '2D shapes'),
            ('Compare and classify 2D shapes', 'Compare and classify 2D shapes'),
            ('Draw 2-D shapes', 'Draw 2-D shapes'),
            ('Questions on shapes', 'Questions on shapes'),
            ('Name parts of circle, radius, diameter, circumference', 'Name parts of circle, radius, diameter, circumference'),
            ('Solve problems on 2D shapes', 'Solve problems on 2D shapes'),
            ('3D shapes', '3D shapes'),
            ('Features of a 3D shape', 'Features of a 3D shape'),
            ('Solve problems on 3D shapes', 'Solve problems on 3D shapes'),
            ('Angles', 'Angles'),
            ('More Angles', 'More Angles'),
            ('Solve problems on angles', 'Solve problems on angles'),
            ('Symmetry in 2D shapes', 'Symmetry in 2D shapes'),
            ('Coordinates', 'Coordinates'),
            ('Drawing shapes on a coordinates graph', 'Drawing shapes on a coordinates graph'),
            ('Solve problems on coordinates', 'Solve problems on coordinates'),
            ('Bar Charts, Bar graphs, tally chart, pictograms and tables, time graphs', 'Bar Charts, Bar graphs, tally chart, pictograms and tables, time graphs'),
            ('Questions and interpreting all of the above', 'Questions and interpreting all of the above'),
            ('Solve problems on the above', 'Solve problems on the above'),
            ('Venn and Carroll diagrams', 'Venn and Carroll diagrams'),
            ('Pie charts and line graphs', 'Pie charts and line graphs'),
            ('Solve problems on the above', 'Solve problems on the above'),
            ('Mean, Median and Mode', 'Mean, Median and Mode'),
            ('Solve problems on mean, median and mode', 'Solve problems on mean, median and mode'),
            ('Solve problems on all of the above', 'Solve problems on all of the above'),
        )

    OLD_OLD_CATEGORIES = (
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
        (7, 'Very Difficult'),
        (6, 'Year 6'),
        (5, 'Year 5'),
        (4, 'Year 4'),
        (3, 'Year 3'),
    )

    category = models.CharField(choices=CATEGORIES, max_length=250, null=False)
    difficulty = models.CharField(choices=DIFFICULTIES, null=False, max_length=20)
    out_of = models.IntegerField(null=False)
    answer = models.CharField(max_length=500, blank=True)
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

