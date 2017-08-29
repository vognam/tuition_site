# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-29 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20170824_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(choices=[('maths : numbers and place value', 'maths : numbers and place value'), ('maths : number sequences and properties', 'maths : number sequences and properties'), ('maths : addition and subtraction', 'maths : addition and subtraction'), ('maths : short and long multiplication', 'maths : short and long multiplication'), ('maths : times tables', 'maths : times tables'), ('maths : mode, median and mean', 'maths : mode, median and mean'), ('maths : fractions', 'maths : fractions'), ('maths : decimals', 'maths : decimals'), ('maths : coordinates', 'maths : coordinates'), ('maths : negative numbers', 'maths : negative numbers'), ('maths : multiplication involving decimals', 'maths : multiplication involving decimals'), ('maths : division', 'maths : division'), ('maths : calculations', 'maths : calculations'), ('maths : percentages', 'maths : percentages'), ('maths : rounding numbers', 'maths : rounding numbers'), ('maths : measurements', 'maths : measurements'), ('maths : solving problems', 'maths : solving problems'), ('maths : line graphs', 'maths : line graphs'), ('maths : algebra', 'maths : algebra'), ('maths : square, cube and triangular numbers', 'maths : square, cube and triangular numbers'), ('maths : factors, multiples and prime numbers', 'maths : factors, multiples and prime numbers'), ('maths : estimation', 'maths : estimation'), ('maths : ratio and proportion', 'maths : ratio and proportion'), ('maths : perimeter and area', 'maths : perimeter and area'), ('maths : angles', 'maths : angles'), ('maths : shapes', 'maths : shapes'), ('maths : volume', 'maths : volume'), ('maths : probability', 'maths : probability'), ('maths : statistics', 'maths : statistics')], max_length=20),
        ),
    ]