# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


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
            email = form.cleaned_data['contact_email']
            message = form.cleaned_data['contact_message']
            try:
                send_mail('Booking query', name + '\n' + message, email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "home/bookings.html", {
        'form': form,
        'nbar': 'bookings'})


def success(request):
    return HttpResponse('Success! Thank you for your message.')


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