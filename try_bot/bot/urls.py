from django.conf.urls import url,include
from django.contrib import admin
from .views import trybotview

urlpatterns = [
url(r'^66d2b8f4a09cd35cb23076a1da5d51529136a3373fd570b122/?$', trybotview.as_view()),
]

