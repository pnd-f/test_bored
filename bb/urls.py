from django.urls import path

from bb.views import index, create, get_activity, about

urlpatterns = [
    path('', index, name='index'),

    path('create/', create, name='create-a'),
    path('get/', get_activity, name='get-a'),
    path('about/', about, name='about'),
]
