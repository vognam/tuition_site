from . import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^aboutus', views.aboutus, name="aboutus"),
    url(r'^meettheteam', views.meettheteam, name="meettheteam"),
    url(r'^pricing', views.pricing, name="pricing"),
    url(r'^bookings', views.bookings, name="bookings"),
    url(r'^success$', views.success, name="success" ),
    url(r'^philosophy', views.philosophy, name="philosophy"),
    url(r'^whatis11plus', views.whatis11plus, name="whatis11plus"),
    url(r'^findus', views.findus, name="findus"),
    url(r'^testimonials', views.testimonials, name="testimonials"),
    url(r'^login', auth_views.login, {'template_name': 'home/login.html'}, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    url(r'^account', views.account, name='account'),
    url(r'^addstudent', views.addstudent, name='addstudent'),
    url(r'^addtutor', views.addtutor, name='addtutor'),
    url(r'^uploadquestions', views.uploadquestions, name='uploadquestions'),
    url(r'^generatepack', views.generatepack, name='generatepack'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
