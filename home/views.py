# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .forms import ContactForm, ClassChoiceForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StudentForm, StudentChoiceForm, CategoryChoiceForm
from django.core.urlresolvers import reverse
from .viewfunctions import *
from django.forms import inlineformset_factory

from.models import Question, QuestionDone, Student, Attendance
import zipfile as zf
import shutil
import sqlite3
import os
from django.core.files import File
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    return render(request, 'home/index.html', {'nbar': 'home'})


def aboutus(request):
    return render(request, 'home/aboutus.html', {'nbar': 'aboutus'})


def meettheteam(request):
    return render(request, 'home/meettheteam.html', {'nbar': 'meettheteam'})


def pricing(request):
    return render(request, 'home/pricing.html', {'nbar': 'pricing'})


def bookings(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['contact_name']
            phone = form.cleaned_data['contact_phone']
            email = form.cleaned_data['contact_email']
            message = form.cleaned_data['contact_message']
            try:
                send_mail(subject='Booking query',
                          message='Name: ' + name + '\nEmail: ' + email + '\nPhone: ' + phone + '\n' + message,
                          recipient_list=['info@just11plus.com'],
                          from_email='vignesh.uma1@gmail.com')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "home/bookings.html", {
        'form': form,
        'nbar': 'bookings'})


def success(request):
    return render(request, 'home/success.html')


def philosophy(request):
    return render(request, 'home/philosophy.html', {'nbar': 'philosophy'})


def whatis11plus(request):
    return render(request, 'home/whatis11plus.html', {'nbar': 'whatis11plus'})


def findus(request):

    return render(request, 'home/findus.html', {
        'nbar': 'findus',
    })


def testimonials(request):
    return render(request, 'home/testimonials.html', {'nbar': 'testimonials'})


def login(request):
    return render(request, 'home/login.html')

@login_required()
def account(request):
    return render(request, 'account/account.html')


@user_passes_test(lambda u: u.is_superuser)
def addstudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.classID.tutor = request.user
            post.save()
            return redirect('account')
    else:
        form = StudentForm()
    return render(request, 'account/addstudent.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def uploadquestions(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        error = handle_file(myfile)
        print(error)
        request.session['error'] = error
        return HttpResponseRedirect(reverse('uploadquestions'))

        #return render(request, 'account/uploadquestions.html', {
        #    'uploaded_file_url': error
        #})
    return render(request, 'account/uploadquestions.html', {
            'uploaded_file_url': request.session.get('error', 'No file uploaded')
        })


@login_required()
def generatepack(request):
    categories = CategoryChoiceForm()

    if request.method == 'POST':
        if 'generatepack' in request.POST:
            form = StudentChoiceForm(data=request.POST, user=request.user)
            form_category = CategoryChoiceForm(data=request.POST)
            if form.is_valid() and form_category.is_valid():
                createPDF(student=form.cleaned_data['students'], category=form_category.cleaned_data['choice_field'], user=request.user)
                return HttpResponseRedirect('generatepack')
        elif 'viewhomework' in request.POST:
            form = StudentChoiceForm(data=request.POST, user=request.user)
            if form.is_valid():
                # create lists of all the homeworks and their dates
                homeworks =[]
                dates = []
                links = []
                student = form.cleaned_data['students']
                folder = os.path.join(BASE_DIR, 'home', 'media', 'homework',
                                         str(student.classID.time), str(student.id))
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        homeworks.append(file)
                        date = file[-14:]
                        date = date[:-4]
                        dates.append(date)
                        links.append(os.path.join('media', 'homework', str(student.classID.time), str(student.id), file))
                # order from newest to oldest
                dates.reverse()
                homeworks.reverse()
                links.reverse()
                homeworks = zip(dates, homeworks, links)
                return render(request, 'account/generatepack.html', {
                    'students': form,
                    'homeworks': homeworks,
                    'categories': categories,
                })
        else:
            form = StudentChoiceForm(user=request.user)
    else:
        form = StudentChoiceForm(user=request.user)

    return render(request, 'account/generatepack.html',
                  {'students': form,
                   'categories': categories,
    })


@login_required()
def inputscores(request):
    if request.method == 'POST':
        if 'selectstudent' in request.POST:

            form = StudentChoiceForm(data=request.POST, user=request.user)

            if form.is_valid():

                # create forms
                student = form.cleaned_data['students']
                request.session['studentID'] = student.id

                queryset = QuestionDone.objects.filter(score=-1, student=student)

                QuestionDoneFormSet = inlineformset_factory(Student, QuestionDone, fields=('score',), can_delete=True, extra=0)
                formset = QuestionDoneFormSet(instance=student, queryset=queryset)

                # create dict of questions
                questions = []
                for q in queryset:
                    questions.append(q.question)

                questions_and_formset = zip(questions, formset)
                form = StudentChoiceForm(user=request.user)

                return render(request, 'account/inputscores.html',
                              {'students': form,
                               'questions_and_formset': questions_and_formset,
                               'formset': formset,
                               })
            else:
                return render(request, 'account/inputscores.html',
                              {'students': form,
                               })

        # if scores are inputted
        elif 'inputscores' in request.POST:

            student = Student.objects.get(id=request.session['studentID'])
            QuestionDoneFormSet = inlineformset_factory(Student, QuestionDone, fields=('score',), extra=0)
            queryset = QuestionDone.objects.filter(score=-1, student=student)
            formset = QuestionDoneFormSet(request.POST, request.FILES, instance=student)

            if formset.is_valid():
                formset.save()

            queryset = QuestionDone.objects.filter(score=-1, student=student)

            QuestionDoneFormSet = inlineformset_factory(Student, QuestionDone, fields=('score',), extra=0)
            formset = QuestionDoneFormSet(instance=student, queryset=queryset)

            # create dict of questions
            questions = []
            for q in queryset:
                questions.append(q.question)

            questions_and_formset = zip(questions, formset)
            form = StudentChoiceForm(user=request.user)

            return render(request, 'account/inputscores.html',
                          {'students': form,
                           'questions_and_formset': questions_and_formset,
                           'formset': formset,
                           })

        # if something else happens?
        else:
            print('hmm not working')
            form = StudentChoiceForm(user=request.user)

            return render(request, 'account/inputscores.html',
                          {'students': form,
                           })
    else:
        form = StudentChoiceForm(user=request.user)

        return render(request, 'account/inputscores.html',
                  {'students': form,
                   })

@user_passes_test(lambda u: u.is_superuser)
def attendance(request):
    classChoiceForm = ClassChoiceForm(user=request.user)
    if request.method == 'POST':
        classChoiceForm = ClassChoiceForm(data=request.POST, user=request.user)
        if classChoiceForm.is_valid():

            classID = classChoiceForm.cleaned_data['classes'].id
            students = Student.objects.filter(classID=classID)

            attendanceForms = createAttendanceForms(students)

            classChoiceForm = ClassChoiceForm(user=request.user)

            return render(request, 'account/attendance.html',
                          {'form': classChoiceForm,
                           'students': students,
                           'attendanceForms': attendanceForms,

                          })
    else:
        return render(request, 'account/attendance.html',
                      {'form': classChoiceForm,
                       })
