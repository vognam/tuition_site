# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import ContactForm

# new imports that go at the top of the file
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template


def index(request):
    return render(request, 'home/index.html', {'nbar': 'home'})


def aboutus(request):
    return render(request, 'home/aboutus.html', {'nbar': 'aboutus'})


def meettheteam(request):
    return render(request, 'home/meettheteam.html', {'nbar': 'meettheteam'})


def pricing(request):
    return render(request, 'home/pricing.html', {'nbar': 'pricing'})


def bookings(request):
    return render(request, 'home/bookings.html', {'nbar': 'bookings'})


def philosophy(request):
    return render(request, 'home/philosophy.html', {'nbar': 'philosophy'})


def whatis11plus(request):
    return render(request, 'home/whatis11plus.html', {'nbar': 'whatis11plus'})


def findus(request):
    form_class = ContactForm

    # TODO - code for emailing
    '''
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            # store form content into variables
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_message = request.POST.get('form_message', '')

            # create template with context and render it
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_message': form_message
            })
            content = template.render(context)

            # subject, body, from, list of 'to', headers
            email = EmailMessage(
                "Tuition query from website",
                content,
                "Your website" + '',
                ['youremail@gmail.com'],
                headers={'Reply-To': contact_email }
            )

            email.send()
            return redirect('findus')
    '''

    return render(request, 'home/findus.html', {
        'nbar': 'findus',
        'form': form_class,
    })


def testimonials(request):
    return render(request, 'home/testimonials.html', {'nbar': 'testimonials'})