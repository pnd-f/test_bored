import json
import os
import re

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

from bb.models import Activity
from django.conf import settings


def index(request):
    activities = Activity.objects.order_by('-id')
    return render(
        request,
        'index.html',
        context={'activities': activities},
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
        
        # 4. Обрабатываем проблемные поля
        # Исправляем link - если пустая строка, устанавливаем None
        if 'link' in data and data['link'] == '':
            data['link'] = None
            
        # Преобразуем accessibility в float
        if 'accessibility' in data:
            try:
                data['accessibility'] = float(data['accessibility'])
            except (ValueError, TypeError):
                data['accessibility'] = 0.5  # значение по умолчанию
                
        # Преобразуем availability в float если есть
        if 'availability' in data and data['availability'] is not None:
            try:
                data['availability'] = float(data['availability'])
            except (ValueError, TypeError):
                data['availability'] = None
        
        activity = Activity(**data)
        activity.save()
        return redirect(index)

def delete(request, activity_id):
    if request.method == 'DELETE':
        Activity.objects.filter(id=activity_id).delete()
        return redirect(index)
    return HttpResponse(status=404)


def envvar(request):
    vv = dict(os.environ)
    connection_string = settings.MONGODB_CONNECTION
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
