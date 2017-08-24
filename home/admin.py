# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Tutor)
admin.site.register(models.Student)
admin.site.register(models.Question)
