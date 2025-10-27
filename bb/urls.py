from django.urls import path

from bb.views import index, create, delete, get_activity, envvar, about

urlpatterns = [
    path('', index, name='index'),

    path('create/', create, name='create-a'),
    path('get/', get_activity, name='get-a'),
    path('delete/<activity_id>/', delete, name='delete-a'),
    path('envvars', envvar, name='envvars'),
    path('about/', about, name='about'),
]
