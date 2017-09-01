# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import smtplib
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import StudentForm, TutorForm, StudentChoiceForm

from.models import Question
import zipfile as zf
import shutil
import sqlite3
import os
from django.core.files import File
import re


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


@login_required()
def addstudent(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('account')
    else:
        form = StudentForm()
    return render(request, 'account/addstudent.html', {'form': form})


@login_required()
def addtutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('account')
    else:
        form = TutorForm()
    return render(request, 'account/addtutor.html', {'form': form})


@login_required()
def uploadquestions(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        error = handle_file(myfile)
        print(error)
        return render(request, 'account/uploadquestions.html', {
            'uploaded_file_url': error
        })
    return render(request, 'account/uploadquestions.html')


# handle the uploaded file
# unzip file, get all questions from DB, save them as models
def handle_file(file):
    try:
        # extract zip into a folder
        if os.path.isdir('./extraction'):
            shutil.rmtree('./extraction')
        input_zip = zf.ZipFile(file, 'r')
        input_zip.extractall('./extraction')

        # see if the database exists and connect to it
        if os.path.isfile('./extraction/Categoriser-master/data.db'):
            db = sqlite3.connect('./extraction/Categoriser-master/data.db')
            cursor = db.cursor()
            cursor.execute('SELECT * FROM questions')
            all_rows = cursor.fetchall()

            for row in all_rows:
                print(row)

            last_id = get_last_qid()
            rename_questions(last_id)

            for row in all_rows:

                last_id += 1
                print('./extraction/Categoriser-master{}'.format(row[7][1:]))
                print(os.path.basename(row[7]))
                question = Question(category=row[1], difficulty=row[2], out_of=row[3],
                                    answer=row[6])
                question.save()
                question.image.save(
                    'QID{}.jpg'.format(last_id),
                    File(open('./extraction/Categoriser-master/questions/QID{}.jpg'.format(last_id), str('rb')))
                )
            db.close()
            return 'Uploaded success!'
    except Exception as e:
        return 'Upload failed: ' + str(e)


# Get the last question id
def get_last_qid():
    print('getting last id')
    all_questions = Question.objects.all()
    if len(all_questions) == 0:
        return 0
    else:
        path = os.path.basename(str(all_questions[len(all_questions)-1].image))
        print('got last id {}'.format(path))
        return int(path[3:-4])


# Rename the question jpgs in the uploaded file
def rename_questions(last_id):
    print('renaming files - last_id = ' + str(last_id))
    folder = './extraction/Categoriser-master/questions'

    # natural sort and reverse order the list of questions
    lst = os.listdir(folder)
    lst = natural_sort(lst)
    lst.reverse()

    for filename in lst:
        if filename.endswith('.jpg'):
            # print('first file doing')
            # last_id += 1
            question_id = int(filename[3:-4])
            print('file is {}/{}'.format(folder, filename))
            os.rename('{}/{}'.format(folder, filename), '{}/QID{}.jpg'.format(folder, question_id + last_id))


# sort numerically
def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)


@login_required()
def generatepack(request):

    if request.method == 'POST':
        form = StudentChoiceForm(request.POST)
        if form.is_valid():

            return redirect('generatepack')
    else:
        form = StudentChoiceForm()

    return render(request, 'account/generatepack.html',
                  {'students': form,
    })
