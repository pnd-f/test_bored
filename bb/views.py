import json
import os
import re

import requests
from django.shortcuts import render, redirect

from bb.models import Activity
from django.conf import settings
from django.http import HttpResponse


def index(request):
    activities = Activity.objects.all().order_by('-id')
    return render(
        request,
        'index.html',
        context={'activities': activities}
    )


def get_activity(request):
    response = requests.get(settings.BORED_URL)
    details = response.json()
    context = {
        'details': details
    }
    return render(
        request,
        template_name='details.html',
        context=context
    )


def create(request):
    if request.method == 'POST':
        data = request.POST
        json_data: str = data['activity']
        # 1. Заменяем одинарные кавычки вокруг ключей и значений на двойные
        cleaned = re.sub(r"(?<=[:\s])'([^']*)'", r'"\1"', json_data)  # значения
        cleaned = re.sub(r"'(\w+)'(?=\s*:)", r'"\1"', cleaned)  # ключи

        # 2. Приводим Python-логические значения к JSON
        cleaned = cleaned.replace("True", "true").replace("False", "false").replace("None", "null")

        # 3. Загружаем как JSON
        data = json.loads(cleaned)

        data['activity_type'] = data.pop('type')
        Activity.objects.create(**data)
        return redirect(index)


def delete(request, activity_id):
    if request.method == 'DELETE':
        Activity.objects.filter(id=activity_id).delete()
        return redirect(index)
    return HttpResponse(status=404)


def envvar(request):
    vv = dict(os.environ)
    connection_string = settings.POSTGRES_CONNECTION
    return render(
        request,
        'envvars.html',
        context={'vars': vv, 'connection_string': connection_string},
    )


def about(request):
    return render(
        request,
        'about.html'
    )
