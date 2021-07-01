
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home),
    path('my-slots/', my_slots),
    path('check-slot/', check_slot),
    path('book-slot/', book_slot),
]
