from . import views
from django.conf.urls import url

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
]