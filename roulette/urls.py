from django.urls import path

from roulette.views import SpinRouletteAPI, StaticSpinAPI, StaticUserAPI

app_name = 'roulette'

urlpatterns = [
    path('spin/', SpinRouletteAPI.as_view(), name='spin'),
    path('static-spin', StaticSpinAPI.as_view()),
    path('static-user', StaticUserAPI.as_view()),
]
