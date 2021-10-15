import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .models import TFinances


def index(request):
    template = loader.get_template('finances/index.html')
    context = {}

    return HttpResponse(template.render(context, request))


def simple_upload(request):
    print('entrou')
    template = loader.get_template('finances/success.html')
    context = {}
    if request.method == 'POST':
        files = request.FILES
        for file in files:
            data = str(files[file].read().decode('utf-8')).split('\n')
            data = format_file(data[:-1])
            TFinances.objects.bulk_create(data, 100)
        print('passou')
    # return HttpResponse(template.render(context, request))
    # return render(request, 'finances/success.html', context)
    return redirect('success')


def success(request):
    return render(request, 'finances/success.html')


def format_file(data):
    new_data = list()
    for obj in data:
        new_data.append(TFinances(
          type=obj[0],
          desc_type=get_description_type(obj[0]),
          date_hour=format_date_hour(obj[1:9] + ' ' + obj[42:48]),
          value=int(obj[9:19])/100,
          cpf=obj[19:30],
          card=obj[30:42],
          store_owner=obj[48:62].rstrip(),
          store=obj[62:].rstrip()
        ))
    return new_data


def format_date_hour(date):
    return datetime.strptime(date, '%Y%m%d %H%M%S')


def get_description_type(value):
    desc = {
        '1': 'Débito',
        '2': 'Boleto',
        '3': 'Financiamento',
        '4': 'Crédito',
        '5': 'Recebimento Empréstimo',
        '6': 'Vendas',
        '7': 'Recebimento TED',
        '8': 'Recebimento DOC',
        '9': 'Aluguel'
    }
    return desc[value]
